"""
Everything we need to perform outputs from ALS

For now, we only save some images to disk, but who knows...
"""
import os
import sys
from logging import getLogger
from pathlib import Path

import cv2
from PyQt5.QtCore import QT_TRANSLATE_NOOP

import als.model.data
from als import config
from als.code_utilities import log, SignalingQueue, AlsLogAdapter
from als.messaging import MESSAGE_HUB
from als.model.base import Image
from als.processing import QueueConsumer

_LOGGER = AlsLogAdapter(getLogger(__name__), {})


class ImageSaver(QueueConsumer):
    """
    Saves images according to commands posted to IMAGE_SAVE_QUEUE in its own thread

    """
    @log
    def __init__(self, save_queue: SignalingQueue, controller):
        QueueConsumer.__init__(self, "save", save_queue)
        self._controller = controller

    @log
    def _handle_item(self, image: Image):

        # image conversions involved in saving to various formats forces us to clone the received image
        ImageSaver._save_image(image.clone())

        # if we just saved an image for the server output, have the controller notify the browsers
        if image.destination.strip().startswith(config.get_web_folder_path()):
            self._controller.notify_browsers_about_new_image()

    @staticmethod
    @log
    def _save_image(image):
        """
        Saves image to disk

        :param image: the image to save
        :type image: Image
        """
        target_path = str(Path(image.destination).parent / f"ALZ{Path(image.destination).name}")
        cwd = os.getcwd()

        if sys.platform == 'win32':
            os.chdir(Path(target_path).parent)
            target_path = Path(target_path).name

        if image.destination.endswith('.' + als.model.data.IMAGE_SAVE_TYPE_TIFF):
            pre_save_is_successful, failure_details = ImageSaver._save_image_as_tiff(image, target_path)

        elif image.destination.endswith('.' + als.model.data.IMAGE_SAVE_TYPE_PNG):
            pre_save_is_successful, failure_details = ImageSaver._save_image_as_png(image, target_path)

        elif image.destination.endswith('.' + als.model.data.IMAGE_SAVE_TYPE_JPEG):
            pre_save_is_successful, failure_details = ImageSaver._save_image_as_jpg(image, target_path)

        else:
            # Unsupported format in config file. Should never happen
            pre_save_is_successful, failure_details = False, f"Unsupported File format for {image.destination}"

        post_save_is_successful = False

        if pre_save_is_successful:

            actual_destination = str(Path(image.destination))

            failure_details = ""
            try:

                if sys.platform == 'win32' and Path(actual_destination).exists():
                    os.remove(actual_destination)

                os.rename(target_path, actual_destination)
                post_save_is_successful = True

            except OSError:
                try:
                    os.remove(target_path)
                except OSError:
                    pass

        if post_save_is_successful:

            MESSAGE_HUB.dispatch_info(
                __name__,
                QT_TRANSLATE_NOOP("", "Image saved : {}"),
                [image.destination]
            )

        else:
            details = image.destination

            if failure_details.strip():
                details += ' : ' + failure_details

            MESSAGE_HUB.dispatch_error(__name__, QT_TRANSLATE_NOOP("", "Failed to save image : {}"), [details, ])

        if sys.platform == 'win32':
            os.chdir(cwd)

    @staticmethod
    @log
    def _save_image_as_tiff(image: Image, target_path: str):
        """
        Saves image as tiff.

        :param image: the image to save
        :type image: Image

        :param target_path: the absolute path of the image file to save to
        :type target_path: str

        :return: a tuple with 2 values :

          - True if save succeeded, False otherwise
          - Details on cause of save failure, if occurs

        As we are using cv2.imwrite, we won't get any details on failures. So failure details will always
        be the empty string.
        """
        cv2_color_conversion_flag = cv2.COLOR_RGB2BGR if image.is_color() else cv2.COLOR_GRAY2BGR
        return cv2.imwrite(target_path, cv2.cvtColor(image.data, cv2_color_conversion_flag)), ""

    @staticmethod
    @log
    def _save_image_as_png(image: Image, target_path: str):
        """
        Saves image as png.

        :param image: the image to save
        :type image: Image

        :param target_path: the absolute path of the image file to save to
        :type target_path: str

        :return: a tuple with 2 values :

          - True if save succeeded, False otherwise
          - Details on cause of save failure, if occurs

        As we are using cv2.imwrite, we won't get any details on failures. So failure details will always
        be the empty string.
        """
        cv2_color_conversion_flag = cv2.COLOR_RGB2BGR if image.is_color() else cv2.COLOR_GRAY2BGR
        return cv2.imwrite(target_path,
                           cv2.cvtColor(image.data, cv2_color_conversion_flag),
                           [cv2.IMWRITE_PNG_COMPRESSION, 9]), ""

    @staticmethod
    @log
    def _save_image_as_jpg(image: Image, target_path: str):
        """
        Saves image as jpg.

        :param image: the image to save
        :type image: Image

        :param target_path: the absolute path of the image file to save to
        :type target_path: str

        :return: a tuple with 2 values :

          - True if save succeeded, False otherwise
          - Details on cause of save failure, if occurs

        As we are using cv2.imwrite, we won't get any details on failures. So failure details will always
        be the empty string.
        """
        # here we are sure that image data type is unsigned 16 bits. We need to downscale to 8 bits
        image.data = (image.data / (((2 ** 16) - 1) / ((2 ** 8) - 1))).astype('uint8')
        cv2_color_conversion_flag = cv2.COLOR_RGB2BGR if image.is_color() else cv2.COLOR_GRAY2BGR

        return cv2.imwrite(target_path,
                           cv2.cvtColor(image.data, cv2_color_conversion_flag),
                           [int(cv2.IMWRITE_JPEG_QUALITY), 85]), ''
