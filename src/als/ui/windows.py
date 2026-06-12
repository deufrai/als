# SPDX-FileCopyrightText: 2019-2026 The ALS Authors
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Holds all windows used in the app
"""
import datetime
import platform
from logging import getLogger
from os import chmod, makedirs
from pathlib import Path
from typing import List

from PyQt5.QtCore import pyqtSlot, Qt, QStandardPaths, QResource, QTimer, QUrl
from PyQt5.QtGui import QPixmap, QIcon, QDesktopServices
# pylint: disable=no-name-in-module
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsPixmapItem, QDialog, QApplication, \
    QListWidgetItem, QLabel, QFrame, QFileDialog, QMessageBox, QWidget
from generated.als_ui import Ui_stack_window

import als.model.data
from als import config
from als.code_utilities import log, AlsLogAdapter
from als.config import CouldNotSaveConfig
from als.logic import Controller, SessionError, FolderSetupError, WebServerOnLoopback, \
    PortInUseError
from als.messaging import MESSAGE_HUB
from als.model.data import (
    DYNAMIC_DATA, I18n, WEB_SERVER_STATUS_RUNNING,
    WEB_SERVER_STATUS_STARTING, WEB_SERVER_STATUS_STOPPED,
    WEB_SERVER_STATUS_STOPPING
)
from als.ui.dialogs import PreferencesDialog, AboutDialog, error_box, warning_box, SaveWaitDialog, question, \
    message_box, SessionStopDialog, QRDisplay
from als.ui.params_utils import update_controls_from_params, update_params_from_controls, init_params, \
    set_sliders_defaults
from als.ui.widgets import Slider
from als.updates import find_available_update
from als.version import version as BUILD_VERSION

_LOGGER = AlsLogAdapter(getLogger(__name__), {})
_INFO_LOG_TAG = 'INFO'
ALS_DOCUMENTATION_URL = "https://als-app.org/docs/v1.0/?mtm_campaign=docFromApp"
CURRENT_STABLE_VERSION_URL = "https://als-app.org/current-stable.txt"
UPDATE_CHECK_TIMEOUT_MILLISECONDS = 20000

# pylint: disable=R0904, R0902
class MainWindow(QMainWindow):
    """
    ALS main window.
    """

    _LOG_DOCK_INITIAL_HEIGHT = 150

    # pylint: disable=too-many-statements
    @log
    def __init__(self, controller: Controller, parent=None):

        super().__init__(parent)

        self._warning_sign_off = QIcon()
        self._warning_sign_on = QIcon(QPixmap(":/icons/warning_sign.svg"))

        self.setWindowIcon(QIcon(":/icons/als_logo.png"))

        self._controller = controller
        self._ui = Ui_stack_window()
        self._ui.setupUi(self)
        self.setWindowTitle("Astro Live Stacker")

        self._qrDisplay = QRDisplay(self)
        self._qrDisplay.hide()
        self._qrDisplay.visibility_changed_signal[bool].connect(self.on_qr_display_visibility_changed)
        self._web_server_was_running = False
        self._update_check_network_manager = None
        self._update_check_reply = None
        self._update_check_timeout_timer = None

        # populate stacking mode combo box=
        self._ui.cb_stacking_mode.blockSignals(True)
        stacking_modes = [I18n.STACKING_MODE_SUM, I18n.STACKING_MODE_MEAN]
        for stacking_mode in stacking_modes:
            self._ui.cb_stacking_mode.addItem(stacking_mode)
        self._ui.cb_stacking_mode.setCurrentIndex(stacking_modes.index(self._controller.get_stacking_mode()))
        self._ui.cb_stacking_mode.blockSignals(False)

        # update align checkbox
        self._ui.chk_align.setChecked(self._controller.get_align_before_stack())

        # update save every frame checkbox
        self._ui.chk_save_every_image.setChecked(self._controller.get_save_every_image())

        # prevent log dock to be too tall
        self.resizeDocks([self._ui.log_dock], [MainWindow._LOG_DOCK_INITIAL_HEIGHT], Qt.Vertical)

        # setup rgb controls and params
        self._rgb_controls = [
            self._ui.chk_rgb_active,
            self._ui.sld_rgb_r,
            self._ui.sld_rgb_g,
            self._ui.sld_rgb_b,
            self._ui.sld_rgb_saturation,
        ]

        self._rgb_parameters = self._controller.get_rgb_parameters()

        set_sliders_defaults(
            [self._rgb_parameters[1], self._rgb_parameters[2], self._rgb_parameters[3], self._rgb_parameters[4]],
            [self._ui.sld_rgb_r, self._ui.sld_rgb_g, self._ui.sld_rgb_b, self._ui.sld_rgb_saturation]
        )

        init_params(self._rgb_parameters, self._rgb_controls)

        # setup autostretch controls and params
        self._autostretch_controls = [

            self._ui.chk_stretch_active,
            self._ui.sld_stretch_strength
        ]

        self._autostretch_parameters = self._controller.get_autostretch_parameters()

        set_sliders_defaults(
            [self._autostretch_parameters[1]],
            [self._ui.sld_stretch_strength]
        )

        init_params(self._autostretch_parameters, self._autostretch_controls)

        # setup levels controls and parameters
        self._levels_controls = [
            self._ui.chk_levels_active,
            self._ui.sld_black,
            self._ui.sld_midtones,
            self._ui.sld_white,
        ]

        self._levels_parameters = self._controller.get_levels_parameters()

        set_sliders_defaults(
            [self._levels_parameters[1], self._levels_parameters[2], self._levels_parameters[3]],
            [self._ui.sld_black, self._ui.sld_midtones, self._ui.sld_white]
        )

        init_params(self._levels_parameters, self._levels_controls)

        # setup exchanges with dynamic data
        self._controller.add_model_observer(self)

        self.setGeometry(*config.get_window_geometry())

        # setup management of 'image only' mode
        self._restore_log_dock = False
        self._restore_session_dock = False
        self._restore_processing_dock = False

        # setup image display
        self._image_item = None
        self.reset_image_view()

        self._setup_statusbar()

        self.update_display()
        MESSAGE_HUB.add_receiver(self)

        if 0 == config.get_profile():
            self._lbl_statusbar_current_profile.setText(f"{I18n.PROFILE} : {I18n.VISUAL}")
        else:
            self._lbl_statusbar_current_profile.setText(f"{I18n.PROFILE} : Photo")

        self._ui.action_full_screen.setChecked(config.get_full_screen_active())

        if config.get_full_screen_active():
            self.showFullScreen()
        elif config.get_window_maximized():
            self.showMaximized()
        else:
            self.show()

        self._ui.action_create_launcher.setVisible(platform.system().lower() == 'linux')

        if config.get_check_updates_on_startup_active():
            QTimer.singleShot(2000, self._start_update_check)

    @log
    def _start_update_check(self):
        """
        Starts the optional asynchronous check for a newer ALS release.
        """
        self._update_check_network_manager = QNetworkAccessManager(self)
        request = QNetworkRequest(QUrl(CURRENT_STABLE_VERSION_URL))
        request.setRawHeader(
            b"User-Agent",
            f"ALS/{BUILD_VERSION}".encode("ascii", "replace")
        )

        self._update_check_reply = self._update_check_network_manager.get(request)
        self._update_check_reply.finished.connect(self._on_update_check_finished)

        self._update_check_timeout_timer = QTimer(self)
        self._update_check_timeout_timer.setSingleShot(True)
        self._update_check_timeout_timer.timeout.connect(self._on_update_check_timeout)
        self._update_check_timeout_timer.start(UPDATE_CHECK_TIMEOUT_MILLISECONDS)

    @log
    def _on_update_check_finished(self):
        """
        Processes a completed update request and releases request resources.
        """
        reply = self._update_check_reply
        if reply is None:
            return

        if self._update_check_timeout_timer is not None:
            self._update_check_timeout_timer.stop()

        if reply.error() == QNetworkReply.NoError:
            try:
                remote_version_content = bytes(reply.readAll()).decode("utf-8")
            except UnicodeDecodeError:
                remote_version_content = ""

            available_version = find_available_update(
                BUILD_VERSION,
                remote_version_content
            )
            if available_version is not None:
                self._ui.lbl_available_update.setText(
                    self.tr("ALS {} is available").format(available_version))
                self._ui.lbl_available_update.show()

        self._release_update_check_resources()

    @log
    def _on_update_check_timeout(self):
        """
        Aborts an update request that exceeded the configured timeout.
        """
        if self._update_check_reply is not None:
            self._update_check_reply.abort()

    @log
    def _release_update_check_resources(self):
        """
        Releases objects used by the one-shot update request.
        """
        if self._update_check_reply is not None:
            self._update_check_reply.deleteLater()
            self._update_check_reply = None

        if self._update_check_timeout_timer is not None:
            self._update_check_timeout_timer.deleteLater()
            self._update_check_timeout_timer = None

        if self._update_check_network_manager is not None:
            self._update_check_network_manager.deleteLater()
            self._update_check_network_manager = None

    @log
    def _setup_statusbar(self):
        """
        Initialize status bar widgets and layout.
        """
        self._lbl_statusbar_current_profile = QLabel(self._ui.statusBar)
        self._lbl_statusbar_current_profile.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self._lbl_statusbar_frame_total_proc = QLabel(self._ui.statusBar)
        self._lbl_statusbar_frame_total_proc.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self._lbl_statusbar_stack_exposure = QLabel(self._ui.statusBar)
        self._lbl_statusbar_stack_exposure.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self._lbl_statusbar_session_status = QLabel(self._ui.statusBar)
        self._lbl_statusbar_session_status.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self._lbl_statusbar_scanner_status = QLabel(self._ui.statusBar)
        self._lbl_statusbar_scanner_status.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self._lbl_statusbar_stack_size = QLabel(self._ui.statusBar)
        self._lbl_statusbar_stack_size.setMinimumWidth(150)
        self._lbl_statusbar_stack_size.setAlignment(Qt.AlignHCenter)
        self._lbl_statusbar_stack_size.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self._lbl_statusbar_web_server_status = QLabel(self._ui.statusBar)
        self._lbl_statusbar_web_server_status.setOpenExternalLinks(True)
        self._lbl_statusbar_web_server_status.setFrameStyle(QFrame.Panel | QFrame.Sunken)

        self._ui.statusBar.addPermanentWidget(self._lbl_statusbar_session_status)
        self._ui.statusBar.addPermanentWidget(self._lbl_statusbar_current_profile)
        self._ui.statusBar.addPermanentWidget(self._lbl_statusbar_scanner_status)
        self._ui.statusBar.addPermanentWidget(self._lbl_statusbar_stack_size)
        self._ui.statusBar.addPermanentWidget(self._lbl_statusbar_stack_exposure)
        self._ui.statusBar.addPermanentWidget(self._lbl_statusbar_web_server_status)
        self._ui.statusBar.addPermanentWidget(self._lbl_statusbar_frame_total_proc)

    @log
    @pyqtSlot(bool)
    def on_chk_stretch_active_clicked(self, checked: bool):
        """
        Qt slot executed when autostretch 'active' checkbox is clicked

        :param checked: is the box now checked ?
        :type: bool
        """

        self._ui.btn_stretch_reload.setEnabled(checked)
        self._ui.btn_stretch_reset.setEnabled(checked)
        self._ui.btn_stretch_apply.setEnabled(checked)
        self._ui.sld_stretch_strength.setEnabled(checked)

        self.on_btn_stretch_apply_clicked()

    @log
    @pyqtSlot(bool)
    def on_chk_levels_active_clicked(self, checked: bool):
        """
        Qt slot executed when levels 'active' checkbox is clicked

        :param checked: is the box now checked ?
        :type: bool
        """

        self._ui.btn_levels_reload.setEnabled(checked)
        self._ui.btn_levels_reset.setEnabled(checked)
        self._ui.btn_levels_apply.setEnabled(checked)
        self._ui.sld_black.setEnabled(checked)
        self._ui.sld_midtones.setEnabled(checked)
        self._ui.sld_white.setEnabled(checked)

        self.on_btn_levels_apply_clicked()

    @log
    @pyqtSlot(bool)
    def on_chk_rgb_active_clicked(self, checked: bool):
        """
        Qt slot executed when RGB 'active' checkbox is clicked

        :param checked: is the box now checked ?
        :type: bool
        """

        self._ui.btn_rgb_reload.setEnabled(checked)
        self._ui.btn_rgb_reset.setEnabled(checked)
        self._ui.btn_rgb_apply.setEnabled(checked)
        self._ui.sld_rgb_r.setEnabled(checked)
        self._ui.sld_rgb_g.setEnabled(checked)
        self._ui.sld_rgb_b.setEnabled(checked)
        self._ui.sld_rgb_saturation.setEnabled(checked)

        self.on_btn_rgb_apply_clicked()

    @log
    @pyqtSlot(bool)
    def on_btn_stretch_apply_clicked(self, checked: bool = False):
        """
        Apply autostretch processing
        """
        update_params_from_controls(self._autostretch_parameters, self._autostretch_controls)

        self._controller.apply_processing()

    @log
    @pyqtSlot(bool)
    def on_btn_rgb_apply_clicked(self, checked: bool = False):
        """
        Apply rgb processing
        """
        update_params_from_controls(self._rgb_parameters, self._rgb_controls)

        self._controller.apply_processing()

    @log
    @pyqtSlot(bool)
    def on_btn_levels_apply_clicked(self, checked: bool = False):
        """
        Apply levels processing
        """
        update_params_from_controls(self._levels_parameters, self._levels_controls)

        self._controller.apply_processing()

    @log
    def _reset_sliders(self, controls: List[QWidget]):
        """
        Resets sliders in a list to their default values

        :param controls: the list of sliders to reset
        :type controls: List[QWidget]
        """
        for control in controls:
            if isinstance(control, Slider):
                control.setValue(control.default_value())

    @log
    @pyqtSlot(bool)
    def on_btn_stretch_reset_clicked(self, checked: bool = False):
        """
        Resets autostretch controls to their defaults
        """
        self._reset_sliders(self._autostretch_controls)

    @log
    @pyqtSlot(bool)
    def on_btn_rgb_reset_clicked(self, checked: bool = False):
        """
        Resets rgb controls to their defaults
        """
        self._reset_sliders(self._rgb_controls)

    @log
    @pyqtSlot(bool)
    def on_btn_levels_reset_clicked(self, checked: bool = False):
        """
        Resets levels processing controls to their defaults
        """
        self._reset_sliders(self._levels_controls)

    @log
    @pyqtSlot(bool)
    def on_btn_rgb_reload_clicked(self, checked: bool = False):
        """
        Sets rgb controls to their previously recorded values (last apply)
        """
        update_controls_from_params(self._rgb_parameters, self._rgb_controls)

    @log
    @pyqtSlot(bool)
    def on_btn_stretch_reload_clicked(self, checked: bool = False):
        """
        Sets autostretch controls to their previously recorded values (last apply)
        """
        update_controls_from_params(self._autostretch_parameters, self._autostretch_controls)

    @log
    @pyqtSlot(bool)
    def on_btn_levels_reload_clicked(self, checked: bool = False):
        """
        Sets levels processing controls to their previously recorded values (last apply)
        """
        update_controls_from_params(self._levels_parameters, self._levels_controls)

    @log
    def reset_image_view(self):
        """
        Reset image viewer to its initial state
        """
        self._ui.image_view.setScene(QGraphicsScene(self))
        self._ui.image_view.reset_zoom()
        self._image_item = QGraphicsPixmapItem(QPixmap(":/icons/window_background.png"))
        self._ui.image_view.scene().addItem(self._image_item)


    @log
    def closeEvent(self, event):
        """Handles window close events."""
        # pylint: disable=C0103

        if not self.isFullScreen():
            window_rect = self.geometry()
            config.set_window_geometry((window_rect.x(), window_rect.y(), window_rect.width(), window_rect.height()))

        config.set_full_screen_active(self.isFullScreen())
        config.set_window_maximized(self.isMaximized())
        self._save_config()

        self._stop_session()

        if DYNAMIC_DATA.session.is_stopped:

            image_waiter = SaveWaitDialog(self._controller, self)

            if image_waiter.count_remaining_images() > 0:
                image_waiter.exec()

            event.accept()
        else:
            event.ignore()

    @log
    @pyqtSlot(bool)
    def on_btn_follow_logs_clicked(self, checked):
        """
        scroll session log to last message when checkbox is checked

        :param checked: is the checkbox checked ?
        :type checked: bool
        """

        if checked:
            self._ui.log.scrollToBottom()

    @log
    @pyqtSlot(bool)
    def on_btn_issues_only_clicked(self, toggled):
        """
        Filters out INFO messages from session log button is toggled

        :param toggled: is button toggled ?
        :type toggled: bool
        """

        if toggled:
            for item in self._ui.log.findItems(_INFO_LOG_TAG, Qt.MatchContains):
                item.setHidden(True)
        else:
            for i in range(self._ui.log.count()):
                self._ui.log.item(i).setHidden(False)

        if self._ui.btn_follow_logs.isChecked():
            self._ui.log.scrollToBottom()

    @pyqtSlot(bool)
    @log
    def on_btn_save_clicked(self, checked: bool = False):
        """
        Qt slot for mouse clicks on the 'save' button.

        This saves the processed image using user chosen format

        """
        image_to_save = DYNAMIC_DATA.post_processor_result
        if image_to_save is not None:
            self._controller.save_image(image_to_save,
                                        config.get_image_save_format(),
                                        config.get_work_folder_path(),
                                        als.model.data.STACKED_IMAGE_FILE_NAME_BASE,
                                        add_timestamp=True)

    @pyqtSlot(bool)
    @log
    def on_action_quit_triggered(self, checked: bool = False):
        """ Qt slot for activation of the 'quit' action"""
        super().close()

    @pyqtSlot(bool)
    @log
    def on_action_prefs_triggered(self, checked: bool = False):
        """ Qt slot for activation of the 'preferences' action"""
        self._open_preferences()

    @pyqtSlot(bool)
    @log
    def on_action_about_als_triggered(self, checked: bool = False):
        """ Qt slot for activation of the 'about' action"""
        dialog = AboutDialog(self)
        dialog.resize(dialog.minimumSize())
        dialog.exec()

    @log
    def on_sld_align_threshold_valueChanged(self, value):
        """
        align threshold slider value just changed.

        We register that value for next stacking operation

        :param value: new stacking threshold
        :type value: int
        """
        config.set_minimum_match_count(value)

    # pylint: disable=C0103
    @log
    def on_cb_stacking_mode_currentTextChanged(self, stacking_mode: str):
        """
        Qt slot executed when stacking mode comb box changed

        :param stacking_mode: new stacking mode
        :type stacking_mode: str
        """
        self._controller.set_stacking_mode(stacking_mode)

    @log
    def on_chk_align_toggled(self, checked: bool):
        """
        Qt slot executed when 'align' check box is changed

        :param checked: is checkbox checked ?
        :type checked: bool
        """
        self._controller.set_align_before_stack(checked)

    @log
    def on_chk_save_every_image_toggled(self, checked: bool):
        """
        Qt slot executed when 'save ever image' check box is changed

        :param checked: is checkbox checked ?
        :type checked: bool
        """
        self._controller.set_save_every_image(checked)

    @pyqtSlot()
    @log
    def on_btn_web_start_clicked(self):
        """
        Qt slot executed when START web button is clicked
        """

        self._ui.btn_web_start.setEnabled(False)
        self._ui.lbl_web_server_status_main.setText(I18n.STARTING)
        QApplication.processEvents()

        try:
            self._controller.start_www()
            self._qrDisplay.update_code()

        except PortInUseError:
            error_message = self.tr("Port {} is already in use.").format(config.get_www_server_port_number())
            error_message_part2 = "\n\n" + self.tr("Change server port number in preferences and start server again")
            error_title = self.tr("Could not start web server")
            MESSAGE_HUB.dispatch_error(__name__, error_title + ". " + error_message)
            error_box(error_title, error_message + error_message_part2)

        except WebServerOnLoopback:
            self._warn_web_server_access_is_limited()

        finally:
            self.update_display()

    @pyqtSlot()
    @log
    def on_btn_web_stop_clicked(self):
        """
        Qt slot executed when STOP web button is clicked
        """
        self._controller.stop_www()


    @log
    def on_action_full_screen_toggled(self, checked):
        """
        Qt slot executed when action 'Full screen' is toggled

        :param checked: is the action active ?
        :type checked: bool
        """

        if checked:
            self.showFullScreen()
        else:
            self.showNormal()

    @log
    @pyqtSlot(bool)
    def on_action_help_triggered(self, _):
        """
        Open the user's default browser and navigate to ALS documentation.
        """
        QDesktopServices.openUrl(QUrl(ALS_DOCUMENTATION_URL))


    @log
    @pyqtSlot(bool)
    def on_action_qrcode_toggled(self, checked):
        """
        QR action has changed : we deal with QR Code display

        :param checked: is action now checked ?
        :type checked: bool
        """
        self._qrDisplay.setVisible(checked)

    @log
    def on_qr_display_visibility_changed(self, visible):
        """
        QR Code display's visibility just changed.

        :param visible: is QR code visible now ?
        :type visible: bool
        """
        self._ui.action_qrcode.setChecked(visible)

    @pyqtSlot()
    @log
    def on_action_image_only_triggered(self):
        """
        Qt slot executed when 'image only' action is triggered
        """

        actions_restore_mapping = {

            self._ui.action_show_processing_panel: self._restore_processing_dock,
            self._ui.action_show_session_controls: self._restore_session_dock,
            self._ui.action_show_session_log: self._restore_log_dock,
        }

        checked = self._ui.action_image_only.isChecked()

        if checked:

            self._restore_session_dock = self._ui.session_dock.isVisible()
            self._restore_log_dock = self._ui.log_dock.isVisible()
            self._restore_processing_dock = self._ui.processing_dock.isVisible()

            for action in actions_restore_mapping:

                if action.isChecked():
                    action.trigger()

        else:
            for action, restore in actions_restore_mapping.items():

                if restore:
                    action.trigger()

    @log
    @pyqtSlot(bool)
    def on_action_zoom_in_triggered(self, _):
        """ user wants to zoom into the image """
        self._ui.image_view.zoom_in()

    @log
    @pyqtSlot(bool)
    def on_action_zoom_out_triggered(self, _):
        """ user wants to zoom out of the image """
        self._ui.image_view.zoom_out()

    @log
    @pyqtSlot(bool)
    def on_action_zoom_reset_triggered(self, _):
        """ user wants to reset image zoom """
        self._ui.image_view.reset_zoom()

    @log
    @pyqtSlot(bool)
    def on_action_adjust_image_triggered(self, _):
        """ user wants to adjust image to view """
        self._ui.image_view.adjustZoom()

    @log
    def on_processing_dock_visibilityChanged(self, visible):
        """
        Qt slot executed when prcessing dock visibility changed

        :param visible: is it now visible ?
        :type visible: bool
        """

        if visible:
            self._cancel_image_only_mode()

    @log
    def on_log_dock_visibilityChanged(self, visible):
        """
        Qt slot executed when log dock visibility changed

        :param visible: is it now visible ?
        :type visible: bool
        """
        self._update_issues_button_visibility()

        if visible:
            self._cancel_image_only_mode()
            self._ui.log.scrollToBottom()

    @log
    @pyqtSlot(bool)
    def on_btn_issues_clicked(self, _):
        """ Main control panel issues button clicked """

        if not self._ui.log_dock.isVisible():
            self._ui.log_dock.setVisible(True)

    @log
    @pyqtSlot(bool)
    def on_btn_issues_ack_clicked(self, _):
        """ issues ack button clicked """

        self._ui.action_ack_issues.trigger()

    @log
    @pyqtSlot()
    def on_action_ack_issues_triggered(self):
        """ user acknowledged issues """

        DYNAMIC_DATA.has_new_warnings = False
        self.update_display(False)

    # pylint: disable=no-self-use
    @log
    def on_log_itemClicked(self, item):
        """
        Copy clicked log line content to clipboard

        :param item: the clicked log item
        :type item: PyQt5.QtWidgets.QListWidgetItem
        """
        QApplication.clipboard().setText(item.text())

    @log
    def on_session_dock_visibilityChanged(self, visible):
        """
        Qt slot executed when session dock visibility changed

        :param visible: is it now visible ?
        :type visible: bool
        """

        if visible:
            self._cancel_image_only_mode()

    @log
    def _cancel_image_only_mode(self):
        """
        Untick 'image only' menu entry
        """

        self._ui.action_image_only.setChecked(False)

    @log
    def _update_image(self):
        """
        Update central image display.
        """
        self._image_item.setPixmap(DYNAMIC_DATA.post_processor_result_qimage)


    @pyqtSlot()
    @log
    def on_btn_session_start_clicked(self):
        """Qt slot for mouse clicks on the session START button"""

        self._ui.btn_session_start.setEnabled(False)
        self._ui.lbl_session_status.setText(I18n.STARTING)
        QApplication.processEvents()

        self._start_session()
        self.update_display()

    @log
    def on_message(self, message):
        """
        print received message to GUI log window

        :param message: the message
        :type message: str
        """
        new_item = QListWidgetItem(message)
        if any([log_type in message for log_type in ['WARNING', 'ERROR']]):
            DYNAMIC_DATA.has_new_warnings = True

        self._ui.log.addItem(new_item)
        if _INFO_LOG_TAG in message and self._ui.btn_issues_only.isChecked():
            new_item.setHidden(True)

        if self._ui.btn_follow_logs.isChecked() and self._ui.log.isVisible():
            self._ui.log.scrollToBottom()

    # pylint: disable=too-many-statements
    @log
    def update_display(self, image_only: bool = False):
        """
        Updates all displays and controls depending on DataStore held data
        """

        if image_only:
            self._update_image()
            self._ui.histogram_view.update()

        else:
            web_server_status = DYNAMIC_DATA.web_server_status
            web_server_is_running = web_server_status == WEB_SERVER_STATUS_RUNNING
            web_server_is_starting = web_server_status == WEB_SERVER_STATUS_STARTING
            web_server_is_stopped = web_server_status == WEB_SERVER_STATUS_STOPPED
            web_server_is_stopping = web_server_status == WEB_SERVER_STATUS_STOPPING
            session = DYNAMIC_DATA.session
            session_is_running = session.is_running
            session_is_stopped = session.is_stopped
            session_is_paused = session.is_paused

            # update web server status and QR visibility
            if web_server_is_running:
                url = DYNAMIC_DATA.web_server_advertised_url
                web_server_status_text = f'{I18n.RUNNING_M} : <a href="{url}" style="color: #CC0000">{url}</a>'
                self._ui.action_qrcode.setEnabled(True)
            elif web_server_is_starting:
                web_server_status_text = I18n.STARTING
                self._ui.action_qrcode.setDisabled(True)
            elif web_server_is_stopping:
                web_server_status_text = I18n.STOPPING
                self._ui.action_qrcode.setDisabled(True)
            else:
                web_server_status_text = I18n.STOPPED_M
                self._ui.action_qrcode.setDisabled(True)

            if self._web_server_was_running and not web_server_is_running:
                self._qrDisplay.setVisible(False)

            self._web_server_was_running = web_server_is_running

            self._ui.lbl_web_server_status_main.setText(f"{web_server_status_text}")

            if session_is_stopped:
                session_status = I18n.STOPPED_F
            elif session_is_paused:
                session_status = I18n.PAUSED
            elif session_is_running:
                session_status = I18n.RUNNING_F
            else:
                # this should never happen, that's why we check ;)
                session_status = "### BUG !"

            self._ui.lbl_session_status.setText(f"{session_status}")

            # handle Start / Pause / Stop  buttons
            self._ui.btn_session_start.setEnabled(session_is_stopped or session_is_paused)
            self._ui.btn_session_stop.setEnabled(session_is_running or session_is_paused)
            self._ui.btn_session_pause.setEnabled(session_is_running)

            # handle align + stack mode buttons
            self._ui.chk_align.setEnabled(session_is_stopped)
            self._ui.cb_stacking_mode.setEnabled(session_is_stopped)

            # handle web stop start buttons
            self._ui.btn_web_start.setEnabled(web_server_is_stopped)
            self._ui.btn_web_stop.setEnabled(web_server_is_running)

            # update stack size and total exposure time
            stack_size_str = str(DYNAMIC_DATA.stack_size)
            self._ui.lbl_stack_size.setText(stack_size_str)
            exposure_time_str = str(datetime.timedelta(seconds=int(round(DYNAMIC_DATA.total_exposure_time, 0))))
            self._ui.lbl_stack_exposure.setText(exposure_time_str)

            # update statusbar labels
            scanner_status_message = f"{I18n.SCANNER} {I18n.OF} {config.get_scan_folder_path()} : "
            scanner_status_message += f"{I18n.RUNNING_M}" if session_is_running else f"{I18n.STOPPED_M}"
            self._lbl_statusbar_scanner_status.setText(scanner_status_message)
            self._lbl_statusbar_web_server_status.setText(f"{I18n.WEB_SERVER} : {web_server_status_text}")
            self._lbl_statusbar_session_status.setText(f"{I18n.SESSION} {session_status}")
            self._lbl_statusbar_stack_size.setText(f"{I18n.STACK_SIZE} : {stack_size_str}")
            self._lbl_statusbar_stack_exposure.setText(
                self.tr("Total stack exp. time: {}").format(exposure_time_str))
            self._lbl_statusbar_frame_total_proc.setText(
                self.tr("Total frame proc. time: {} s").format(f"{DYNAMIC_DATA.last_timing:6.1f}"))

            # update queues sizes
            self._ui.lbl_pre_process_queue_size.setText(str(DYNAMIC_DATA.pre_process_queue.qsize()))
            self._ui.lbl_stack_queue_size.setText(str(DYNAMIC_DATA.stacker_queue.qsize()))
            self._ui.lbl_process_queue_size.setText(str(DYNAMIC_DATA.process_queue.qsize()))
            self._ui.lbl_save_queue_size.setText(str(DYNAMIC_DATA.save_queue.qsize()))

            # handle component statuses
            self._ui.lbl_pre_processor_status.setText(I18n.WORKER_STATUS_BUSY if DYNAMIC_DATA.pre_processor_busy else "-")
            self._ui.lbl_stacker_status.setText(I18n.WORKER_STATUS_BUSY if DYNAMIC_DATA.stacker_busy else "-")
            self._ui.lbl_post_processor_status.setText(I18n.WORKER_STATUS_BUSY if DYNAMIC_DATA.post_processor_busy else "-")
            self._ui.lbl_saver_status.setText(I18n.WORKER_STATUS_BUSY if DYNAMIC_DATA.saver_busy else "-")

            # manage warnings
            new_warnings = DYNAMIC_DATA.has_new_warnings
            self._ui.action_ack_issues.setEnabled(new_warnings)

            self._ui.btn_issues_ack.setEnabled(new_warnings)
            self._ui.btn_issues.setEnabled(new_warnings)

            self._ui.btn_issues_ack.setIcon(self._warning_sign_on if new_warnings else self._warning_sign_off)
            self._ui.btn_issues.setIcon(self._warning_sign_on if new_warnings else self._warning_sign_off)

            self._update_issues_button_visibility()

            # disable color balance controls on B&W image
            if DYNAMIC_DATA.post_processor_result:
                self._ui.rgbProcessBox.setEnabled(DYNAMIC_DATA.post_processor_result.is_color())

            self._ui.sld_align_threshold.setValue(config.get_minimum_match_count())
            self._ui.lbl_align_threshold.setText(str(self._ui.sld_align_threshold.value()))

    @pyqtSlot()
    @log
    def on_btn_session_stop_clicked(self):
        """Qt slot for mouse clicks on the session STOP button"""

        self._ui.btn_session_stop.setEnabled(False)
        self._ui.lbl_session_status.setText(I18n.STOPPING)
        QApplication.processEvents()
        self._stop_session()
        self.update_display()

    @pyqtSlot()
    @log
    def on_btn_session_pause_clicked(self):
        """Qt slot for mouse clicks on the session PAUSE button"""

        self._ui.btn_session_pause.setEnabled(False)
        QApplication.processEvents()
        self._controller.pause_session()
        self.update_display()

    @log
    def _start_session(self, is_retry: bool = False):
        """
        Stars session

        :param is_retry: is this a retry ?
        :type is_retry: bool
        """

        try:
            if DYNAMIC_DATA.session.is_stopped:
                self._ui.log.clear()
                self.reset_image_view()
            self._controller.start_session()
            if is_retry:
                message_box(self.tr("Session started"), self.tr("Session successfully started after retry"))

        except FolderSetupError as folder_error:

            text = folder_error.details + "\n\n" + self.tr("Session cannot start" + "\n\n")
            text += self.tr("Do you want to fix the issue in ALS preferences ?")

            if question(folder_error.message, text) and self._open_preferences():
                self._start_session(is_retry=True)

        except SessionError as session_error:
            error_box(session_error.message, str(session_error.details) + "\n\n" + self.tr("Session start aborted"))

    @log
    def _stop_session(self, ask_confirmation: bool = True):
        """
        Stops sessions

        :param ask_confirmation: do we ask user for confirmation ?
        :type ask_confirmation: bool
        """

        if not DYNAMIC_DATA.session.is_stopped:

            do_stop_session = True
            stop_dialog = SessionStopDialog()

            if ask_confirmation and DYNAMIC_DATA.stack_size > 0:

                do_stop_session = stop_dialog.exec()

            if do_stop_session:
                if stop_dialog.save_on_stop and DYNAMIC_DATA.post_processor_result is not None:
                    self._controller.save_post_process_result(final=True)
                self._controller.stop_session()

    @log
    def _open_preferences(self):
        """
        Opens preferences dialog box and return True if dialog was closed using "OK"

        :return: Was the dilaog closed with "OK" ?
        :rtype: bool
        """

        previous_advertised_ip = DYNAMIC_DATA.web_server_advertised_ip
        accepted = PreferencesDialog(self).exec() == QDialog.Accepted

        if accepted:

            self.update_display()

            if (
                    DYNAMIC_DATA.web_server_status == WEB_SERVER_STATUS_RUNNING
                    and previous_advertised_ip != DYNAMIC_DATA.web_server_advertised_ip):

                if self._qrDisplay.isVisible():
                    self._qrDisplay.update_code()

                advertised_address = self._find_web_server_advertised_address()

                if advertised_address is not None and advertised_address.is_loopback:
                    self._warn_web_server_access_is_limited(advertised_address.ip)

        return accepted

    @log
    def _find_web_server_advertised_address(self):
        """
        Finds the selected web server advertised address candidate.

        :return: selected advertised address candidate or None
        """
        for candidate in DYNAMIC_DATA.web_server_address_candidates:
            if candidate.ip == DYNAMIC_DATA.web_server_advertised_ip:
                return candidate
        return None

    @log
    def _warn_web_server_access_is_limited(self, displayed_address: str = None):
        """
        Displays the limited web server access warning.

        :param displayed_address: selected displayed address
        """
        title = self.tr("Image server access is limited")
        message = self.tr(
            "Displayed address is {}.\n\n"
            "Other devices on your network will not be able to browse the image server from that address.\n\n"
            "If another device needs to browse the image server, change the Displayed address in "
            "Preferences > Output > Server, then retry from that device."
        ).format(displayed_address or DYNAMIC_DATA.web_server_advertised_ip)
        warning_box(title, message)

    @log
    def _save_config(self):

        try:
            config.save()
        except CouldNotSaveConfig as save_error:
            error_box(
                save_error.message,
                self.tr("Your settings could not be saved\n\nDetails : {}").format(save_error.details))

    @log
    def _update_issues_button_visibility(self):
        """ update issues button according to warnings & log visibility """

        self._ui.btn_issues.setVisible(

            self._ui.action_ack_issues.isEnabled() and not self._ui.log_dock.isVisible()
        )

    @log
    @pyqtSlot(bool)
    def on_action_create_launcher_triggered(self, _):
        """
        Creates a desktop application launcher for 'Astro Live Stacker' on Linux systems.

        It involves setting up an icon in the user's local share directory,
        creating a .desktop launcher file,
        and handling potential errors

        :return: None
        """
        if platform.system().lower() == 'linux':

            home_path = QStandardPaths.writableLocation(QStandardPaths.HomeLocation)
            local_share_path = Path(home_path).joinpath(".local", "share")
            local_icons_path = Path(local_share_path).joinpath("icons")
            local_apps_path = Path(local_share_path).joinpath("applications")
            target_dirs = [local_icons_path, local_apps_path]
            launcher_path = Path(local_apps_path).joinpath("als.desktop")
            icon_path = Path(local_icons_path).joinpath("als.png")
            resource_path = ":/icons/als_logo.png"

            # switch for PCs vs RPI64
            if platform.machine().lower() == 'aarch64':
                file_filter = "als*"
            else:
                file_filter = "als*.run"

            als_path = QFileDialog.getOpenFileName(self,
                                                   caption=self.tr("Select your ALS executable"),
                                                   directory=home_path,
                                                   filter=file_filter,
                                                   options=QFileDialog.DontUseNativeDialog)[0]

            if als_path:

                try:

                    for target_dir in target_dirs:
                        makedirs(target_dir, exist_ok=True)

                    with open(icon_path, 'wb') as f:
                        f.write(QResource(resource_path).data())

                    with open(launcher_path, 'w') as f:

                        f.write("#!/usr/bin/env xdg-open\n")
                        f.write("[Desktop Entry]\n")
                        f.write(f"Name=Astro Live Stacker\n")
                        f.write(f"Type=Application\n")
                        f.write(f"Icon={icon_path}\n")
                        f.write(f"Version=1.0\n")
                        f.write(f"Terminal=False\n")
                        f.write(f"Categories=Graphics\n")
                        f.write(f"Comment=Live Stacking Made in France\n")
                        f.write(f"Exec={als_path}\n")
                        chmod(str(launcher_path), 0o750)

                        QMessageBox.information(self,
                                                self.tr('ALS launcher created / updated.'),
                                                self.tr("You'll find ALS with the graphics apps"))

                except FileNotFoundError as e:
                    QMessageBox.critical(self, "File Error", f"File not found: {e}")
                except PermissionError as e:
                    QMessageBox.critical(self, "Permission Error", f"Permission denied: {e}")
                except OSError as e:
                    QMessageBox.critical(self, "OS Error", f"OS error: {e}")
                except ValueError as e:
                    QMessageBox.critical(self, "Value Error", f"Value error: {e}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")
