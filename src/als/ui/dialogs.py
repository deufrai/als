"""
Provides all dialogs used in ALS GUI
"""
from logging import getLogger
from os import mkdir
from pathlib import Path

import qrcode
from PIL.ImageQt import ImageQt
from PyQt5.QtCore import pyqtSlot, QT_TRANSLATE_NOOP, pyqtSignal, Qt, QStandardPaths
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox, QApplication
from generated.about_ui import Ui_AboutDialog
from generated.first_run_ui import Ui_FirstRunDialog
from generated.prefs_ui import Ui_PrefsDialog
from generated.qr_ui import Ui_QrDialog
from generated.save_wait_ui import Ui_SaveWaitDialog
from generated.stop_ui import Ui_SessionStopDialog

import als.model.data
from als import config
from als.code_utilities import log, AlsLogAdapter
from als.logic import Controller
from als.messaging import MESSAGE_HUB
from als.model.data import (
    VERSION, DYNAMIC_DATA, I18n, WEB_SERVER_ACTIVE_STATUSES,
    WEB_SERVER_STATUS_RUNNING
)
from als.streams.network import (
    ADVERTISED_ADDRESS_AUTO, build_advertised_address_preference,
    get_network_address_candidates
)

_LOGGER = AlsLogAdapter(getLogger(__name__), {})
_WARNING_STYLE_SHEET = "border: 1px solid orange"
_NORMAL_STYLE_SHEET = "border: 1px"
class PreferencesDialog(QDialog):
    """
    Our main preferences dialog box
    """

    @log
    def __init__(self, parent=None):
        super().__init__(parent)
        self._ui = Ui_PrefsDialog()
        self._ui.setupUi(self)

        self._ui.tabWidget.setCurrentIndex(0)
        self._ui.scannerBox.setEnabled(DYNAMIC_DATA.session.is_stopped)
        self._ui.preprocessBox.setEnabled(DYNAMIC_DATA.session.is_stopped)
        web_server_is_active = (
            DYNAMIC_DATA.web_server_status in WEB_SERVER_ACTIVE_STATUSES)
        self._ui.pathsBox.setEnabled(
            not web_server_is_active and DYNAMIC_DATA.session.is_stopped)
        _set_web_server_port_controls_enabled(
            self._ui, not web_server_is_active)


        self._ui.cmb_lang.setItemData(0, 'sys')
        self._ui.cmb_lang.setItemData(1, 'en')
        self._ui.cmb_lang.setItemData(2, 'fr')
        self._ui.cmb_lang.setItemData(3, 'ru')
        self._ui.cmb_lang.setCurrentIndex(self._ui.cmb_lang.findData(config.get_lang()))

        for pattern_index in range(5):
            self._ui.cmb_bayer_pattern.setItemData(pattern_index, self._ui.cmb_bayer_pattern.itemText(pattern_index))
        self._ui.cmb_bayer_pattern.setCurrentIndex(self._ui.cmb_bayer_pattern.findData(config.get_bayer_pattern()))

        self._ui.ln_scan_folder_path.setText(config.get_scan_folder_path())
        self._ui.ln_scan_folder_path.setToolTip(config.get_scan_folder_path())

        self._ui.ln_work_folder_path.setText(config.get_work_folder_path())
        self._ui.ln_work_folder_path.setToolTip(config.get_work_folder_path())

        self._ui.ln_web_folder_path.setText(config.get_web_folder_path())
        self._ui.ln_web_folder_path.setToolTip(config.get_web_folder_path())

        self._ui.ln_master_dark_path.setText(config.get_master_dark_file_path())
        self._ui.ln_master_dark_path.setToolTip(config.get_master_dark_file_path())

        self._ui.ln_master_flat_path.setText(config.get_master_flat_file_path())
        self._ui.ln_master_flat_path.setToolTip(config.get_master_flat_file_path())

        self._ui.ln_web_server_port.setText(str(config.get_www_server_port_number()))
        self._populate_web_server_address_dropdown()
        self._ui.chk_debug_logs.setChecked(config.is_debug_log_on())
        self._ui.chk_use_dark.setChecked(config.get_use_master_dark())
        self._ui.chk_use_flat.setChecked(config.get_use_master_flat())
        self._ui.chk_use_hpr.setChecked(config.get_hot_pixel_remover())
        self._ui.chk_save_on_stop.setChecked(config.get_save_on_stop())

        config_to_image_save_type_mapping = {

            als.model.data.IMAGE_SAVE_TYPE_JPEG: self._ui.radioSaveJpeg,
            als.model.data.IMAGE_SAVE_TYPE_PNG:  self._ui.radioSavePng,
            als.model.data.IMAGE_SAVE_TYPE_TIFF: self._ui.radioSaveTiff
        }

        config_to_image_save_type_mapping[config.get_image_save_format()].setChecked(True)

        self._profile_config_mapping = {

            0: self._ui.rd_visual_profile,
            1: self._ui.rd_photo_profile
        }

        for k, v in self._profile_config_mapping.items():
            v.setChecked(config.get_profile() == k)

        self._ui.chk_www_own_folder.setChecked(config.get_www_use_dedicated_folder())

        self._web_folder_controls = [self._ui.ln_web_folder_path,
                                     self._ui.btn_browse_web]

        for control in self._web_folder_controls:
            control.setVisible(self._ui.chk_www_own_folder.isChecked())

        self._validate_all_paths()

        self._ui.sld_mem_preserve.setValue(config.get_preserved_mem())

        self._ui.chk_stats.setChecked(config.get_send_stats_active())

    @log
    def _validate_all_paths(self):
        """
        Draw a red border around text fields containing a path to a missing folder
        """

        path_labels_to_check = [self._ui.ln_work_folder_path, self._ui.ln_scan_folder_path]

        if self._ui.chk_www_own_folder.isChecked():
            path_labels_to_check.append(self._ui.ln_web_folder_path)

        for path_label in path_labels_to_check:

            label_text = path_label.text()

            if not label_text or not Path(label_text).is_dir():
                path_label.setStyleSheet(_WARNING_STYLE_SHEET)
            else:
                path_label.setStyleSheet(_NORMAL_STYLE_SHEET)

        master_dark_path = self._ui.ln_master_dark_path.text()
        if (Path(master_dark_path).is_file() or
                (not master_dark_path and not self._ui.chk_use_dark.isChecked())):
            self._ui.ln_master_dark_path.setStyleSheet(_NORMAL_STYLE_SHEET)
        else:
            self._ui.ln_master_dark_path.setStyleSheet(_WARNING_STYLE_SHEET)

        master_flat_path = self._ui.ln_master_flat_path.text()
        if (Path(master_flat_path).is_file() or
                (not master_flat_path and not self._ui.chk_use_flat.isChecked())):
            self._ui.ln_master_flat_path.setStyleSheet(_NORMAL_STYLE_SHEET)
        else:
            self._ui.ln_master_flat_path.setStyleSheet(_WARNING_STYLE_SHEET)

    @log
    def on_chk_use_dark_toggled(self, _):
        """
        Triggers config values validation when chk_use_dark is toggled

        :param _: well, you know, we really don't care. This the method we call that will check this
        """
        self._validate_all_paths()

    @log
    def on_chk_use_flat_toggled(self, _):
        """
        Triggers config values validation when chk_use_flat is toggled

        :param _: well, you know, we really don't care. This the method we call that will check this
        """
        self._validate_all_paths()

    @log
    @pyqtSlot(bool)
    def on_chk_www_own_folder_clicked(self, checked):
        """
        Hides web folder setting controls if server does not use dedicated folder

        :param checked: is 'use dedicated folder' box checked ?
        :type checked: bool
        """
        for control in self._web_folder_controls:
            control.setVisible(checked)

    @log
    def on_ln_scan_folder_path_textChanged(self, text):
        """
        Qt signal for scan folder path widget text changed
        :param text: new scan folder path
        :type text: str
        """
        self._ui.ln_scan_folder_path.setToolTip(text)

    @log
    def on_ln_work_folder_path_textChanged(self, text):
        """
        Qt signal for work folder path widget text changed
        :param text: new work folder path
        :type text: str
        """
        self._ui.ln_work_folder_path.setToolTip(text)

    @log
    def on_ln_web_folder_path_textChanged(self, text):
        """
        Qt signal for web folder path widget text changed
        :param text: new web folder path
        :type text: str
        """
        self._ui.ln_web_folder_path.setToolTip(text)

    @log
    def on_ln_master_dark_path_textChanged(self, text):
        """
        Qt signal for master dark path widget text changed
        :param text: new master dark path
        :type text: str
        """
        self._ui.ln_master_dark_path.setToolTip(text)

    @log
    def on_ln_master_flat_path_textChanged(self, text):
        """
        Qt signal for master flat path widget text changed
        :param text: new master flat path
        :type text: str
        """
        self._ui.ln_master_flat_path.setToolTip(text)

    @log
    @pyqtSlot()
    def accept(self):

        # prepare flags for settings that require restart to take effect
        PROFILE = self.tr("Profile")
        LOG = self.tr("Debug logs")
        LANG = self.tr("Language")

        settings_needing_restart = {
            PROFILE: False,
            LOG: False,
            LANG: False
        }

        """checks and stores user settings"""
        config.set_scan_folder_path(self._ui.ln_scan_folder_path.text())
        config.set_work_folder_path(self._ui.ln_work_folder_path.text())

        www_own_folder_is_checked = self._ui.chk_www_own_folder.isChecked()
        config.set_www_use_dedicated_folder(www_own_folder_is_checked)

        if www_own_folder_is_checked:
            web_folder_path = self._ui.ln_web_folder_path.text()
        else:
            web_folder_path = self._ui.ln_work_folder_path.text()

        config.set_web_folder_path(web_folder_path)

        web_server_port_number_str = self._ui.ln_web_server_port.text()

        config.set_use_master_dark(self._ui.chk_use_dark.isChecked())
        config.set_master_dark_file_path(self._ui.ln_master_dark_path.text())

        config.set_use_master_flat(self._ui.chk_use_flat.isChecked())
        config.set_master_flat_file_path(self._ui.ln_master_flat_path.text())

        config.set_hot_pixel_remover(self._ui.chk_use_hpr.isChecked())

        config.set_save_on_stop(self._ui.chk_save_on_stop.isChecked())

        if web_server_port_number_str.isdigit() and 1024 <= int(web_server_port_number_str) <= 65535:
            config.set_www_server_port_number(int(web_server_port_number_str))
        else:
            message = self.tr("Web server port number must be a number between 1024 and 65535")
            error_box(self.tr("Wrong value"), message)
            MESSAGE_HUB.dispatch_error(__name__, QT_TRANSLATE_NOOP("", "Port number validation failed : {}"), [message,])
            self._ui.ln_web_server_port.setFocus()
            self._ui.ln_web_server_port.selectAll()
            return
        config.set_www_server_advertised_address(
            self._ui.cmb_web_server_address.currentData())
        if DYNAMIC_DATA.web_server_status == WEB_SERVER_STATUS_RUNNING:
            Controller.update_web_server_advertised_address()

        # debug log choice
        debug_old_value = config.is_debug_log_on()
        debug_new_value = self._ui.chk_debug_logs.isChecked()
        if debug_new_value != debug_old_value:
            config.set_debug_log(debug_new_value)
            settings_needing_restart[LOG] = True

        image_save_type_to_config_mapping = {

            self._ui.radioSaveJpeg: als.model.data.IMAGE_SAVE_TYPE_JPEG,
            self._ui.radioSavePng: als.model.data.IMAGE_SAVE_TYPE_PNG,
            self._ui.radioSaveTiff: als.model.data.IMAGE_SAVE_TYPE_TIFF
        }

        for radio_button, image_save_type in image_save_type_to_config_mapping.items():
            if radio_button.isChecked():
                config.set_image_save_format(image_save_type)
                break

        # profile choice
        profile_old_value = config.get_profile()
        for k, v in self._profile_config_mapping.items():
            if v.isChecked():
                if k != profile_old_value:
                    settings_needing_restart[PROFILE] = True
                    config.set_profile(k)
                break

        # lang choice
        lang_old_value = config.get_lang()
        lang_new_value = self._ui.cmb_lang.currentData()

        if lang_new_value != lang_old_value:
            settings_needing_restart[LANG] = True
            config.set_lang(lang_new_value)

        config.set_bayer_pattern(self._ui.cmb_bayer_pattern.currentData())

        PreferencesDialog._save_config()

        if any(settings_needing_restart.values()):
            message = self.tr("You need to restart ALS for these changes to take effect :\n\n")
            for k, v in settings_needing_restart.items():
                message += f"* {k}\n" if v else ""
            message_box(self.tr("Restart needed"), message)

        config.set_preserved_mem(self._ui.sld_mem_preserve.value())

        config.set_send_stats_active(self._ui.chk_stats.isChecked())

        super().accept()



    @pyqtSlot(bool)
    @log
    def on_btn_browse_scan_clicked(self, checked: bool = False):
        """ Asks user to pick scan folder """
        scan_folder_path = ask_for_directory_path(self,
                                                  self.tr("Select scan folder"),
                                                  self._ui.ln_scan_folder_path.text())

        if scan_folder_path:
            self._ui.ln_scan_folder_path.setText(scan_folder_path)

        self._validate_all_paths()

    @pyqtSlot(bool)
    @log
    def on_btn_browse_work_clicked(self, checked: bool = False):
        """Opens a folder dialog to choose work folder"""
        work_folder_path = ask_for_directory_path(self,
                                                  self.tr("Select work folder"),
                                                  self._ui.ln_work_folder_path.text())
        if work_folder_path:
            self._ui.ln_work_folder_path.setText(work_folder_path)

        self._validate_all_paths()

    @pyqtSlot(bool)
    @log
    def on_btn_browse_web_clicked(self, checked: bool = False):
        """Opens a folder dialog to choose web folder"""
        web_folder_path = ask_for_directory_path(self,
                                                 self.tr("Select web folder"),
                                                 self._ui.ln_web_folder_path.text())
        if web_folder_path:
            self._ui.ln_web_folder_path.setText(web_folder_path)

        self._validate_all_paths()

    @pyqtSlot(bool)
    @log
    def on_btn_browse_dark_clicked(self, checked: bool = False):
        """Opens a folder dialog to choose dark file"""
        dark_file_path = QFileDialog.getOpenFileName(self,
                                                     self.tr("Select master dark file"),
                                                     self._ui.ln_master_dark_path.text(),
                                                     options=QFileDialog.DontUseNativeDialog)
        if dark_file_path[0]:
            self._ui.ln_master_dark_path.setText(dark_file_path[0])

        self._validate_all_paths()

    @pyqtSlot(bool)
    @log
    def on_btn_browse_flat_clicked(self, checked: bool = False):
        """Opens a folder dialog to choose flat file"""
        flat_file_path = QFileDialog.getOpenFileName(self,
                                                     self.tr("Select master flat file"),
                                                     self._ui.ln_master_flat_path.text(),
                                                     options=QFileDialog.DontUseNativeDialog)
        if flat_file_path[0]:
            self._ui.ln_master_flat_path.setText(flat_file_path[0])

        self._validate_all_paths()

    @staticmethod
    @log
    def _save_config():

        try:
            config.save()
        except config.CouldNotSaveConfig as save_error:
            error_box(save_error.message, f"Your settings could not be saved\n\nDetails : {save_error.details}")

    @log
    def _populate_web_server_address_dropdown(self) -> None:
        """
        Populates the persistent advertised-address dropdown.
        """
        current_preference = config.get_www_server_advertised_address()
        address_items = _address_preference_items(
            get_network_address_candidates(config.get_www_server_port_number()))

        self._ui.cmb_web_server_address.clear()
        for label, preference in address_items:
            self._ui.cmb_web_server_address.addItem(label, preference)

        selected_index = _address_preference_index(
            current_preference, address_items)
        self._ui.cmb_web_server_address.setCurrentIndex(selected_index)


class AboutDialog(QDialog):
    """
    Our about dialog box
    """

    @log
    def __init__(self, parent=None):
        super().__init__(parent)
        self._ui = Ui_AboutDialog()
        self._ui.setupUi(self)
        self._ui.lblVersionValue.setText(VERSION)
        self._ui.tabWidget.setCurrentIndex(0)


class SaveWaitDialog(QDialog):
    """
    Dialog shown while waiting for all pending image saves to complete
    """
    @log
    def __init__(self, controller: Controller, parent=None):
        super().__init__(parent)
        self._ui = Ui_SaveWaitDialog()
        self._ui.setupUi(self)

        self._controller = controller

        self.update_display(None)
        self._controller.add_model_observer(self)

    @log
    def update_display(self, _):
        """
        Update display
        """

        remaining_image_count = self.count_remaining_images()
        self._ui.lbl_remaining_saves.setText(str(remaining_image_count))

        if remaining_image_count == 0:
            self._controller.remove_model_observer(self)
            self.close()

    @log
    def count_remaining_images(self):
        """
        Count images that still need to be saved.

        We count 1 image to save for each image in the queues and each worker still Busy and also
        take 'save every image' setting and web server status into account

        :return: the number of images remaining to be saved
        :rtype: int
        """

        remaining_image_save_count = 0

        remaining_image_save_count += [

            DYNAMIC_DATA.pre_processor_busy,
            DYNAMIC_DATA.stacker_busy,
            DYNAMIC_DATA.post_processor_busy,

        ].count(True)

        for queue_size in [

                DYNAMIC_DATA.pre_process_queue.qsize(),
                DYNAMIC_DATA.stacker_queue.qsize(),
                DYNAMIC_DATA.process_queue.qsize(),
        ]:
            remaining_image_save_count += queue_size

        additional_saves_per_image = 1 if self._controller.get_save_every_image() else 0

        remaining_image_save_count *= 1 + additional_saves_per_image

        remaining_image_save_count += 1 if DYNAMIC_DATA.saver_busy else 0
        remaining_image_save_count += DYNAMIC_DATA.save_queue.qsize()

        return remaining_image_save_count

    @log
    @pyqtSlot()
    def on_btn_quit_clicked(self):
        """
        Qt slot called when user clicks 'Discard unsaved images and quit'
        """
        self.close()


class SessionStopDialog(QDialog):
    """
    confirm session stop
    """

    @log
    def __init__(self, parent=None):
        super().__init__(parent)
        self._ui = Ui_SessionStopDialog()
        self._ui.setupUi(self)
        self._ui.chk_save.setChecked(config.get_save_on_stop())

    @property
    def save_on_stop(self):
        """
        retrieves "save on stop" checkbox state

        :return: True if "save on stop" checkbox is checked, False otherwise
        :rtype: bool
        """
        return self._ui.chk_save.isChecked()


class QRDisplay(QDialog):

    visibility_changed_signal = pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.WindowDoesNotAcceptFocus)
        self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        self._ui = Ui_QrDialog()
        self._ui.setupUi(self)

        self.move(QApplication.desktop().screen().rect().center())

        self._geometry = self.geometry()

    @log
    def update_code(self):
        """
        Create a new QR code from the current runtime server URL.
        """
        if DYNAMIC_DATA.web_server_status == WEB_SERVER_STATUS_RUNNING:

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=7,
                border=1,
            )
            qr.add_data(DYNAMIC_DATA.web_server_advertised_url)
            qr.make(fit=True)
            img = qr.make_image()
            qim = ImageQt(img)
            pix = QPixmap.fromImage(qim)
            self._ui.lblQR.setPixmap(pix)
            self._ui.lblQR.adjustSize()
            self.adjustSize()

    @log
    def setVisible(self, visible: bool):
        """
        Set our visibility.

        :param visible: True if we must show ourself
        :type visible: bool
        """
        old_state = self.isVisible()
        if visible:
            self.setGeometry(self._geometry)
            self.update_code()
        else:
            self._geometry = self.geometry()

        if old_state != visible:
            self.visibility_changed_signal.emit(visible)

        super().setVisible(visible)


class FirstRunDialog(QDialog):
    """
    Displayed on first run, to let user choose between default config or custom config
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._ui = Ui_FirstRunDialog()
        self._ui.setupUi(self)
        self._ui.stackedWidget.setCurrentIndex(0)
        self._scan_folder_path = ""
        self._work_folder_path = ""
        self._scan_btn_default_text = self.tr("Select Scan folder...")
        self._work_btn_default_text = self.tr("Select Work folder...")
        self._ui.btn_scan.setText(self._scan_btn_default_text)
        self._ui.btn_work.setText(self._work_btn_default_text)

    @pyqtSlot(bool)
    def on_btn_no_config_clicked(self):
        """
        create default config

        Scan folder : als-scan on user desktop
        Work folder : als-work on user desktop
        """

        user_desktop = Path(QStandardPaths.writableLocation(QStandardPaths.DesktopLocation))
        default_scan_dir = user_desktop / "als-scan"
        default_work_dir = user_desktop / "als-work"

        try:
            mkdir(default_scan_dir, mode=0o755)
            mkdir(default_work_dir, mode=0o755)
        except FileExistsError:
            pass

        config.set_scan_folder_path(str(default_scan_dir))
        config.set_work_folder_path(str(default_work_dir))
        config.set_web_folder_path(str(default_work_dir))

        self.accept()

    @pyqtSlot(bool)
    def on_btn_go_clicked(self):
        """
        store configuration entries and closes dialog
        """
        config.set_scan_folder_path(str(self._scan_folder_path))
        config.set_work_folder_path(str(self._work_folder_path))
        config.set_web_folder_path(str(self._work_folder_path))
        self.accept()

    @pyqtSlot(bool)
    def on_btn_config_clicked(self):
        """
        displays custom config panel
        """
        self._ui.stackedWidget.setCurrentIndex(1)

    @pyqtSlot(bool)
    def on_btn_scan_clicked(self):
        """
        handle user choice of scan folder
        """
        self._scan_folder_path = ask_for_directory_path(self, self.tr("Select scan folder"))
        if Path(self._scan_folder_path).is_dir() and self._scan_folder_path != "":
            self._ui.btn_scan.setText(self._scan_folder_path)
        else:
            self._ui.btn_scan.setText(self._scan_btn_default_text)
        self._enable_go_button_if_folders_are_valid()

    @pyqtSlot(bool)
    def on_btn_work_clicked(self):
        """
        handle user choice of work folder
        """
        self._work_folder_path = ask_for_directory_path(self, self.tr("Select work folder"))
        if Path(self._work_folder_path).is_dir() and self._work_folder_path != "":
            self._ui.btn_work.setText(self._work_folder_path)
        else:
            self._ui.btn_work.setText(self._work_btn_default_text)
        self._enable_go_button_if_folders_are_valid()

    def _enable_go_button_if_folders_are_valid(self):
        """
        Enable "Go" button if both scan and work folder paths are set to existing folders
        """
        self._ui.btn_go.setEnabled(
            self._scan_folder_path != ""
            and self._work_folder_path != ""
            and Path(self._scan_folder_path).is_dir()
            and Path(self._work_folder_path).is_dir()
        )

@log
def _address_preference_items(candidates):
    """
    Builds persistent advertised-address dropdown items.

    :param candidates: network address candidates
    :return: list of label/preference tuples
    """
    address_items = [(I18n.AUTO_RECOMMENDED, ADVERTISED_ADDRESS_AUTO)]
    for candidate in candidates:
        address_items.append(
            (_address_candidate_label(candidate),
             build_advertised_address_preference(candidate.ip)))
    return address_items


@log
def _address_preference_index(preference, address_items) -> int:
    """
    Finds the dropdown index matching a persisted preference.

    :param preference: persisted advertised-address preference
    :param address_items: dropdown items
    :return: matching index or Auto index
    """
    for index, (_, item_preference) in enumerate(address_items):
        if item_preference == preference:
            return index
    return 0


@log
def _address_candidate_label(candidate) -> str:
    """
    Builds the translated UI label for a network address candidate.

    :param candidate: network address candidate
    :return: translated display label
    """
    if not candidate.interface_name:
        return "{} - {}".format(I18n.NETWORK_ADAPTER, candidate.ip)
    return candidate.label


@log
def _set_web_server_port_controls_enabled(ui, enabled: bool) -> None:
    """
    Enables or disables only the persistent web server port controls.

    :param ui: preferences dialog UI
    :param enabled: True when the port controls can be changed
    """
    ui.lbl_server_port.setEnabled(enabled)
    ui.ln_web_server_port.setEnabled(enabled)
    ui.label_4.setEnabled(enabled)


@log
def question(title, message, default_yes: bool = True):
    """
    Asks a question to user in a Qt MessageBox and return True/False as Yes/No

    :param title: Title of the box
    :param message: Message displayed in the box

    :param default_yes: set 'yes' button as the default button
    :type default_yes: bool

    :return: True if user replies "Yes", False otherwise
    """

    default_button = QMessageBox.Yes if default_yes else QMessageBox.No

    return QMessageBox.Yes == QMessageBox.question(
        QApplication.activeWindow(),
        title,
        message,
        QMessageBox.Yes | QMessageBox.No,
        default_button)


@log
def warning_box(title, message):
    """
    Displays a waring Qt MessageBox

    :param title: Title of the box
    :param message: Message displayed in the box
    :return: None
    """
    message_box('Warning : ' + title, message, QMessageBox.Warning)


@log
def error_box(title, message):
    """
    Displays an error Qt MessageBox

    :param title: Title of the box
    :param message: Message displayed in the box
    :return: None
    """
    message_box('Error : ' + title, message, QMessageBox.Critical)


@log
def message_box(title, message, icon=QMessageBox.Information):
    """
    Displays a Qt MessageBox with custom icon : Info by default

    :param title: Title of the box
    :param message: Message displayed in the box
    :param icon: The icon to show
    :return: None
    """
    box = QMessageBox()
    box.setIcon(icon)
    box.setWindowTitle(title)
    box.setText(message)
    box.exec()


@log
def ask_for_directory_path(parent, invite, start_folder= ""):
    """
    open a dialog box for the user to choose a directory path

    :param parent: parent Qt Widget
    :type parent: QWidget

    :param invite: title of the dialog box
    :type invite: str

    :param start_folder: folder in which dialog box is opened
    :type start_folder: str

    :return: the folder path chose by the user
    :rtype: str
    """
    if not start_folder:
        start_folder = QStandardPaths.writableLocation(QStandardPaths.HomeLocation)

    return QFileDialog.getExistingDirectory(parent,
                                            invite,
                                            start_folder,
                                            options=QFileDialog.DontUseNativeDialog | QFileDialog.ShowDirsOnly)