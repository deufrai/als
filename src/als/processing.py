"""
Provides all means of image processing
"""
import logging
import time
from abc import abstractmethod
from pathlib import Path
from typing import List

import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal, QT_TRANSLATE_NOOP
from PyQt5.QtGui import QPixmap
from qimage2ndarray import array2qimage
from scipy.signal import convolve2d

from als import config
from als.code_utilities import log, Timer, SignalingQueue, human_readable_byte_size, available_memory
from als.crunching import get_image_memory_size, compute_histograms_for_display
from als.io import input as als_input
from als.io.input import read_disk_image
from als.messaging import MESSAGE_HUB
from als.model.base import Image
from als.model.data import I18n, DYNAMIC_DATA
from als.model.params import ProcessingParameter, RangeParameter, SwitchParameter
from contrib.stretch import Stretch

_LOGGER = logging.getLogger(__name__)

_16_BITS_MAX_VALUE = 2**16 - 1
_HOT_PIXEL_RATIO = 2


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

            if processed:
                image.data = np.clip(image.data, 0, _16_BITS_MAX_VALUE)

        return image


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

            # final interpolation
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


class FileReader(ImageProcessor):
    """
    Handles image read from file
    """

    # //FIXME : BEWARE, in this specific processor, what we actually process is file paths, not image objects
    def process_image(self, image: Image):
        image_path = image

        # TODO: Move this logic to Controller somehow
        #       Checking if available memory is twice as big as what an image requires
        #       twice because we preallocate a copy when aligning...
        reference_image = DYNAMIC_DATA.post_processor_result
        needed_memory_in_bytes = get_image_memory_size(reference_image) * 2 if reference_image else 0
        _LOGGER.debug(f"Needed memory for next image: {human_readable_byte_size(needed_memory_in_bytes)}")
        _LOGGER.debug(f"Available system memory : {human_readable_byte_size(available_memory())}")
        while available_memory() < needed_memory_in_bytes:
            _LOGGER.warning(f"Memory low ! Needed memory: {human_readable_byte_size(needed_memory_in_bytes)} "
                            f"/ Available: {human_readable_byte_size(available_memory())} Waiting...")
            time.sleep(1)

        image = read_disk_image(Path(image_path))
        if image:
            image.ticket = image_path
        return image


class HotPixelRemover(ImageProcessor):
    """Provides hot pixels removal"""

    @staticmethod
    def _neighbors_average(data):
        """
        returns an array containing the means of all original array's pixels' neighbors
        :param data: the image to compute means for
        :return: an array containing the means of all original array's pixels' neighbors
        :rtype: np.Array
        """

        kernel = np.ones((3, 3))
        kernel[1, 1] = 0

        neighbor_sum = convolve2d(data, kernel, mode='same', boundary='fill', fillvalue=0)
        num_neighbor = convolve2d(np.ones(data.shape), kernel, mode='same', boundary='fill', fillvalue=0)

        return (neighbor_sum / num_neighbor).astype(data.dtype)

    @log
    def process_image(self, image: Image):

        # the idea is to check every pixel value against its 8 neighbors
        # if its value is more than _HOT_RATIO times the mean of its neighbors' values
        # me replace its value with that mean

        # this can only work on B&W or non-debayered color images

        if not image:
            return None

        hpr_on = config.get_hot_pixel_remover()

        _LOGGER.debug(f"Hot pixel remover enabled : {hpr_on}")

        if hpr_on:

            if not image.is_color():
                means = HotPixelRemover._neighbors_average(image.data)
                image.data = np.where(image.data / means > _HOT_PIXEL_RATIO, means, image.data)
            else:
                MESSAGE_HUB.dispatch_warning(
                    __name__,
                    QT_TRANSLATE_NOOP("", "Hot Pixel Remover cannot work on debayered color images.")
                )

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
    def process_image(self, image: Image):

        if not image:
            return None

        do_subtract = config.get_use_master_dark()

        _LOGGER.debug(f"Dark subtraction enabled : {do_subtract}")

        if do_subtract:

            dark = als_input.read_disk_image(Path(config.get_master_dark_file_path()))

            if dark is None:
                read_error_message = QT_TRANSLATE_NOOP(
                    "",
                    "Could not read dark {}. Dark subtraction is SKIPPED"
                )
                read_error_values = [config.get_master_dark_file_path(), ]
                MESSAGE_HUB.dispatch_warning(__name__, read_error_message, read_error_values)
                return image

            if not image.is_same_shape_as(dark):
                mismatch_message = QT_TRANSLATE_NOOP(
                    "",
                    "Data structure inconsistency. Light: {} vs Dark: {}. Dark subtraction is SKIPPED"
                )
                mismatch_values = [image.data.shape, dark.data.shape]
                MESSAGE_HUB.dispatch_warning(__name__, mismatch_message, mismatch_values)
                return image

            if image.data.dtype.name != dark.data.dtype.name:

                MESSAGE_HUB.dispatch_info(
                    __name__,
                    QT_TRANSLATE_NOOP(
                        "",
                        "Dark & Light data types mismatch. Light: {} vs Dark: {}. Dark needs to be conformed."
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

                    dark.data = np.interp(
                        dark.data,
                        (dark_min_allowed, dark_max_allowed),
                        (image_min_allowed, image_max_allowed)).astype(image.data.dtype)

                _LOGGER.debug(f"Dark frame conforming done in {conforming_timer.elapsed_in_milli_as_str} ms")

            _LOGGER.debug("Subtracting dark frame...")

            with Timer() as subtraction_timer:
                image.data = np.where(image.data > dark.data, image.data - dark.data, 0)
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


class ConvertForOutput(ImageProcessor):
    """
    Moves colors data to 3rd array axis for color images and reduce data range to unsigned 16 bits
    """
    @log
    def process_image(self, image: Image):

        # make sure  that our changes are made on a copy of the received image.
        # So whoever kept a ref to it won't be affected
        image = image.clone()

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

    new_result_signal = pyqtSignal(Image)
    """Qt signal to emit when a new image has been processed"""

    busy_signal = pyqtSignal()
    """Qt signal to emit when an image has been retrieved and we are about to process it"""

    waiting_signal = pyqtSignal()
    """Qt signal to emit when image processing is complete"""

    @log
    def __init__(self, name: str, queue: SignalingQueue):
        QThread.__init__(self)
        self._stop_asked = False
        self._name = name
        self._queue = queue

    @abstractmethod
    @log
    def _handle_item(self, image: Image):
        """
        Perform hopefully useful actions on image

        :param image: the image to handle
        :type image: Image
        """

    @log
    def run(self):
        """
        Starts polling the queue and perform processing units to each image

        If any processing error occurs, the current image is dropped
        """
        while not self._stop_asked:

            if self._queue.qsize() > 0:

                self.busy_signal.emit()
                item = self._queue.get()
                MESSAGE_HUB.dispatch_info(__name__,
                                          QT_TRANSLATE_NOOP("", "Start {} on {}"),
                                          [self._name, item.origin if type(item) == Image else item])

                with Timer() as timer:
                    self._handle_item(item)

                MESSAGE_HUB.dispatch_info(
                    __name__,
                    QT_TRANSLATE_NOOP("", "End {} on {} in {} ms"),
                    [self._name, item.origin if type(item) == Image else item, timer.elapsed_in_milli_as_str])
                self.waiting_signal.emit()

            self.msleep(20)

    @log
    def stop(self):
        """
        Sets flag that will interrupt the main loop in run()
        """
        self._stop_asked = True
        MESSAGE_HUB.dispatch_info(__name__, QT_TRANSLATE_NOOP("", "{} stopped"), [self._name, ])


class Pipeline(QueueConsumer):
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
