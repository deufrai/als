# SPDX-FileCopyrightText: 2019-2026 The ALS Authors
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Provides all means of image processing
"""
import threading
import time
from abc import abstractmethod
from logging import getLogger
from pathlib import Path
from typing import List, Optional

import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal, QT_TRANSLATE_NOOP, QFileInfo
from PyQt5.QtGui import QPixmap
from qimage2ndarray import array2qimage

from als import config
from als.code_utilities import human_readable_byte_size, available_memory
from als.code_utilities import log, Timer, SignalingQueue, AlsLogAdapter
from als.crunching import compute_histograms_for_display
from als.messaging import MESSAGE_HUB
from als.model.base import Image
from als.model.data import DYNAMIC_DATA, I18n, AVAILABLE_PROFILES
from als.model.params import ProcessingParameter, RangeParameter, SwitchParameter
from als.streams.input import get_cached_master_dark, get_cached_master_flat, read_disk_image
from contrib.stretch import Stretch

_LOGGER = AlsLogAdapter(getLogger(__name__), {})

_16_BITS_MAX_VALUE = 2**16 - 1
_HOT_PIXEL_RATIO = 1.25
_HOT_PIXEL_MIN_DELTA = 256
_DARK_SUBTRACTION_CLIPPING_WARNING_THRESHOLD = 0.01


class ProcessingError(Exception):
    """
    Must be raised in case of processing error.
    """


# pylint: disable=R0903
class ImageProcessor:
    """
    Base abstract class for all image processors, regardless of what pipeline they are used in

    Subclasses must implement a single method : process_image(image: Image)
    """

    @log
    def __init__(self):
        self._parameters = list()

    @log
    def get_parameters(self) -> List[ProcessingParameter]:
        """
        Gets processes parameters

        :return: the parameters
        :rtype: List[ProcessingParameter]
        """
        return self._parameters

    @abstractmethod
    def process_image(self, image: Image):
        """
        Perform  image processing specific to this class

        :param image: the image to process
        :type image: Image

        :raises: ProcessingError - an error occurred while processing image

        :return: the processed image
        :rtype: Image
        """


class ColorBalance(ImageProcessor):
    """
    Implements color balance processing
    """

    _HISTOGRAM_BIN_COUNT = 512

    @log
    def __init__(self):

        super().__init__()

        self._parameters.append(
            SwitchParameter(
                "active",
                I18n.TOOLTIP_RGB_ACTIVE,
                default=True
            )
        )

        self._parameters.append(
            RangeParameter(
                "red",
                I18n.TOOLTIP_RED_LEVEL,
                default=1,
                minimum=0,
                maximum=2
            )
        )

        self._parameters.append(
            RangeParameter(
                "green",
                I18n.TOOLTIP_GREEN_LEVEL,
                default=1,
                minimum=0,
                maximum=2
            )
        )

        self._parameters.append(
            RangeParameter(
                "blue",
                I18n.TOOLTIP_BLUE_LEVEL,
                default=1,
                minimum=0,
                maximum=2
            )
        )

        self._parameters.append(
            RangeParameter(
                "saturation",
                I18n.TOOLTIP_SATURATION_LEVEL,
                default=1,
                minimum=0,
                maximum=2
            )
        )

    @log
    def process_image(self, image: Image):
        """
        Performs RGB balance

        :param image: the image to process
        :type image: Image
        """

        for param in self._parameters:
            _LOGGER.debug(f"Color balance param {param.name} = {param.value}")

        active = self._parameters[0]
        red = self._parameters[1]
        green = self._parameters[2]
        blue = self._parameters[3]
        saturation = self._parameters[4]

        if active.value:
            red_value = red.value if red.value > 0 else 0.1
            green_value = green.value if green.value > 0 else 0.1
            blue_value = blue.value if blue.value > 0 else 0.1

            processed = False

            if not red.is_default():
                image.data[0] = image.data[0] * red_value
                processed = True

            if not green.is_default():
                image.data[1] = image.data[1] * green_value
                processed = True

            if not blue.is_default():
                image.data[2] = image.data[2] * blue_value
                processed = True

            if not saturation.is_default():

                mean_channel = np.mean(image.data, axis=0)

                if saturation.value > saturation.default:

                    saturation_mask = self._build_saturation_mask(mean_channel)

                    if np.any(saturation_mask):
                        saturated_data = mean_channel + (image.data - mean_channel) * saturation.value
                        image.data = np.where(saturation_mask, saturated_data, image.data)

                else:
                    image.data = mean_channel + (image.data - mean_channel) * saturation.value


                processed = True

            if processed:
                image.data = np.clip(image.data, 0, _16_BITS_MAX_VALUE)

        return image

    @staticmethod
    def _build_saturation_mask(luminance: np.ndarray) -> np.ndarray:
        """
        Build a mask of pixels considered as above background luminance

        :param luminance: the image luminance data
        :return: a boolean array where True means the pixel is above background luminance
        """
        histogram, bin_edges = np.histogram(
            luminance, ColorBalance._HISTOGRAM_BIN_COUNT, range=(0, _16_BITS_MAX_VALUE)
        )

        peak_index = int(np.argmax(histogram))
        descending_end_index = len(histogram)

        for index in range(peak_index + 1, len(histogram)):
            if histogram[index] >= histogram[index - 1]:
                descending_end_index = index
                break

        threshold_value = bin_edges[descending_end_index]
        return luminance >= threshold_value


class AutoStretch(ImageProcessor):
    """
    Implements auto stretch feature
    """

    @log
    def __init__(self):
        super().__init__()

        self._parameters.append(
            SwitchParameter(
                "active",
                I18n.TOOLTIP_STRETCH_ACTIVE,
                default=True))

        self._parameters.append(
            RangeParameter(
                "strength",
                I18n.TOOLTIP_STRETCH_STRENGTH,
                default=0.18,
                minimum=0,
                maximum=1))

    @log
    def process_image(self, image: Image):

        for param in self._parameters:
            _LOGGER.debug(f"Autostretch param {param.name} = {param.value}")

        active = self._parameters[0]
        stretch_strength = self._parameters[1]

        # make sure, as we are the first process in the pipeline, that our changes are made
        # on a copy of the received image. So whoever kept a ref to it won't be affected
        image = image.clone()

        if active.value:

            _LOGGER.debug("Performing Autostretch...")
            image.data = np.interp(image.data,
                                   (image.data.min(), image.data.max()),
                                   (0, _16_BITS_MAX_VALUE))

            if image.is_color():
                for channel in range(3):
                    image.data[channel] = Stretch(target_bkg=stretch_strength.value).stretch(image.data[channel])
            else:
                image.data = Stretch(target_bkg=stretch_strength.value).stretch(image.data)
            _LOGGER.debug("Autostretch Done")

            # autostretch output range is [0, 1]
            # so we remap values to our range [0, Levels._UPPER_LIMIT]
            image.data *= _16_BITS_MAX_VALUE

        return image


class Levels(ImageProcessor):
    """Implements levels processing"""

    @log
    def __init__(self):
        super().__init__()

        self._parameters.append(
            SwitchParameter(
                "active",
                I18n.TOOLTIP_LEVELS_ACTIVE,
                default=True))

        self._parameters.append(
            RangeParameter(
                "black",
                I18n.TOOLTIP_BLACK_LEVEL,
                default=0,
                minimum=0,
                maximum=_16_BITS_MAX_VALUE))

        self._parameters.append(
            RangeParameter(
                "mids",
                I18n.TOOLTIP_MIDTONES_LEVEL,
                default=1,
                minimum=0,
                maximum=2))

        self._parameters.append(
            RangeParameter(
                "white",
                I18n.TOOLTIP_WHITE_LEVEL,
                default=_16_BITS_MAX_VALUE,
                minimum=0,
                maximum=_16_BITS_MAX_VALUE))

    @log
    def process_image(self, image: Image):
        # pylint: disable=R0914

        active = self._parameters[0]
        black = self._parameters[1]
        midtones = self._parameters[2]
        white = self._parameters[3]

        for param in self._parameters:
            _LOGGER.debug(f"Levels param {param.name} = {param.value}")

        if active.value:
            # midtones correction
            do_midtones = not midtones.is_default()
            _LOGGER.debug(f"Levels : do midtones adjustments : {do_midtones}")

            if do_midtones:
                _LOGGER.debug("Performing midtones adjustments...")
                midtones_value = midtones.value if midtones.value > 0 else 0.1
                image.data = _16_BITS_MAX_VALUE * image.data ** (1 / midtones_value) / _16_BITS_MAX_VALUE ** (
                    1 / midtones_value)
                _LOGGER.debug("Midtones level adjustments Done")

            # black / white levels
            do_black_white_levels = not black.is_default() or not white.is_default()
            _LOGGER.debug(f"Levels : do black and white adjustments : {do_black_white_levels}")

            if do_black_white_levels:
                _LOGGER.debug("Performing black / white level adjustments...")
                image.data = np.clip(image.data, black.value, white.value)
                _LOGGER.debug("Black / white level adjustments Done")

            # final interpolation if we touched the image
            if do_midtones or do_black_white_levels:
                image.data = np.float32(np.interp(image.data,
                                                  (image.data.min(), image.data.max()),
                                                  (0, _16_BITS_MAX_VALUE)))

        return image


# pylint: disable=R0903
class Standardize(ImageProcessor):
    """
    Make image data structure conform to all processing needs.

    Here are the aspects we enforce :

      #. data array of color (debayered) images have color as the first axis. So a typical shape for a color image would
         be : (3, y, x).

      #. each array element is of type float32

    """
    @log
    def process_image(self, image: Image):

        if not image:
            return None

        if image.is_color():
            image.set_color_axis_as(0)

        image.data = np.float32(image.data)

        return image


class HotPixelRemover(ImageProcessor):
    """Provides hot pixels removal"""

    @staticmethod
    def _replace_hot_pixels_from_local_median(data: np.ndarray) -> None:
        """
        Replaces isolated high pixels from same-channel local medians.

        The median is robust against the candidate hot pixel itself, and the
        input array is updated in-place to avoid allocating a replacement image.

        :param data: the image channel to process
        :type data: np.ndarray
        """
        local_median = cv2.medianBlur(np.ascontiguousarray(data), 3)
        median_values = local_median.astype(np.float32)
        threshold = median_values.copy()
        threshold *= _HOT_PIXEL_RATIO
        median_values += _HOT_PIXEL_MIN_DELTA
        np.maximum(threshold, median_values, out=threshold)
        hot_pixels = data > threshold
        data[hot_pixels] = local_median[hot_pixels]

    @staticmethod
    def _replace_bayer_hot_pixels(data: np.ndarray) -> None:
        """
        Removes hot pixels from each Bayer phase independently.

        Bayer raw frames store different colors in adjacent pixels. Processing
        each 2x2 phase plane separately compares each pixel only with nearby
        pixels from the same color position.

        :param data: raw Bayer mosaic image
        :type data: np.ndarray
        """
        for row_offset in range(2):
            for column_offset in range(2):
                HotPixelRemover._replace_hot_pixels_from_local_median(
                    data[row_offset::2, column_offset::2]
                )

    @log
    def process_image(self, image: Image):

        # The detector replaces isolated high pixels with a local median. Raw
        # Bayer frames are processed phase-by-phase so pixels are compared only
        # with same-color neighbors.

        if not image:
            return None

        hpr_on = config.get_hot_pixel_remover()

        _LOGGER.debug(f"Hot pixel remover enabled : {hpr_on}")

        if hpr_on:

            if image.needs_debayering():
                HotPixelRemover._replace_bayer_hot_pixels(image.data)
            elif image.is_bw():
                HotPixelRemover._replace_hot_pixels_from_local_median(image.data)
            else:
                _LOGGER.debug("Hot Pixel Remover skipped on color image")

        return image


# pylint: disable=R0903
class Debayer(ImageProcessor):
    """
    Provides image debayering.
    """

    @log
    def process_image(self, image: Image):

        if not image:
            return None

        preferred_bayer_pattern = config.get_bayer_pattern()

        if preferred_bayer_pattern == "AUTO" and not image.needs_debayering():
            return image

        cv2_debayer_dict = {

            "BG": cv2.COLOR_BAYER_BG2RGB,
            "GB": cv2.COLOR_BAYER_GB2RGB,
            "RG": cv2.COLOR_BAYER_RG2RGB,
            "GR": cv2.COLOR_BAYER_GR2RGB
        }

        if preferred_bayer_pattern != 'AUTO':
            bayer_pattern = preferred_bayer_pattern

            if image.needs_debayering() and bayer_pattern != image.bayer_pattern:
                pattern_mismatch_msg = QT_TRANSLATE_NOOP(
                    "",
                    "The bayer pattern defined in your preferences differs from the one present in current image. "
                    "Preferred: {} vs image: {}. Debayering result may be wrong.")
                pattern_mismatch_values = [preferred_bayer_pattern, image.bayer_pattern]
                MESSAGE_HUB.dispatch_warning(__name__,
                                             pattern_mismatch_msg,
                                             pattern_mismatch_values)

        else:
            bayer_pattern = image.bayer_pattern

        cv_debay = bayer_pattern[3] + bayer_pattern[2]

        try:
            if image.data.dtype not in (np.uint8, np.uint16):
                raise ProcessingError(
                    f"unsupported image data type for debayering: {image.data.dtype}. "
                    "Expected uint8 or uint16"
                )

            debayered_data = cv2.cvtColor(image.data, cv2_debayer_dict[cv_debay])
        except KeyError:
            raise ProcessingError(f"unsupported bayer pattern : {bayer_pattern}")
        except cv2.error as error:
            raise ProcessingError(f"Debayering error : {str(error)}")

        image.data = debayered_data

        return image


class RemoveDark(ImageProcessor):
    """
    Provides image dark removal.
    """

    @log
    def process_image(self, image: Image) -> Optional[Image]:
        """
        Subtracts the configured master dark from the image, using an in-session cache
        to avoid repeated disk reads.

        :param image: the image to process
        :type image: Image

        :return: the processed image or None if processing cannot proceed
        :rtype: Optional[Image]
        """

        if not image:
            return None

        do_subtract = config.get_use_master_dark()

        _LOGGER.debug(f"Dark subtraction enabled : {do_subtract}")

        if do_subtract:

            master_dark_path = config.get_master_dark_file_path()
            dark = get_cached_master_dark(master_dark_path, image.bayer_pattern)

            if dark is None:
                read_error_message = QT_TRANSLATE_NOOP(
                    "",
                    "Could not read master dark {}. Dark subtraction is SKIPPED"
                )
                read_error_values = [master_dark_path, ]
                MESSAGE_HUB.dispatch_warning(__name__, read_error_message, read_error_values)
                return image

            if not image.is_same_shape_as(dark):
                mismatch_message = QT_TRANSLATE_NOOP(
                    "",
                    "Data structure inconsistency. Light: {} vs Master dark: {}. Dark subtraction is SKIPPED"
                )
                mismatch_values = [image.data.shape, dark.data.shape]
                MESSAGE_HUB.dispatch_warning(__name__, mismatch_message, mismatch_values)
                return image

            if image.data.dtype.name != dark.data.dtype.name:

                MESSAGE_HUB.dispatch_info(
                    __name__,
                    QT_TRANSLATE_NOOP(
                        "",
                        "Dark & Light data types mismatch detected. Light: {} vs Master dark: {}. Converting Dark..."
                    ),
                    [image.data.dtype.name, dark.data.dtype.name])

                with Timer() as conforming_timer:

                    try:
                        image_min_allowed, image_max_allowed = RemoveDark._get_allowed_min_and_max(image.data)
                    except TypeError:
                        raise ProcessingError(f"unhandled image data type : {image.data.dtype.type}")

                    try:
                        dark_min_allowed, dark_max_allowed = RemoveDark._get_allowed_min_and_max(dark.data)
                    except TypeError:
                        raise ProcessingError(f"unhandled masterdark data type : {dark.data.dtype.type}")

                    dark_data = np.interp(
                        dark.data,
                        (dark_min_allowed, dark_max_allowed),
                        (image_min_allowed, image_max_allowed)).astype(image.data.dtype)

                dark.data = dark_data
                DYNAMIC_DATA.master_dark = dark

                _LOGGER.debug(f"Dark frame conforming done in {conforming_timer.elapsed_in_milli_as_str} ms")

            else:
                dark_data = dark.data

            _LOGGER.debug("Subtracting dark frame...")

            with Timer() as subtraction_timer:
                image.data = RemoveDark._subtract_dark_data(image.data, dark_data, master_dark_path)
            _LOGGER.debug(f"Dark frame subtracted in {subtraction_timer.elapsed_in_milli_as_str} ms")

        return image

    @staticmethod
    def _get_allowed_min_and_max(data):
        """
        Get the allowed minimum and maximum values according to data type

        :param data: image data
        :type data: numpy.ndarray

        :return: a tuple of 2 values : minimum and maximum allowed values for data type
        """

        if issubclass(data.dtype.type, np.integer):
            allowed_min = np.iinfo(data.dtype).min
            allowed_max = np.iinfo(data.dtype).max
        elif issubclass(data.dtype.type, np.floating):
            allowed_min = 0.0
            allowed_max = 1.0
        else:
            raise TypeError("Data type must be float or integer")

        return allowed_min, allowed_max

    @staticmethod
    def _subtract_dark_data(image_data: np.ndarray, dark_data: np.ndarray, master_dark_path: str) -> np.ndarray:
        """
        Subtracts dark data through a signed intermediate and clips once.

        :param image_data: light image data
        :type image_data: numpy.ndarray
        :param dark_data: master dark data
        :type dark_data: numpy.ndarray
        :param master_dark_path: master dark path used for warning context
        :type master_dark_path: str
        :return: dark-subtracted image data
        :rtype: numpy.ndarray
        """
        subtracted_data = image_data.astype(np.float32) - dark_data.astype(np.float32)
        clipped_pixels = subtracted_data < 0
        clipped_fraction = float(np.count_nonzero(clipped_pixels)) / clipped_pixels.size

        if clipped_fraction > _DARK_SUBTRACTION_CLIPPING_WARNING_THRESHOLD:
            MESSAGE_HUB.dispatch_warning(
                __name__,
                QT_TRANSLATE_NOOP(
                    "",
                    "Dark subtraction with master dark {} clipped {:.1f}% of pixels to black. "
                    "The master dark may be too strong or mismatched."
                ),
                [master_dark_path, clipped_fraction * 100.0]
            )

        if issubclass(image_data.dtype.type, np.integer):
            limits = np.iinfo(image_data.dtype)
            return np.clip(subtracted_data, 0, limits.max).astype(image_data.dtype)

        return np.clip(subtracted_data, 0.0, None).astype(image_data.dtype, copy=False)


class RemoveFlat(ImageProcessor):
    """
    Provides image flat removal.
    """

    @log
    def process_image(self, image: Image) -> Optional[Image]:
        """
        Divides by the configured master flat, using an in-session cache of a
        normalized flat (per-channel when a Bayer pattern is known).

        :param image: the image to process
        :type image: Image

        :return: the processed image or None if processing cannot proceed
        :rtype: Optional[Image]
        """

        if not image:
            return None

        do_divide = config.get_use_master_flat()

        _LOGGER.debug(f"Flat division enabled : {do_divide}")

        if do_divide:

            master_flat_path = config.get_master_flat_file_path()
            bayer_pattern = image.bayer_pattern

            if not bayer_pattern and image.is_color():
                MESSAGE_HUB.dispatch_warning(
                    __name__,
                    QT_TRANSLATE_NOOP("", "Unknown Bayer pattern. Falling back to global flat normalization."),
                    []
                )

            flat = get_cached_master_flat(master_flat_path, bayer_pattern)

            if flat is None:
                read_error_message = QT_TRANSLATE_NOOP(
                    "",
                    "Could not read master flat {}. Flat division is SKIPPED"
                )
                read_error_values = [master_flat_path, ]
                MESSAGE_HUB.dispatch_warning(__name__, read_error_message, read_error_values)
                return image

            if not image.is_same_shape_as(flat):
                mismatch_message = QT_TRANSLATE_NOOP(
                    "",
                    "Data structure inconsistency. Light: {} vs Master flat: {}. Flat division is SKIPPED"
                )
                mismatch_values = [image.data.shape, flat.data.shape]
                MESSAGE_HUB.dispatch_warning(__name__, mismatch_message, mismatch_values)
                return image

            _LOGGER.debug("Dividing by flat frame...")

            with Timer() as division_timer:

                light_data = image.data.astype(np.float32, copy=False)
                normalized_flat_data = flat.data.astype(np.float32, copy=False)
                image.data = np.uint16(np.clip(light_data / normalized_flat_data, 0, _16_BITS_MAX_VALUE))

            _LOGGER.debug(f"Flat frame divided in {division_timer.elapsed_in_milli_as_str} ms")

        return image

class ConvertForOutput(ImageProcessor):
    """
    Moves colors data to 3rd array axis for color images and reduce data range to unsigned 16 bits
    """
    @log
    def process_image(self, image: Image):

        if image.is_color():
            image.set_color_axis_as(2)

        image.data = np.uint16(np.clip(image.data, 0, 2 ** 16 - 1))

        return image


class HistogramComputer(ImageProcessor):
    """ Responsible of computing image histogram """

    _BIN_COUNT = 512

    @log
    def process_image(self, image: Image):
        DYNAMIC_DATA.histogram_container = compute_histograms_for_display(image, HistogramComputer._BIN_COUNT)
        return image


class QImageGenerator(ImageProcessor):
    """ Converts Numpy data to QPixmap """
    def process_image(self, image: Image):
        image_raw_data = image.data.copy()
        temp_image = array2qimage(image_raw_data, normalize=(2 ** 16 - 1))
        DYNAMIC_DATA.post_processor_result_qimage = QPixmap.fromImage(temp_image)

        return image


class QueueConsumer(QThread):
    """
    Abstract class for all our queue consumers.

    Responsible of grabbing images from a queue

    actual processing payload is to be implemented in the following abstract method : _handle_image().
    """

    busy_signal = pyqtSignal()
    """Qt signal to emit when an image has been retrieved and we are about to process it"""

    waiting_signal = pyqtSignal()
    """Qt signal to emit when image processing is complete"""

    @log
    def __init__(self, name: str, queue: SignalingQueue):
        QThread.__init__(self)
        self._name = name
        self._queue = queue
        self.setObjectName(name)

    def _name_current_thread_for_logging(self) -> None:
        """
        Names the Python thread used by logging for this worker.
        """
        threading.current_thread().name = self._name

    @abstractmethod
    @log
    def _handle_item(self, item_name: str):
        """
        Perform hopefully useful actions on an arbitrary string

        :param image: the image to handle
        :type image: Image
        """

    def run(self):
        """
        Starts polling the queue and perform processing units to each image.
        Receiving a None sentinel stops the consumer.

        If any processing error occurs, the current image is dropped
        """
        self._name_current_thread_for_logging()

        while True:
            item = self._queue.get()

            if item is None:
                MESSAGE_HUB.dispatch_info(__name__, QT_TRANSLATE_NOOP("", "{} stopped"), [self._name, ])
                break

            self.busy_signal.emit()

            with Timer() as timer:
                self._handle_item(item)

            _LOGGER.debug("End {} on {} in {} ms".format(
                self._name, item.origin if type(item) == Image else item, timer.elapsed_in_milli_as_str))

            self.waiting_signal.emit()


class ImageQueueConsumer(QueueConsumer):
    """
    Abstract class for all our queue consumers.

    Responsible of grabbing images from a queue

    actual processing payload is to be implemented in the following abstract method : _handle_image().
    """

    new_result_signal = pyqtSignal(Image)
    """Qt signal to emit when a new image has been processed"""

    @log
    def __init__(self, name: str, queue: SignalingQueue):
        QueueConsumer.__init__(self, name, queue)

    def _name_current_thread_for_logging(self) -> None:
        """
        Names the Python thread used by logging for this worker.
        """
        threading.current_thread().name = self._name

    @abstractmethod
    @log
    def _handle_item(self, image: Image):
        """
        Perform hopefully useful actions on image

        :param image: the image to handle
        :type image: Image
        """

    def run(self):
        """
        Starts polling the queue and perform processing units to each image.
        Receiving a None sentinel stops the consumer.

        If any processing error occurs, the current image is dropped
        """
        self._name_current_thread_for_logging()

        while True:
            item = self._queue.get()

            if item is None:
                MESSAGE_HUB.dispatch_info(__name__, QT_TRANSLATE_NOOP("", "{} stopped"), [self._name, ])
                break

            self.busy_signal.emit()
            MESSAGE_HUB.dispatch_info(
                __name__,
                QT_TRANSLATE_NOOP("", "Start {} on {}"),
                [self._name, item.origin if type(item) == Image else item]
            )

            with Timer() as timer:
                self._handle_item(item)

            MESSAGE_HUB.dispatch_info(
                __name__,
                QT_TRANSLATE_NOOP("", "End {} on {} in {} ms"),
                [self._name, item.origin if type(item) == Image else item, timer.elapsed_in_milli_as_str]
            )
            self.waiting_signal.emit()



class Pipeline(ImageQueueConsumer):
    """
    QueueConsumer specialization allowing to apply a list of image processors to each image
    """

    @log
    def __init__(self, name: str, queue: SignalingQueue, final_processes: list):
        QueueConsumer.__init__(self, name, queue)
        self._processes = []
        self._final_processes = final_processes

    @log
    def _handle_item(self, image: Image):

        try:
            for processor in self._processes + self._final_processes:
                image = processor.process_image(image)

            if image:
                self.new_result_signal.emit(image)

        except ProcessingError as processing_error:
            message = QT_TRANSLATE_NOOP("", "Error applying process '{}' to image {} : {} *** Image will be ignored")
            MESSAGE_HUB.dispatch_warning(__name__, message, [processor.__class__.__name__, image, processing_error])

    @log
    def add_process(self, process: ImageProcessor):
        """
        Add an image processor to the list of processes to run on images

        :param process: the processor to add
        :type process: ImageProcessor
        """
        self._processes.append(process)


class FileReader(QueueConsumer):
    """
    Handles image read from file
    """

    ZERO_FILE_SIZE_TIMEOUT = 2.0
    RAM_AVAILABILITY_TIMEOUT = 2.0

    image_read = pyqtSignal(Image)

    def __init__(self, queue: SignalingQueue):
        super().__init__("FileReader", queue)

    MEMORY_CODES_MAPPING = {

        0: 256 * 1024 ** 2,
        1: 512 * 1024 ** 2,
        2: 1024 ** 3,
        3: 2 * 1024 ** 3
    }

    def _handle_item(self, item: str):

        image_path = Path(item)

        _LOGGER.debug("loading image from %s", image_path)

        ram_to_preserve = FileReader.MEMORY_CODES_MAPPING[config.get_preserved_mem()]

        _LOGGER.debug(f"RAM amount to preserve: {human_readable_byte_size(ram_to_preserve)}")
        _LOGGER.debug(f" Available system memory : {human_readable_byte_size(available_memory())}")

        waited = False
        while available_memory() < ram_to_preserve:
            waited = True
            _LOGGER.info(f"RAM amount to preserve: {human_readable_byte_size(ram_to_preserve)} "
                         f"/ Available: {human_readable_byte_size(available_memory())}. Waiting...")

        time.sleep(FileReader.RAM_AVAILABILITY_TIMEOUT)

        _LOGGER.debug('RAM amount is OK. Reading new file...')

        if waited:
            MESSAGE_HUB.dispatch_info(__name__, self.tr("Done waiting for available RAM, now reading new file..."),)


        file_is_complete = False
        last_file_size = -1
        zero_size_since = None

        while not file_is_complete:
            size = QFileInfo(str(image_path)).size()
            _LOGGER.debug(f"File {image_path}'s size = {size}")

            if size == 0:
                if zero_size_since is None:
                    zero_size_since = time.monotonic()
                elif time.monotonic() - zero_size_since >= FileReader.ZERO_FILE_SIZE_TIMEOUT:

                    zero_size_error_message = (f"File {image_path} remained empty for "
                                               f"{FileReader.ZERO_FILE_SIZE_TIMEOUT} seconds. Abandoning wait")

                    MESSAGE_HUB.dispatch_error(
                        __name__,
                        zero_size_error_message)
                    return
            else:
                zero_size_since = None

            if size > 0 and size == last_file_size:
                file_is_complete = True
                _LOGGER.debug(f"File {image_path} is ready to be read")

            last_file_size = size

            if not file_is_complete:
                time.sleep(AVAILABLE_PROFILES[config.get_profile()].get_file_read_size_polling_period)

        image = read_disk_image(Path(image_path))

        if image is not None:
            image.ticket = str(image_path)
            self.image_read.emit(image)
