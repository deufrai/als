# SPDX-FileCopyrightText: 2019-2026 The ALS Authors
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Provides base application data
"""
from logging import getLogger
from typing import List, Optional

from PyQt5.QtCore import QObject

import als
from als.code_utilities import SignalingQueue, log, AlsLogAdapter
from als.model.base import Image, Session, STACKING_MODE_MEAN, STACKING_MODE_SUM, VisualProfile, PhotoProfile

_LOGGER = AlsLogAdapter(getLogger(__name__), {})

VERSION = als.__version__

WORKER_STATUS_IDLE = "-"

IMAGE_SAVE_TYPE_TIFF = "tiff"
IMAGE_SAVE_TYPE_PNG = "png"
IMAGE_SAVE_TYPE_JPEG = "jpg"

STACKED_IMAGE_FILE_NAME_BASE = "stack_image"
WEB_SERVED_IMAGE_FILE_NAME_BASE = "web_image"

WEB_SERVER_STATUS_STOPPED = "stopped"
WEB_SERVER_STATUS_STARTING = "starting"
WEB_SERVER_STATUS_RUNNING = "running"
WEB_SERVER_STATUS_STOPPING = "stopping"
WEB_SERVER_ACTIVE_STATUSES = (
    WEB_SERVER_STATUS_STARTING,
    WEB_SERVER_STATUS_RUNNING,
    WEB_SERVER_STATUS_STOPPING,
)

EAA_PROFILE_CODE = 0
PHOTO_PROFILE_CODE = 1

AVAILABLE_PROFILES = {

    EAA_PROFILE_CODE: VisualProfile(),
    PHOTO_PROFILE_CODE: PhotoProfile()
}


# pylint: disable=R0903
class I18n(QObject):
    """
    Holds global localized strings.

    All strings are initialized with dummy text and MUST be defined in setup()
    """

    STACKING_MODE_SUM_STR = "TEMP"
    STACKING_MODE_MEAN_STR = "TEMP"

    STACKING_MODES = {}

    SCANNER = "TEMP"
    OF = "TEMP"

    SCAN_FOLDER = "TEMP"
    WORK_FOLDER = "TEMP"
    WEB_FOLDER = "TEMP"

    PROFILE = "TEMP"
    VISUAL = "TEMP"
    PHOTO = "TEMP"

    STARTING = "TEMP"
    STOPPING = "TEMP"
    RUNNING_M = "TEMP"
    RUNNING_F = "TEMP"
    STOPPED_M = "TEMP"
    STOPPED_F = "TEMP"
    PAUSED = "TEMP"

    WEB_SERVER = "TEMP"
    ADDRESS = "TEMP"
    AUTO_RECOMMENDED = "TEMP"
    NETWORK_ADAPTER = "TEMP"

    TOOLTIP_BLACK_LEVEL = "TEMP"
    TOOLTIP_MIDTONES_LEVEL = "TEMP"
    TOOLTIP_WHITE_LEVEL = "TEMP"
    TOOLTIP_RED_LEVEL = "TEMP"
    TOOLTIP_GREEN_LEVEL = "TEMP"
    TOOLTIP_BLUE_LEVEL = "TEMP"
    TOOLTIP_SATURATION_LEVEL = "TEMP"
    TOOLTIP_STRETCH_STRENGTH = "TEMP"
    TOOLTIP_RGB_ACTIVE = "TEMP"
    TOOLTIP_STRETCH_ACTIVE = "TEMP"
    TOOLTIP_LEVELS_ACTIVE = "TEMP"

    STACK_SIZE = "TEMP"

    SESSION = "TEMP"

    def setup(self):
        """
        Sets real values for localized strings
        """
        I18n.STACKING_MODE_SUM_STR = self.tr("Sum")
        I18n.STACKING_MODE_MEAN_STR = self.tr("Mean")
        I18n.SCANNER = self.tr("scanner")
        I18n.OF = self.tr("of")
        I18n.PROFILE = self.tr("Profile")
        I18n.VISUAL = self.tr("Visual")
        I18n.PHOTO = self.tr("Photo")
        I18n.STARTING = self.tr("starting")
        I18n.STOPPING = self.tr("stopping")
        I18n.RUNNING_M = self.tr("running", "gender m")
        I18n.RUNNING_F = self.tr("running", "gender f")
        I18n.STOPPED_M = self.tr("stopped", "gender m")
        I18n.STOPPED_F = self.tr("stopped", "gender f")
        I18n.PAUSED = self.tr("paused")
        I18n.WEB_SERVER = self.tr("web server")
        I18n.ADDRESS = self.tr("address")
        I18n.AUTO_RECOMMENDED = self.tr("Auto - recommended")
        I18n.NETWORK_ADAPTER = self.tr("Network adapter")
        I18n.TOOLTIP_RED_LEVEL = self.tr("Red level")
        I18n.TOOLTIP_GREEN_LEVEL = self.tr("Green level")
        I18n.TOOLTIP_BLUE_LEVEL = self.tr("Blue level")
        I18n.TOOLTIP_SATURATION_LEVEL = self.tr("Color saturation")
        I18n.TOOLTIP_BLACK_LEVEL = self.tr("Black clipping")
        I18n.TOOLTIP_MIDTONES_LEVEL = self.tr("Midtones level")
        I18n.TOOLTIP_WHITE_LEVEL = self.tr("White clipping")
        I18n.TOOLTIP_STRETCH_STRENGTH = self.tr("Autostretch strength")
        I18n.TOOLTIP_RGB_ACTIVE = self.tr("RGB balance active")
        I18n.TOOLTIP_STRETCH_ACTIVE = self.tr("Autostretch active")
        I18n.TOOLTIP_LEVELS_ACTIVE = self.tr("Levels active")
        I18n.STACK_SIZE = self.tr("stack size")
        I18n.SESSION = self.tr("Session")
        I18n.SCAN_FOLDER = self.tr("scan folder")
        I18n.WORK_FOLDER = self.tr("work folder")
        I18n.WEB_FOLDER = self.tr("web folder")

        I18n.STACKING_MODES[STACKING_MODE_MEAN] = I18n.STACKING_MODE_MEAN_STR
        I18n.STACKING_MODES[STACKING_MODE_SUM] = I18n.STACKING_MODE_SUM_STR


# pylint: disable=R0902, R0903
class DynamicData:
    """
    Holds and maintain application dynamic data and notify observers on significant changes
    """
    def __init__(self):
        self.session = Session()
        self.web_server_status = WEB_SERVER_STATUS_STOPPED
        self.web_server_advertised_ip = ""
        self.web_server_advertised_url = ""
        self.web_server_address_candidates: List[object] = list()
        self.stack_size = 0
        self.post_processor_result = None
        self.histogram_container: HistogramContainer = None
        self.file_reader_queue = SignalingQueue()
        self.pre_process_queue = SignalingQueue()
        self.stacker_queue = SignalingQueue()
        self.process_queue = SignalingQueue()
        self.save_queue = SignalingQueue()
        self.file_reader_busy = False
        self.pre_processor_busy = False
        self.stacker_busy = False
        self.post_processor_busy = False
        self.saver_busy = False
        self.has_new_warnings = False
        self.is_first_run = True
        self.post_processor_result_qimage = None
        self.last_timing = 0
        self.total_exposure_time: int = 0
        self.master_dark: Optional[Image] = None
        self.master_flat: Optional[Image] = None
        self.current_sub_width = "n/a"
        self.current_sub_height = "n/a"
        self.current_sub_exposure_time = "n/a"
        self.current_sub_is_color = False
        self.current_sub_bayer_pattern = ""

    @log
    def clear_master_calibration_cache(self) -> None:
        """
        Clears cached master calibration frames for the running session.
        """
        self.master_dark = None
        self.master_flat = None


DYNAMIC_DATA = DynamicData()
