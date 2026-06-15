# SPDX-FileCopyrightText: 2019-2026 The ALS Authors
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Provides everything need to handle ALS main inputs : images.

We need to read file and in the future, get images from INDI
"""
from abc import abstractmethod
from logging import getLogger
from pathlib import Path
from typing import Optional

import cv2
import exifread
from PyQt5.QtCore import pyqtSignal, QObject, QT_TRANSLATE_NOOP
from astropy.io import fits
from rawpy import imread
from rawpy._rawpy import LibRawNonFatalError, LibRawFatalError
from watchdog.events import FileSystemEventHandler
from watchdog.observers.polling import PollingObserver

from als import config
from als.code_utilities import AlsLogAdapter, log
from als.crunching import _normalize_bayer_flat, _normalize_global_flat
from als.messaging import MESSAGE_HUB
from als.model.base import Image
from als.model.data import DYNAMIC_DATA

_LOGGER = AlsLogAdapter(getLogger(__name__), {})

_IGNORED_FILENAME_START_PATTERNS = ['.', '~', 'tmp']
EXPOSURE_TIME_EXIF_TAG = 'EXIF ExposureTime'
SCANNER_TYPE_FILESYSTEM = "FS"
FOLDER_SCANNER_THREAD_NAME = "folder-scanner"


class InputError(Exception):
    """
    Base class for all Exception subclasses in this module
    """


class ScannerStartError(InputError):
    """
    Raised when folder scanner start is in error.
    """


class InputScanner:
    """
    Base abstract class for all code responsible of ALS "image acquisition".

    Subclasses are responsible for :

      - replying to start & stop commands
      - reading images from actual source
      - creating Image objects
      - broadcasting every new image
    """

    new_image_path_signal = pyqtSignal(str)
    """Qt signal emitted when a new image is detected by scanner"""

    @log
    def broadcast_image_path(self, path: str):
        """
        Send a signal with newly detected image path to anyone who cares

        :param path: the new image path
        :type path: str
        """
        if path is not None:
            self.new_image_path_signal.emit(path)

    @abstractmethod
    def start(self):
        """
        Starts checking for new images

        :raises: ScannerStartError if startup fails
        """

    @abstractmethod
    def stop(self):
        """
        Stops checking for new images
        """

    @staticmethod
    @log
    def create_scanner(scanner_type: str = SCANNER_TYPE_FILESYSTEM):
        """
        Factory for image scanners.

        :param scanner_type: the type of scanner to create. Accepted values are :

          - "FS" for a filesystem scanner

        :type scanner_type: str.

        :return: the right scanner implementation
        :rtype: InputScanner subclass
        """

        if scanner_type == SCANNER_TYPE_FILESYSTEM:
            return FolderScanner()

        raise ValueError(f"Unsupported scanner type : {scanner_type}")


class FolderScanner(FileSystemEventHandler, InputScanner, QObject):
    """
    Watches file changes (creation, move) in a specific filesystem folder

    the watched directory is retrieved from user config on scanner startup
    """
    @log
    def __init__(self):
        FileSystemEventHandler.__init__(self)
        InputScanner.__init__(self)
        QObject.__init__(self)
        self._observer = None

    @log
    def start(self):
        """
        Starts scanning scan folder for new files
        """
        try:
            scan_folder_path = config.get_scan_folder_path()
            self._observer = PollingObserver()
            self._observer.name = FOLDER_SCANNER_THREAD_NAME
            self._observer.schedule(self, scan_folder_path, recursive=True)
            self._observer.start()
        except OSError as os_error:
            raise ScannerStartError(os_error)

    @log
    def stop(self):
        """
        Stops scanning scan folder for new files
        """
        if self._observer is not None:
            self._observer.stop()
            self._observer = None

    @log
    def on_moved(self, event):
        if event.event_type == 'moved':
            image_path = event.dest_path
            if not self._must_ignore_file(image_path):
                _LOGGER.debug(f"File move detected : {image_path}")
                self.broadcast_image_path(image_path)

    @log
    def on_created(self, event):
        if event.event_type == 'created':
            image_path = event.src_path
            if not self._must_ignore_file(image_path):
                _LOGGER.debug(f"File creation detected : {image_path}")
                self.broadcast_image_path(image_path)

    @log
    def _must_ignore_file(self, image_path):
        """
        Check if the image path should be ignored based on the start patterns

        :param image_path: the path to check
        :type image_path: str
        :return: True if the file should be ignored, False otherwise
        :rtype: bool
        """
        for pattern in _IGNORED_FILENAME_START_PATTERNS:
            if Path(image_path).name.startswith(pattern):
                _LOGGER.debug(f"File '{image_path}' ignored : Matches filename start ignore pattern '{pattern}'")
                return True
        return False

@log
def read_disk_image(path: Path):
    """
    Reads an image from disk

    :param path: path to the file to load image from
    :type path:  pathlib.Path

    :return: the image read from disk or None if image is ignored or an error occurred
    :rtype: Image or None
    """

    image = None

    if path.suffix.lower() in ['.fit', '.fits', '.fts']:
        image = _read_fit_image(path)

    elif path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.tif', '.tiff']:
        image = _read_standard_image(path)
    else:
        image = _read_raw_image(path)

    if image is not None:
        image.origin = f"FILE : {str(path.resolve())}"
        MESSAGE_HUB.dispatch_info(
            __name__,
            QT_TRANSLATE_NOOP("", "Successful image read from {}"),
            [image.origin, ]
        )

    return image


@log
def _read_fit_image(path: Path):
    """
    read FIT image from filesystem

    :param path: path to image file to load from
    :type path: pathlib.Path

    :return: the loaded image, with data and headers parsed or None if a known error occurred
    :rtype: Image or None
    """
    try:
        with fits.open(str(path.resolve())) as fit:
            # pylint: disable=E1101
            image_hdu = None

            if fit[0].data is not None:
                image_hdu = fit[0]
            else:
                for hdu in fit[1:]:
                    if isinstance(hdu, (fits.ImageHDU, fits.CompImageHDU)) and hdu.data is not None:
                        image_hdu = hdu
                        break

            if image_hdu is None:
                raise ValueError("No image data found in FITS file")

            data = image_hdu.data
            header = image_hdu.header

        image = Image(data)

        if 'BAYERPAT' in header:
            image.bayer_pattern = header['BAYERPAT']

        if 'EXPTIME' in header:
            image.exposure_time = header['EXPTIME']
            _LOGGER.debug(f"*SD-EXP_T* extracted exposure time: {image.exposure_time}")

    except (OSError, TypeError, ValueError) as error:
        _report_fs_error(path, error)
        return None

    return image


@log
def _read_standard_image(path: Path):
    """
    read standard image from filesystem using OpenCV

    :param path: path to image file to load from
    :type path: pathlib.Path

    :return: the loaded image or None if a known error occurred
    :rtype: Image or None
    """

    data = cv2.imread(str(path.resolve()), cv2.IMREAD_UNCHANGED)

    if data is None:
        _LOGGER.warning("Could not read image at %s; file is ignored", path)
        return None

    # convert color layers order for color images
    if data.ndim > 2:
        data = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)

    return Image(data)


@log
def _read_raw_image(path: Path):
    """
    Reads a RAW DLSR image from file

    :param path: path to the file to read from
    :type path: pathlib.Path

    :return: the image or None if a known error occurred
    :rtype: Image or None
    """

    try:
        with imread(str(path.resolve())) as raw_image:

            # in here, we make sure we store the bayer pattern as it would be advertised if image was a FITS image.
            #
            # lets assume image comes from a DSLR sensor with the most common bayer pattern.
            #
            # The actual/physical bayer pattern would look like a repetition of :
            #
            # +---+---+
            # | R | G |
            # +---+---+
            # | G | B |
            # +---+---+
            #
            # RawPy will report the bayer pattern description as 2 discrete values :
            #
            # 1) raw_image.raw_pattern : a 2x2 numpy array representing the indices used to express the bayer patten
            #
            # in our example, its value is :
            #
            # +---+---+
            # | 0 | 1 |
            # +---+---+
            # | 3 | 2 |
            # +---+---+
            #
            # and its flatten version is :
            #
            # [0, 1, 3, 2]
            #
            # 2) raw_image.color_desc : a bytes literal formed of the color of each pixel of the bayer pattern, in
            #                           ascending index order from raw_image.raw_pattern
            #
            # in our example, its value is : b'RGBG'
            #
            # We need to express/store this pattern in a more common way, i.e. as it would be described in a FITS
            # header. Or put simply, we want to express the bayer pattern as it would be described if
            # raw_image.raw_pattern was :
            #
            # +---+---+
            # | 0 | 1 |
            # +---+---+
            # | 2 | 3 |
            # +---+---+
            bayer_pattern_indices = raw_image.raw_pattern.flatten()
            bayer_pattern_desc = raw_image.color_desc.decode()

            _LOGGER.debug(f"Bayer pattern indices = {bayer_pattern_indices}")
            _LOGGER.debug(f"Bayer pattern description = {bayer_pattern_desc}")

            assert len(bayer_pattern_indices) == len(bayer_pattern_desc)
            bayer_pattern = ""
            for i, index in enumerate(bayer_pattern_indices):
                assert bayer_pattern_indices[i] < len(bayer_pattern_indices)
                bayer_pattern += bayer_pattern_desc[index]

            _LOGGER.debug(f"Computed, FITS-compatible bayer pattern = {bayer_pattern}")

            new_image = Image(raw_image.raw_image_visible.copy())
            new_image.bayer_pattern = bayer_pattern

            extract_exifs(new_image, path)

            return new_image

    except LibRawNonFatalError as non_fatal_error:
        _report_fs_error(path, non_fatal_error)
        return None
    except LibRawFatalError as fatal_error:
        _report_fs_error(path, fatal_error)
        return None


@log
def extract_exifs(image, image_path):
    """
    Try and get some exifs from the image file

    For now, we only look for exposure time, but who knows...
    The image in modified in place

    :param image: the image to feed
    :type image: Image

    :param image_path: path to original file
    :type image_path: Path

    :return: None
    """
    with open(image_path, 'rb') as raw:
        tags = exifread.process_file(raw)
        if tags and EXPOSURE_TIME_EXIF_TAG in tags.keys():
            exposure_time = float(tags[EXPOSURE_TIME_EXIF_TAG].values[0])
            _LOGGER.debug(f"*SD-EXP_T* extracted exposure time: {exposure_time}")
            image.exposure_time = exposure_time


@log
def _report_fs_error(path: Path, error: Exception):
    MESSAGE_HUB.dispatch_error(
        __name__,
        QT_TRANSLATE_NOOP("", "Error reading from file {} : {}"),
        [str(path.resolve()), str(error)])


@log
def get_cached_master_dark(master_dark_path: str) -> Optional[Image]:
    """
    Retrieves the master dark frame from in-session cache or disk if missing.

    :param master_dark_path: filesystem path to the master dark file
    :type master_dark_path: str

    :return: the cached or freshly read master dark, None if unavailable
    :rtype: Optional[Image]
    """
    if not master_dark_path:
        return None

    if DYNAMIC_DATA.master_dark is not None:
        _LOGGER.debug("Using cached master dark: %s", master_dark_path)
        return DYNAMIC_DATA.master_dark

    dark = read_disk_image(Path(master_dark_path))
    if dark is not None:
        _LOGGER.debug("Loaded master dark from disk: %s", master_dark_path)
        DYNAMIC_DATA.master_dark = dark
    else:
        _LOGGER.debug("Failed to load master dark from disk: %s", master_dark_path)

    return dark


@log
def get_cached_master_flat(master_flat_path: str, bayer_pattern: Optional[str]) -> Optional[Image]:
    """
    Retrieves the master flat from cache or disk and stores a normalized float32 version in cache.

    :param master_flat_path: filesystem path to the master flat file
    :type master_flat_path: str
    :param bayer_pattern: Bayer pattern extracted from the first sub, if applicable
    :type bayer_pattern: Optional[str]
    :return: the cached or freshly read normalized master flat, None if unavailable
    :rtype: Optional[Image]
    """
    if not master_flat_path:
        return None

    if DYNAMIC_DATA.master_flat is not None:
        _LOGGER.debug("Using cached normalized master flat: %s", master_flat_path)
        return DYNAMIC_DATA.master_flat

    flat = read_disk_image(Path(master_flat_path))
    if flat is None:
        _LOGGER.debug("Failed to load master flat from disk: %s", master_flat_path)
        return None

    _LOGGER.debug("Loaded master flat from disk: %s", master_flat_path)

    if bayer_pattern:
        flat = _normalize_bayer_flat(flat, master_flat_path, bayer_pattern)
    else:
        flat = _normalize_global_flat(flat, master_flat_path)

    if flat is not None:
        DYNAMIC_DATA.master_flat = flat

    return flat
