# SPDX-FileCopyrightText: 2019-2026 The ALS Authors
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Main module, basically in charge of application init / start
"""
import argparse
import os
import platform
import socket
import sys
from logging import getLogger

from PyQt5.QtCore import QLocale, QTranslator, QT_TRANSLATE_NOOP, QThread, Qt
from PyQt5.QtWidgets import QApplication, QDialog

from als import config
from als.code_utilities import Timer, human_readable_byte_size, available_memory, AlsLogAdapter, log, \
    get_text_content_of_resource
from als.logic import Controller
from als.messaging import MESSAGE_HUB
from als.model.data import I18n, VERSION, DYNAMIC_DATA
from als.ui.dialogs import FirstRunDialog
from als.ui.platform_ui import install_windows_title_bar_styling
from als.ui.windows import MainWindow

_LOGGER = AlsLogAdapter(getLogger(__name__), {})

SUPPORTED_LANGUAGES = {"en", "fr", "ru"}


def log_system_infos():
    """
    Log detailed info about current running system
    """
    python_version = sys.version.replace('\n', '')

    _LOGGER.debug("***************************************************************************")
    _LOGGER.debug('System info dump - START')
    _LOGGER.debug(f"Platform name         : {sys.platform}")
    _LOGGER.debug(f"Platform architecture : {platform.architecture()}")
    _LOGGER.debug(f"Machine name          : {platform.machine()}")
    _LOGGER.debug(f"CPU type              : {platform.processor()}")
    _LOGGER.debug(f"CPU count             : {os.cpu_count()}")
    _LOGGER.debug(f"OS name               : {platform.system()}")
    _LOGGER.debug(f"OS release            : {platform.release()}")
    _LOGGER.debug(f"Available memory      : {human_readable_byte_size(available_memory())}")
    _LOGGER.debug(f"Python version        : {python_version}")
    _LOGGER.debug('System info dump - END')
    _LOGGER.debug("***************************************************************************")


def call_home():
    """
    Make app send a ping to ALS team to let us know that the app is being used.

    This is used to gather anonymous usage statistics and help us make informed decisions about future development.
    The ping includes:
    - the app version
    - the machine architecture
    - the operating system
    No personally identifiable information is sent.

    Info is sent using UDP protocol, to be lightweight and fast.

    We purposefuly ignore all errors that may occur during this process, as we don't want to impact user experience
    in any way if something goes wrong (e.g. no network connection, firewall blocking the ping, etc.).

    If we get the data, great. If we don't, so be it.
    """
    home_host = "ping.als-app.org"
    home_port = 16810

    try:
        home_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        message = f"{VERSION}||{platform.machine()}||{platform.system()}"
        home_socket.sendto(message.encode(), (home_host, home_port))
        home_socket.close()
    except socket.error:
        pass

CONTINUE_STARTUP = "continue"
STOP_STARTUP = "stop"

# pylint: disable=R0914
def main():
    """
    Runs ALS
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-s",
                        "--start_session",
                        help="Start session on application startup",
                        action="store_true")

    parser.add_argument("-w",
                        "--start_server",
                        help="Start web server on application startup",
                        action="store_true")

    parser.add_argument('-l',
                        '--lang',
                        help='Select application language',
                        choices=['sys', 'en', 'fr', 'ru'],
                        dest="lang",
                        default="")

    args = parser.parse_args()

    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    with Timer() as startup_timer:

        config.setup()
        log_system_infos()

        app = QApplication(sys.argv)
        QThread.currentThread().setPriority(QThread.TimeCriticalPriority)

        setup_ui_styling(app)

        # Translators must stay referenced while the app lives.
        # This assignment looks unused, but removing it breaks .ui translations.
        translators = setup_i18n(app, args.lang)

        if do_first_run_setup_if_needed() == STOP_STARTUP:
            return

        _LOGGER.debug("Building and showing main window")
        controller = Controller()
        window = MainWindow(controller)

        window.reset_image_view()

        if args.start_session:
            controller.start_session()

        if args.start_server:
            controller.start_www()

    start_message = QT_TRANSLATE_NOOP("", "Astro Live Stacker version {} started in {} ms.")
    start_message_values = [VERSION, startup_timer.elapsed_in_milli_as_str]
    MESSAGE_HUB.dispatch_info(__name__, start_message, start_message_values)

    if config.get_send_stats_active():
        call_home()

    app_return_code = app.exec()
    controller.shutdown()

    _LOGGER.info(f"Astro Live Stacker terminated with return code = {app_return_code}")

    sys.exit(app_return_code)


def _detect_system_language() -> str:
    """
    Detect the first system UI language supported by ALS.
    """
    system_languages = QLocale.system().uiLanguages()
    _LOGGER.debug("System UI languages = %s", system_languages)

    for locale_name in system_languages:
        language = locale_name.replace("_", "-").split("-")[0].lower()
        if language in SUPPORTED_LANGUAGES:
            return language

    return "en"


@log
def setup_ui_styling(app: QApplication):
    """Apply shared and platform-specific application styling."""

    style_sheet = get_text_content_of_resource(":/main/dark.css")
    _LOGGER.debug("loaded shared application stylesheet")

    if sys.platform == "darwin":
        style_sheet += "\n" + get_text_content_of_resource(":/main/dark-macos.css")
        _LOGGER.debug("appended macOS specific stylesheet")

    elif sys.platform == "win32":
        default_font = app.font()
        default_font.setPointSize(default_font.pointSize() + 1)
        app.setFont(default_font)
        style_sheet += "\n" + get_text_content_of_resource(":/main/dark-windows.css")
        install_windows_title_bar_styling(app)
        _LOGGER.debug("appended Windows specific stylesheet and installed title bar styling")

    app.setStyleSheet(style_sheet)
    _LOGGER.debug("composite stylesheet applied to application")


def setup_i18n(app: QApplication, lang: str = "") -> list:
    """
    Setup i18n for the all application

    - install translators for Qt Base & application text according to user config or CLI
    - initialize our I18n tool

    if CLI param is used, user config is ignored

    If user config asks for ALS to use system locale and we fail to detect system locale,
    fallback to english

    :param app: the to install translators into
    :type app: QApplication

    :parm lang: code of language to use for translations
    accepted values :
    - "fr"
    - "en"
    - "ru"
    - "sys" (to use system locale)
    - empty string to use application prefs
    :type lang: str

    :return: list of loaded translators
    list is empty if effective lang (via lang or app prefs) is 'en'
    :rtype: list
    """

    _LOGGER.debug("command line language choice = %s", lang)
    _LOGGER.debug("config language choice = %s", config.get_lang())

    lang_choice = lang or config.get_lang()
    effective_lang = lang_choice
    translators = list()

    if lang_choice == 'sys':
        effective_lang = _detect_system_language()
        _LOGGER.debug("Selected system language = %s", effective_lang)

    if effective_lang != "en":

        for app_component in ["als", "qtbase"]:
            i18n_file_name = f'{app_component}_{effective_lang}'
            translator = QTranslator()
            if translator.load(f":/i18n/{i18n_file_name}.qm"):
                _LOGGER.debug(f"Successfully loaded {i18n_file_name} translator")
                translator.setObjectName(i18n_file_name)
                translators.append(translator)

        for translator in translators:
            if app.installTranslator(translator):
                _LOGGER.debug(f"Successfully installed {translator.objectName()} translator")

    I18n().setup()

    return translators

@log
def do_first_run_setup_if_needed():
    """
    Detect if this is the first run of ALS and display the FTUE dialog in that case

    :return: whether to continue startup or not :
             - CONTINUE_STARTUP: setup completed by user, or not a first run
             - STOP_STARTUP: firt run and user chose to quit during setup
    :rtype: str
    """
    if not DYNAMIC_DATA.is_first_run:
        _LOGGER.debug("Not a first run. Continuing startup")
        return CONTINUE_STARTUP

    _LOGGER.info("First run detected. Launching first run setup dialog")
    if FirstRunDialog().exec_() == QDialog.Accepted:
        _LOGGER.debug("First run setup completed successfully. Continuing startup")
        return CONTINUE_STARTUP

    _LOGGER.info("First run setup was not completed. Stopping startup")
    return STOP_STARTUP


if __name__ == "__main__":
    main()
