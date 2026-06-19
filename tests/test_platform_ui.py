from PyQt5.QtWidgets import QFileDialog

from als.ui import platform_ui


def _uses_non_native_dialog(options):
    return bool(options & QFileDialog.DontUseNativeDialog)


def test_given_linux_when_file_dialog_options_are_built_then_non_native_dialog_is_used(monkeypatch):
    monkeypatch.setattr(platform_ui.sys, "platform", "linux")

    options = platform_ui.build_file_dialog_options()

    assert _uses_non_native_dialog(options)


def test_given_macos_when_file_dialog_options_are_built_then_native_dialog_is_used(monkeypatch):
    monkeypatch.setattr(platform_ui.sys, "platform", "darwin")

    options = platform_ui.build_file_dialog_options()

    assert not _uses_non_native_dialog(options)


def test_given_windows_when_file_dialog_options_are_built_then_native_dialog_is_used(monkeypatch):
    monkeypatch.setattr(platform_ui.sys, "platform", "win32")

    options = platform_ui.build_file_dialog_options()

    assert not _uses_non_native_dialog(options)


def test_given_directory_dialog_options_when_built_then_directories_only_are_shown(monkeypatch):
    monkeypatch.setattr(platform_ui.sys, "platform", "darwin")

    options = platform_ui.build_directory_dialog_options()

    assert options & QFileDialog.ShowDirsOnly
