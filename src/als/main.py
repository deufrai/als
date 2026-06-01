"""
Main module, basically in charge of application init / start
"""
import argparse
import os
import platform
import socket
import sys
from locale import getlocale
from logging import getLogger

from PyQt5.QtCore import QTranslator, QT_TRANSLATE_NOOP, QThread, Qt
from PyQt5.QtWidgets import QApplication

from als import config
from als.code_utilities import Timer, human_readable_byte_size, available_memory, AlsLogAdapter, log
from als.logic import Controller
from als.messaging import MESSAGE_HUB
from als.model.data import I18n, VERSION
from als.ui.windows import MainWindow

_LOGGER = AlsLogAdapter(getLogger(__name__), {})


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

    args = parser.parse_args()

    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    with Timer() as startup_timer:

        app = QApplication(sys.argv)
        QThread.currentThread().setPriority(QThread.TimeCriticalPriority)
        config.setup()
        log_system_infos()
        setup_i18n(app)

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

@log
def setup_i18n(app: QApplication):
    """
    Setup i18n for the all application

    - install translators for Qt Base & application text according to user config
    - initialize our I18n tool

    If user config asks for ALS to use system locale and we fail to detect system locale,
    fallback to english

    :param app: the to install translators into
    :type app: QApplication
    """
    lang_choice = config.get_lang()
    effective_lang = lang_choice

    if lang_choice == 'sys':
        try:
            system_locale = getlocale()[0]
            if system_locale is None:
                raise ValueError()
            effective_lang = system_locale.split('_')[0]
            _LOGGER.debug(f"System locale = {effective_lang}")

        except (ValueError, IndexError):
            _LOGGER.warning("Failed to detect system locale. Falling back to english")
            effective_lang = "en"

    if effective_lang != "en":

        translators = list()

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


if __name__ == "__main__":
    main()
