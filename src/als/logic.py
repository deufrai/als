# !/usr/bin/python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2019-2026 The ALS Authors
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Module holding all application logic
"""
import datetime
import json
import time
from concurrent.futures import Future
from logging import getLogger
from pathlib import Path
from threading import Thread
from typing import List

from PyQt5.QtCore import QFile, QT_TRANSLATE_NOOP, QCoreApplication, QThread, QTimer

from als import config
from als.code_utilities import log, AlsException, SignalingQueue, get_timestamp, \
    available_memory, AlsLogAdapter
from als.messaging import MESSAGE_HUB
from als.model.base import Image, Session, STACKING_MODE_MEAN, STACKING_MODE_SUM, RunningProfile
from als.model.data import (
    DYNAMIC_DATA,
    I18n, STACKED_IMAGE_FILE_NAME_BASE,
    IMAGE_SAVE_TYPE_JPEG, WEB_SERVED_IMAGE_FILE_NAME_BASE,
    WEB_SERVER_ACTIVE_STATUSES, WEB_SERVER_STATUS_RUNNING, WEB_SERVER_STATUS_STARTING,
    WEB_SERVER_STATUS_STOPPED, WEB_SERVER_STATUS_STOPPING, AVAILABLE_PROFILES
)
from als.model.params import ProcessingParameter
from als.processing import FileReader, Pipeline, Debayer, Standardize, ConvertForOutput, Levels, ColorBalance, \
    AutoStretch, \
    HotPixelRemover, RemoveDark, HistogramComputer, QImageGenerator, RemoveFlat, QueueConsumer
from als.stack import Stacker
from als.streams.input import InputScanner, ScannerStartError
from als.streams.network import (
    Server, WEB_SERVER_BIND_HOST, get_network_address_candidates, NetworkAddress,
    select_advertised_address
)
from als.streams.output import ImageSaver

_LOGGER = AlsLogAdapter(getLogger(__name__), {})


class SessionError(AlsException):
    """
    Class for all errors related to session management
    """


class FolderSetupError(SessionError):
    """Raised when a critical folder is missing"""


class PortInUseError(RuntimeError):
    """Raised when web server cannot start because port is already in use"""


# pylint: disable=R0902, R0904
class Controller:
    """
    The application controller, in charge of implementing application logic
    """

    @log
    def __init__(self):

        DYNAMIC_DATA.session.set_status(Session.stopped)
        DYNAMIC_DATA.web_server_status = WEB_SERVER_STATUS_STOPPED
        DYNAMIC_DATA.file_reader_busy = False
        DYNAMIC_DATA.pre_processor_busy = False
        DYNAMIC_DATA.stacker_busy = False
        DYNAMIC_DATA.post_processor_busy = False
        DYNAMIC_DATA.saver_busy = False
        DYNAMIC_DATA.last_timing = 0

        self._input_scanner: InputScanner = InputScanner.create_scanner()
        self._save_every_image = False

        current_profile: RunningProfile = AVAILABLE_PROFILES[config.get_profile()]

        self._file_reader_queue: SignalingQueue = DYNAMIC_DATA.file_reader_queue
        self._fileReader = FileReader(self._file_reader_queue)
        self._fileReader.start(current_profile.get_pre_process_priority)
        self._input_scanner.new_image_path_signal[str].connect(self.on_new_image_path)

        self._pre_process_queue: SignalingQueue = DYNAMIC_DATA.pre_process_queue
        self._pre_process_pipeline: Pipeline = Pipeline(
            'pre-process',
            self._pre_process_queue,
            [HotPixelRemover(), RemoveDark(), RemoveFlat(), Debayer(), Standardize()])
        self._pre_process_pipeline.start(current_profile.get_pre_process_priority)

        self._stacker_queue: SignalingQueue = DYNAMIC_DATA.stacker_queue
        self._stacker: Stacker = Stacker(self._stacker_queue)
        self._stacker.align_before_stack = True
        self._stacker.start(current_profile.get_stacking_priority)

        self._post_process_queue = DYNAMIC_DATA.process_queue
        self._post_process_pipeline: Pipeline = Pipeline(
            'post-process',
            self._post_process_queue,
            [ConvertForOutput(), HistogramComputer(), QImageGenerator()])
        self._rgb_processor = ColorBalance()
        self._autostretch_processor = AutoStretch()
        self._levels_processor = Levels()
        self._post_process_pipeline.add_process(self._autostretch_processor)
        self._post_process_pipeline.add_process(self._levels_processor)
        self._post_process_pipeline.add_process(self._rgb_processor)
        self._post_process_pipeline.start(current_profile.get_post_process_priority)

        self._saver_queue = DYNAMIC_DATA.save_queue
        self._saver = ImageSaver(self._saver_queue, self)
        self._saver.start(QThread.LowPriority)

        self._last_stacking_result = None

        self._web_server = Server(config.get_web_folder_path())
        self._server_thread = None

        self._model_observers = list()
        self._web_server_observers = list()
        self._subs_processing_start_times = dict()

        self._fileReader.image_read[Image].connect(self.on_new_image)
        self._pre_process_pipeline.new_result_signal[Image].connect(self.on_new_pre_processed_image)
        self._stacker.stack_size_changed_signal[int].connect(self.on_stack_size_changed)
        self._stacker.new_result_signal[Image].connect(self.on_new_stack_result)
        self._post_process_pipeline.new_result_signal[Image].connect(self.on_new_post_processor_result)

        self._file_reader_queue.size_changed_signal[int].connect(self.on_file_reader_queue_size_changed)
        self._pre_process_queue.size_changed_signal[int].connect(self.on_pre_process_queue_size_changed)
        self._stacker_queue.size_changed_signal[int].connect(self.on_stacker_queue_size_changed)
        self._post_process_queue.size_changed_signal[int].connect(self.on_post_processor_queue_size_changed)
        self._saver_queue.size_changed_signal[int].connect(self.on_saver_queue_size_changed)

        self._fileReader.busy_signal.connect(self.on_file_reader_busy)
        self._fileReader.waiting_signal.connect(self.on_file_reader_waiting)
        self._pre_process_pipeline.busy_signal.connect(self.on_pre_processor_busy)
        self._pre_process_pipeline.waiting_signal.connect(self.on_pre_processor_waiting)
        self._stacker.busy_signal.connect(self.on_stacker_busy)
        self._stacker.waiting_signal.connect(self.on_stacker_waiting)
        self._post_process_pipeline.busy_signal.connect(self.on_post_processor_busy)
        self._post_process_pipeline.waiting_signal.connect(self.on_post_processor_waiting)
        self._saver.busy_signal.connect(self.on_saver_busy)
        self._saver.waiting_signal.connect(self.on_saver_waiting)
        self._saver.save_completed_signal[str].connect(self.on_image_saved)

        DYNAMIC_DATA.session.status_changed_signal.connect(self._notify_model_observers)
        self._web_server.startup_failed_signal.connect(self.on_web_server_start_failed)
        self._web_server.startup_succeeded_signal.connect(self.on_web_server_started)
        self._web_server.stopped_signal.connect(self.on_web_server_stopped)

        self._metrics_timer = QTimer()
        self._metrics_timer.setInterval(2000)
        self._metrics_timer.timeout.connect(self.collect_metrics)
        self._metrics_timer.start()

        self._reset_current_sub_infos()

    @log
    def collect_metrics(self):
        _LOGGER.debug(f"*SM-MEM* Available memory (byte): {available_memory()}")

    @log
    def get_autostretch_parameters(self) -> List[ProcessingParameter]:
        """
        Retrieves autostretch parameters

        :return: autostretch parameters
        """
        return self._autostretch_processor.get_parameters()

    @log
    def get_rgb_parameters(self) -> List[ProcessingParameter]:
        """
        Retrieves rgb parameters

        :return: rgb parameters
        """
        return self._rgb_processor.get_parameters()

    @log
    def get_levels_parameters(self) -> List[ProcessingParameter]:
        """
        Retrieves Levels processor parameters

        :return: Levels processor parameters
        """
        return self._levels_processor.get_parameters()

    @log
    def remove_model_observer(self, observer):
        """
        Removes observer from our observers list.

        :param observer: the observer to remove
        :type observer: any
        """
        if observer in self._model_observers:
            self._model_observers.remove(observer)

    @log
    def add_web_server_observer(self, observer):
        """
        Adds an observer for web server lifecycle events.

        :param observer: the new observer
        :type observer: any
        """
        self._web_server_observers.append(observer)

    @log
    def remove_web_server_observer(self, observer):
        """
        Removes an observer for web server lifecycle events.

        :param observer: the observer to remove
        :type observer: any
        """
        if observer in self._web_server_observers:
            self._web_server_observers.remove(observer)

    @log
    def _notify_model_observers(self, image_only=False):
        """
        Tells all registered observers to update their display
        """
        for observer in self._model_observers:
            observer.update_display(image_only)

    @log
    def add_model_observer(self, observer):
        """
        Adds an observer to our observers list.

        :param observer: the new observer
        :type observer: any
        """
        self._model_observers.append(observer)

    @log
    def apply_processing(self):
        """
        Apply processing on last stacking result
        """
        if self._stacker.size > 0 and DYNAMIC_DATA.process_queue.qsize() == 0:

            # don't consider this new processing result for image timing
            image_to_process = self._last_stacking_result.clone(keep_ref_to_data=True)
            image_to_process.ticket = "ALZ"
            DYNAMIC_DATA.process_queue.put(image_to_process)

    @log
    def get_save_every_image(self) -> bool:
        """
        Retrieves the flag that tells if we need to save every process result image

        :return: the flag that tells if we need to save every process result image
        :rtype: bool
        """
        return self._save_every_image

    @log
    def set_save_every_image(self, save_every_image: bool):
        """
        Sets the flag that tells if we need to save every process result image

        :param save_every_image: flag that tells if we need to save every process result image
        :type save_every_image: bool
        """
        self._save_every_image = save_every_image

    @log
    def get_align_before_stack(self) -> bool:
        """
        Gets "align before stack" switch

        :return: Do we align before stacking ?
        :rtype: bool
        """
        return self._stacker.align_before_stack

    @log
    def set_align_before_stack(self, align: bool):
        """
        Sets "align before stack" switch

        :param align: Do we align before stacking ?
        :type align: bool
        """
        self._stacker.align_before_stack = align

    @log
    def is_stacking_mode_mean(self):
        """
        Is stacker set to mean stacking mode

        :return: the truth
        :rtype: bool
        """
        pass
        return self._stacker.stacking_mode == STACKING_MODE_MEAN


    @log
    def is_stacking_mode_sum(self):
        """
        Is stacker set to sum stacking mode

        :return: the truth
        :rtype: bool
        """
        return self._stacker.stacking_mode == STACKING_MODE_SUM

    @log
    def set_stacking_mode_mean(self):
        """
        Sets current stacking mode to mean
        """
        self._stacker.stacking_mode = STACKING_MODE_MEAN


    @log
    def set_stacking_mode_sum(self):
        """
        Sets current stacking mode to mean
        """
        self._stacker.stacking_mode = STACKING_MODE_SUM

    @log
    def set_new_profile(self, profile_code):
        new_profile = AVAILABLE_PROFILES[profile_code]
        DYNAMIC_DATA.current_profile = new_profile

        self._fileReader.setPriority(new_profile.get_pre_process_priority)
        self._pre_process_pipeline.setPriority(new_profile.get_pre_process_priority)
        self._stacker.setPriority(new_profile.get_stacking_priority)
        self._post_process_pipeline.setPriority(new_profile.get_post_process_priority)


    @log
    def on_stack_size_changed(self, size):
        """
        Stack size just changed

        :param size: the stack size
        :type size: int
        """
        DYNAMIC_DATA.stack_size = size
        self._notify_model_observers()

    @log
    def on_new_post_processor_result(self, image: Image):
        """
        A new image processing result is here

        :param image: the new processing result
        :type image: Image
        """

        processing_start_time = self._subs_processing_start_times.pop(image.ticket, None)
        if processing_start_time is not None:
            delta = round(time.time() - processing_start_time, 3)

            _LOGGER.debug(f"*SD-FRMTIME* Total frame processing time: {delta}")
            message = QT_TRANSLATE_NOOP("", "* Full processing time for '{}' : {} s")
            DYNAMIC_DATA.last_timing = delta
            MESSAGE_HUB.dispatch_info(__name__, message, [image.ticket, delta])

        image.origin = "Process result"
        DYNAMIC_DATA.post_processor_result = image
        self._notify_model_observers(image_only=True)
        self.write_stack_info_json()
        self.save_post_process_result()

    @log
    def on_new_stack_result(self, image: Image):
        """
        A new image has been stacked

        :param image: the result of the stack
        :type image: Image
        """
        image.origin = "Stacking result"
        self._last_stacking_result = image

        if image.exposure_time != Image.UNDEF_EXP_TIME:
            DYNAMIC_DATA.total_exposure_time += image.exposure_time

        self.purge_queue(self._post_process_queue)
        self._post_process_queue.put(image)

    @log
    def on_new_image_path(self, image_path: str):
        """
        A new image as been detected by input scanner

        :param image_path: the path of the image to read
        :type image_path: str
        """
        self._subs_processing_start_times[image_path] = time.time()
        self._file_reader_queue.put(image_path)

    @log
    def on_new_image(self, image: Image):
        """
        A new image as been read from disk

        :param image: the new image
        :type image: Image
        """
        DYNAMIC_DATA.current_sub_width = image.width
        DYNAMIC_DATA.current_sub_height = image.height
        DYNAMIC_DATA.current_sub_exposure_time = image.exposure_time

        DYNAMIC_DATA.current_sub_is_color = image.is_color() or image.bayer_pattern != ""

        DYNAMIC_DATA.current_sub_bayer_pattern = image.bayer_pattern
        self._pre_process_queue.put(image)

    @log
    def on_new_pre_processed_image(self, image: Image):
        """
        A new image as been pre-processed

        :param image: the image
        :type image: Image
        """
        self._stacker_queue.put(image)

    @log
    def on_file_reader_queue_size_changed(self, new_size):
        """
        Qt slot executed when an item has just been pushed to the file reader queue

        :param new_size: new queue size
        :type new_size: int
        """
        _LOGGER.debug(f"*SD-Q-READ* New file reader queue size: {new_size}")
        self._notify_model_observers()

    @log
    def on_pre_process_queue_size_changed(self, new_size):
        """
        Qt slot executed when an item has just been pushed to the pre-processor queue

        :param new_size: new queue size
        :type new_size: int
        """
        _LOGGER.debug(f"*SD-Q-PRE* New pre-processor queue size: {new_size}")
        self._notify_model_observers()

    @log
    def on_stacker_queue_size_changed(self, new_size):
        """
        Qt slot executed when an item has just been pushed to the stacker queue

        :param new_size: new queue size
        :type new_size: int
        """
        _LOGGER.debug(f"*SD-Q-STA* New stacker queue size : {new_size}")
        self._notify_model_observers()

    @log
    def on_post_processor_queue_size_changed(self, new_size):
        """
        Qt slot executed when an item has just been pushed to the process queue

        :param new_size: new queue size
        :type new_size: int
        """
        _LOGGER.debug(f"*SD-Q-POST* New post-processor queue size: {new_size}")
        self._notify_model_observers()

    @log
    def on_saver_queue_size_changed(self, new_size):
        """
        Qt slot executed when an item has just been pushed to the save queue

        :param new_size: new queue size
        :type new_size: int
        """
        _LOGGER.debug(f"*SD-Q-SAV* New saver queue size : {new_size}")
        self._notify_model_observers()

    @log
    def on_file_reader_busy(self):
        """
        pre-processor just started working on new image
        """
        DYNAMIC_DATA.file_reader_busy = True
        self._notify_model_observers()

    @log
    def on_file_reader_waiting(self):
        """
        pre-processor just finished working on new image
        """
        DYNAMIC_DATA.file_reader_busy = False
        self._notify_model_observers()

    @log
    def on_pre_processor_busy(self):
        """
        pre-processor just started working on new image
        """
        DYNAMIC_DATA.pre_processor_busy = True
        self._notify_model_observers()

    @log
    def on_pre_processor_waiting(self):
        """
        pre-processor just finished working on new image
        """
        DYNAMIC_DATA.pre_processor_busy = False
        self._notify_model_observers()

    @log
    def on_stacker_busy(self):
        """
        stacker just started working on new image
        """
        DYNAMIC_DATA.stacker_busy = True
        self._notify_model_observers()

    @log
    def on_stacker_waiting(self):
        """
        stacker just finished working on new image
        """
        DYNAMIC_DATA.stacker_busy = False
        self._notify_model_observers()

    @log
    def on_post_processor_busy(self):
        """
        post-processor just started working on new image
        """
        DYNAMIC_DATA.post_processor_busy = True
        self._notify_model_observers()

    @log
    def on_post_processor_waiting(self):
        """
        post-processor just finished working on new image
        """
        DYNAMIC_DATA.post_processor_busy = False
        self._notify_model_observers()

    @log
    def on_saver_busy(self):
        """
        saver just started working on new image
        """
        DYNAMIC_DATA.saver_busy = True
        self._notify_model_observers()

    @log
    def on_saver_waiting(self):
        """
        saver just finished working on new image
        """
        DYNAMIC_DATA.saver_busy = False
        self._notify_model_observers()

    @log
    def on_image_saved(self, destination: str):
        """
        Reacts to a successful image save.

        Notifies browsers only when the dedicated web image has been written.

        :param destination: absolute destination path of the saved image
        :type destination: str
        """
        destination_path = Path(destination).resolve()
        if destination_path.stem == WEB_SERVED_IMAGE_FILE_NAME_BASE:
            self.notify_browsers_about_new_image()

    @log
    def start_session(self):
        """
        Starts session
        """
        try:
            if DYNAMIC_DATA.session.is_stopped:

                DYNAMIC_DATA.session.set_status(Session.starting)

                MESSAGE_HUB.dispatch_info(__name__, QT_TRANSLATE_NOOP("", "Starting new session..."))

                DYNAMIC_DATA.has_new_warnings = False
                self._stacker.reset()
                self._subs_processing_start_times.clear()
                self._reset_current_sub_infos()
                DYNAMIC_DATA.last_timing = 0
                DYNAMIC_DATA.total_exposure_time = 0
                DYNAMIC_DATA.clear_master_calibration_cache()

                scan_folder_path = config.get_scan_folder_path()
                work_folder_path = config.get_work_folder_path()
                web_folder_path = config.get_web_folder_path()

                # checking presence of critical folders
                critical_folders_dict = {
                    I18n.SCAN_FOLDER: scan_folder_path,
                    I18n.WORK_FOLDER: work_folder_path,
                    I18n.WEB_FOLDER:  web_folder_path,
                }

                for role, path in critical_folders_dict.items():
                    if not path or not Path(path).is_dir():
                        title = QT_TRANSLATE_NOOP("", "Missing {}")
                        message = QT_TRANSLATE_NOOP("", "Your {} does not exist :\n{}")
                        raise FolderSetupError(
                            QCoreApplication.translate("", title).format(role),
                            QCoreApplication.translate("", message).format(*[role, path]))

                    if path is not scan_folder_path:
                        if Path(scan_folder_path) in Path(path).parents or Path(path) == Path(scan_folder_path):
                            title = QT_TRANSLATE_NOOP("", "Misplaced {}")
                            message = QT_TRANSLATE_NOOP("", "Your {} :\n{}\n\nmust not be the same as or a subfolder of your {} :\n{}")
                            raise FolderSetupError(
                                QCoreApplication.translate("", title).format(role),
                                QCoreApplication.translate("", message).format(*[role, path, I18n.SCAN_FOLDER, scan_folder_path])
                            )

                MESSAGE_HUB.dispatch_info(
                    __name__,
                    QT_TRANSLATE_NOOP("", "Session started : alignment {}, stacking mode {} and {} profile"),
                    [self._stacker.align_before_stack, I18n.STACKING_MODES[self._stacker.stacking_mode], DYNAMIC_DATA.current_profile])

                # setup web content
                try:
                    Controller._setup_web_waiting_image()
                    self.write_stack_info_json()
                except OSError as os_error:
                    raise SessionError("Web folder could not be prepared", str(os_error))

                self.notify_browsers_about_new_image()

            else:
                # session was paused when this start was ordered. No need for checks & setup
                MESSAGE_HUB.dispatch_info(__name__, QT_TRANSLATE_NOOP("", "Resuming session ..."))

            # start input scanner
            try:
                self._input_scanner.start()
                MESSAGE_HUB.dispatch_info(__name__, QT_TRANSLATE_NOOP("", "Input scanner started"))
                DYNAMIC_DATA.session.set_status(Session.running)

            except ScannerStartError as scanner_start_error:
                raise SessionError("Input scanner could not start", scanner_start_error)

        except SessionError as session_error:
            MESSAGE_HUB.dispatch_error(__name__,
                                       QT_TRANSLATE_NOOP("", "Session start error: {}"),
                                       [session_error.message])
            raise

    @log
    def stop_session(self):
        """
        Stops session : stop input scanner and purge input queue
        """
        if not DYNAMIC_DATA.session.is_stopped:
            self._subs_processing_start_times.clear()
            DYNAMIC_DATA.session.set_status(Session.stopped)
            self._stop_input_scanner()
            Controller.purge_queue(self._file_reader_queue)
            Controller.purge_queue(self._pre_process_queue)
            Controller.purge_queue(self._stacker_queue)
            Controller.purge_queue(self._post_process_queue)
            MESSAGE_HUB.dispatch_info(__name__, QT_TRANSLATE_NOOP("", "Session stopped"))

    @log
    def pause_session(self):
        """
        Pauses session : just stop input scanner
        """
        if DYNAMIC_DATA.session.is_running:
            self._stop_input_scanner()
        MESSAGE_HUB.dispatch_info(__name__, QT_TRANSLATE_NOOP("", "Session paused"))
        DYNAMIC_DATA.session.set_status(Session.paused)

    @log
    def start_www(self):
        """Starts web server"""

        if DYNAMIC_DATA.web_server_status in WEB_SERVER_ACTIVE_STATUSES:
            return

        DYNAMIC_DATA.web_server_status = WEB_SERVER_STATUS_STARTING
        self._notify_model_observers()

        port_number = config.get_www_server_port_number()

        startup_future = Future()
        self._server_thread = Thread(
            target=self._run_web_server,
            args=(port_number, startup_future),
            name="WebServer")
        self._server_thread.start()

    @log
    def _run_web_server(self, port_number: int, startup_future: Future) -> None:
        """
        Prepares web content and runs the web server thread.

        :param port_number: port number to bind
        :param startup_future: future used to guard startup completion signals
        """
        try:
            self._prepare_web_server_content()
        except Exception as error:
            if not startup_future.done():
                startup_future.set_exception(error)
                self._web_server.startup_failed_signal.emit(error)
            return

        self._web_server.start(WEB_SERVER_BIND_HOST, port_number, startup_future)

    @log
    def _prepare_web_server_content(self) -> None:
        """
        Prepares files served by the web server.
        """
        Controller._setup_web_static_content()
        self._setup_web_initial_image()
        self.write_stack_info_json()

    @log
    def on_web_server_started(self) -> None:
        """
        Completes web server start state changes after bind success.
        """
        if DYNAMIC_DATA.web_server_status != WEB_SERVER_STATUS_STARTING:
            return

        advertised_address = self.update_web_server_advertised_address()
        MESSAGE_HUB.dispatch_info(__name__, QT_TRANSLATE_NOOP("", "Image server started"))

        DYNAMIC_DATA.web_server_status = WEB_SERVER_STATUS_RUNNING
        self._notify_model_observers()
        self._notify_web_server_started_observers()

        # if we can only advertise loopback, keep running but notify the powers that be
        if advertised_address.is_loopback:
            self._notify_web_server_access_is_limited_observers(advertised_address.ip)

    @log
    def on_web_server_start_failed(self, error: Exception) -> None:
        """
        Completes web server start state changes after startup failure.

        :param error: startup error reported by the web server thread
        """
        if DYNAMIC_DATA.web_server_status != WEB_SERVER_STATUS_STARTING:
            return

        self._server_thread = None
        DYNAMIC_DATA.web_server_status = WEB_SERVER_STATUS_STOPPED
        self._notify_model_observers()

        if isinstance(error, OSError):
            observer_error = PortInUseError()
        else:
            observer_error = error
        self._notify_web_server_start_failed_observers(observer_error)

    @log
    def _notify_web_server_started_observers(self) -> None:
        """
        Notifies web server observers that startup succeeded.
        """
        for observer in self._web_server_observers:
            observer.on_web_server_started()

    @log
    def _notify_web_server_access_is_limited_observers(self, displayed_address: str) -> None:
        """
        Notifies web server observers that only loopback access can be advertised.

        :param displayed_address: selected displayed address
        """
        for observer in self._web_server_observers:
            observer.on_web_server_access_is_limited(displayed_address)

    @log
    def _notify_web_server_start_failed_observers(self, error: Exception) -> None:
        """
        Notifies web server observers that startup failed.

        :param error: startup error
        """
        for observer in self._web_server_observers:
            observer.on_web_server_start_failed(error)

    @staticmethod
    @log
    def update_web_server_advertised_address() -> NetworkAddress:
        """
        Updates the web server address advertised to browser clients.

        :return: selected advertised address
        """
        port_number = config.get_www_server_port_number()
        address_candidates = get_network_address_candidates(port_number)
        advertised_address = select_advertised_address(
            config.get_www_server_advertised_address(),
            address_candidates)

        DYNAMIC_DATA.web_server_address_candidates = address_candidates
        DYNAMIC_DATA.web_server_advertised_ip = advertised_address.ip
        DYNAMIC_DATA.web_server_advertised_url = advertised_address.url
        return advertised_address

    @log
    def _send_message_to_clients(self, message):
        """
        Sends a message to all connected clients

        :param message: the message to send
        :type message: dict
        """
        if DYNAMIC_DATA.web_server_status == WEB_SERVER_STATUS_RUNNING:
            self._web_server.send_message(message)

    @log
    def notify_browsers_about_new_image(self):
        """
        Notifies all connected browsers about a new image
        """
        self._send_message_to_clients({"type": "new_image"})

    @log
    def stop_www(self, wait: bool = False):
        """Stops web server"""

        if self._web_server and DYNAMIC_DATA.web_server_status in WEB_SERVER_ACTIVE_STATUSES:
            if DYNAMIC_DATA.web_server_status == WEB_SERVER_STATUS_STOPPING:
                if wait and self._server_thread is not None:
                    self._server_thread.join()
                    self.on_web_server_stopped()
                return
            if self._server_thread is not None:
                DYNAMIC_DATA.web_server_status = WEB_SERVER_STATUS_STOPPING
                self._notify_model_observers()
                self._web_server.stop()
                if wait:
                    self._server_thread.join()
                    self.on_web_server_stopped()

    @log
    def on_web_server_stopped(self) -> None:
        """
        Completes web server stop state changes on the Qt thread.
        """
        if DYNAMIC_DATA.web_server_status == WEB_SERVER_STATUS_STOPPED:
            return
        self._server_thread = None
        MESSAGE_HUB.dispatch_info(__name__, QT_TRANSLATE_NOOP("", "Web server stopped"))
        DYNAMIC_DATA.web_server_status = WEB_SERVER_STATUS_STOPPED
        self._notify_model_observers()

    @staticmethod
    @log
    def purge_queue(queue: SignalingQueue):
        """
        Purge a queue

        :param queue: the queue to purge
        :type queue: SignalingQueue
        """

        while not queue.empty():
            queue.get()

    @log
    def _reset_current_sub_infos(self):
        
        DYNAMIC_DATA.current_sub_width = "n/a"
        DYNAMIC_DATA.current_sub_height = "n/a"
        DYNAMIC_DATA.current_sub_exposure_time = "n/a"
        DYNAMIC_DATA.current_sub_is_color = False
        DYNAMIC_DATA.current_sub_bayer_pattern = ""

    @staticmethod
    @log
    def _save_web_file(file_name, source_file):
        """
        Deletes the file if it exists and writes new content or copies from a source file.

        :param file_name: Name of the file to be deleted and written
        :type file_name: str
        :param source_file: Source file to copy from
        :type source_file: QFile
        """
        web_folder_path = config.get_web_folder_path()
        file_path = Path(web_folder_path) / file_name

        if file_path.is_file():
            file_path.unlink()

        source_file.copy(str(file_path.resolve()))
        file_path.chmod(0o644)

    @staticmethod
    @log
    def _setup_web_waiting_image():
        """
        Write the waiting image to web folder.
        """
        standby_image_path = WEB_SERVED_IMAGE_FILE_NAME_BASE + '.' + IMAGE_SAVE_TYPE_JPEG
        Controller._save_web_file(standby_image_path, source_file=QFile(":/web/waiting.jpg"))

    @staticmethod
    @log
    def _setup_web_static_content():
        """Prepares the web folder with the static content required by the server."""

        Controller._save_web_file("index.html", source_file=QFile(":/web/index.html"))

        Controller._save_web_file("favicon.ico", source_file=QFile(":/icons/als_logo.ico"))

        Controller._save_web_file("openseadragon.min.js", source_file=QFile(":/web/openseadragon.min.js"))

        icons_dir = Path(config.get_web_folder_path()) / "icons"
        icons_dir.mkdir(parents=True, exist_ok=True)

        icon_files = [
            "fullpage_grouphover.png", "fullpage_hover.png", "fullpage_pressed.png", "fullpage_rest.png",
            "home_grouphover.png", "home_hover.png", "home_pressed.png", "home_rest.png",
            "zoomin_grouphover.png", "zoomin_hover.png", "zoomin_pressed.png", "zoomin_rest.png",
            "zoomout_grouphover.png", "zoomout_hover.png", "zoomout_pressed.png", "zoomout_rest.png"
        ]

        for icon_file in icon_files:
            Controller._save_web_file(f"icons/{icon_file}", source_file=QFile(f":/webicons/{icon_file}"))

    @log
    def _setup_web_initial_image(self):
        """Writes the image that must be served when the server starts."""
        if DYNAMIC_DATA.stack_size > 0 and DYNAMIC_DATA.post_processor_result is not None:
            self.save_image(
                DYNAMIC_DATA.post_processor_result,
                IMAGE_SAVE_TYPE_JPEG,
                config.get_web_folder_path(),
                WEB_SERVED_IMAGE_FILE_NAME_BASE)
            return

        Controller._setup_web_waiting_image()

    @log
    def write_stack_info_json(self):
        """
        Writes a data.json file in the web folder containing STACK_SIZE and EXPO.
        """
        data = {
            "STACK_SIZE": DYNAMIC_DATA.stack_size,
            "EXPO": str(datetime.timedelta(seconds=int(round(DYNAMIC_DATA.total_exposure_time, 0))))
        }

        web_folder_path = config.get_web_folder_path()
        data_file_path = Path(web_folder_path) / "data.json"

        try:
            with open(data_file_path, 'w') as data_file:
                json.dump(data, data_file)
            _LOGGER.debug(f"data.json written to {data_file_path}")
        except OSError as e:
            _LOGGER.error(f"Failed to write data.json: {e}")

    @log
    def save_post_process_result(self, final=False):
        """
        Saves stacking result image to disk
        """

        # we save the image no matter what, then save a jpg for the web server if it is running
        image = DYNAMIC_DATA.post_processor_result

        if not final:
            self.save_image(image,
                            IMAGE_SAVE_TYPE_JPEG,
                            config.get_web_folder_path(),
                            WEB_SERVED_IMAGE_FILE_NAME_BASE)

            # if user want to save every image, we save a timestamped version
            if self._save_every_image:
                self.save_image(image,
                                config.get_image_save_format(),
                                config.get_work_folder_path(),
                                STACKED_IMAGE_FILE_NAME_BASE,
                                add_timestamp=True)

        self.save_image(image,
                        config.get_image_save_format(),
                        config.get_work_folder_path(),
                        STACKED_IMAGE_FILE_NAME_BASE + ("_final" if final else ""),
                        add_timestamp=final)

    # pylint: disable=R0913
    @log
    def save_image(self, image: Image,
                   file_extension: str,
                   dest_folder_path: str,
                   filename_base: str,
                   add_timestamp: bool = False):
        """
        Save an image to disk.

        :param image: the image to save
        :type image: Image
        :param file_extension: The image save file format extension
        :type file_extension: str
        :param dest_folder_path: The path of the folder image will be saved to
        :type dest_folder_path: str
        :param filename_base: The name of the file to save to (without extension)
        :type filename_base: str
        :param add_timestamp: Do we add a timestamp to image name
        :type add_timestamp: bool
        """
        if add_timestamp:
            filename_base += '-' + get_timestamp().replace(' ', "-").replace(":", '-').replace('.', '-')

        image_to_save = image.clone(keep_ref_to_data=True)
        image_to_save.destination = dest_folder_path + "/" + filename_base + '.' + file_extension
        self._saver_queue.put(image_to_save)

    @log
    def shutdown(self):
        """
        Proper shutdown of all app components
        """
        if not DYNAMIC_DATA.session.is_stopped:
            self.stop_session()

        if DYNAMIC_DATA.web_server_status in WEB_SERVER_ACTIVE_STATUSES:
            self.stop_www(wait=True)

        self._stop_queue_consumer(self._file_reader_queue, self._fileReader)
        self._stop_queue_consumer(self._pre_process_queue, self._pre_process_pipeline)
        self._stop_queue_consumer(self._stacker_queue, self._stacker)
        self._stop_queue_consumer(self._post_process_queue, self._post_process_pipeline)
        self._stop_queue_consumer(self._saver_queue, self._saver)

    @log
    def _stop_input_scanner(self):
        self._input_scanner.stop()
        MESSAGE_HUB.dispatch_info(__name__, QT_TRANSLATE_NOOP("", "Input scanner stopped"))

    @staticmethod
    @log
    def _stop_queue_consumer(queue: SignalingQueue, consumer: QueueConsumer) -> None:
        """
        Stops a queue consumer by enqueuing the stop sentinel and waiting for completion.

        :param queue: queue associated with the consumer
        :type queue: SignalingQueue
        :param consumer: consumer thread to stop
        :type consumer: QueueConsumer
        """
        queue.put(None)
        consumer.wait()
