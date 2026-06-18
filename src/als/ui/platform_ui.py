# SPDX-FileCopyrightText: 2019-2026 The ALS Authors
# SPDX-License-Identifier: GPL-3.0-or-later

"""Apply platform-specific UI adjustments."""

import ctypes
import platform
import sys

from PyQt5.QtCore import QEvent, QObject, QRect, QSize, Qt
from PyQt5.QtGui import QColor, QFontDatabase, QIcon, QPalette
from PyQt5.QtWidgets import (
    QAbstractSlider,
    QApplication,
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFrame,
    QGroupBox,
    QLabel,
    QMenu,
    QMenuBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QStatusBar,
    QStyle,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QWidget,
    QTabBar)

_WINDOWS_COMBO_BOX_ITEM_SPACING = 4
_MACOS_COMBO_BOX_POPUP_HORIZONTAL_PADDING = 12
_MACOS_SLIDER_WHEEL_STEP_MULTIPLIER = 2
_file_dialog_focus_highlight_styler = None

_PREFERRED_FIXED_PITCH_FONT_FAMILIES = (
    "Monospace",
    "DejaVu Sans Mono",
    "Liberation Mono",
    "Noto Mono",
    "Ubuntu Mono",
    "Courier 10 Pitch",
    "Courier",
)


def configure_platform_ui(parent: QWidget, session_log=None):
    """Apply platform-specific adjustments to a newly built UI."""

    _add_current_item_feedback_to_combo_boxes(parent)
    _hide_preferences_focus_highlight(parent)
    _configure_menu(parent)
    _hide_file_dialog_focus_highlight()

    if sys.platform == "darwin":
        _fit_combo_box_popups_to_their_contents(parent)
        _enable_macos_slider_wheel_events(parent)

    if sys.platform == "win32":
        _add_spacing_to_combo_box_items(parent)

    _remove_native_status_bar_cell_frames(parent)

    if session_log is not None:
        configure_session_log_font(session_log)


def _hide_preferences_focus_highlight(parent):

    focus_highlight_control_types = (
        QPushButton,
        QRadioButton,
        QCheckBox,
        QTabBar

    )
    for control_type in focus_highlight_control_types:
        for control in parent.findChildren(control_type):
            _hide_system_overlay(control)


def _configure_menu(parent):

    for menu_bar in parent.findChildren(QMenuBar):
        _hide_system_overlay(menu_bar)

    for menu in parent.findChildren(QMenu):
        _hide_system_overlay(menu)


def _hide_file_dialog_focus_highlight():

    global _file_dialog_focus_highlight_styler

    app = QApplication.instance()

    if app is None or _file_dialog_focus_highlight_styler is not None:
        return

    _file_dialog_focus_highlight_styler = _FileDialogFocusHighlightRemover()

    app.installEventFilter(_file_dialog_focus_highlight_styler)
    app.aboutToQuit.connect(_teardown_file_dialog_focus_highlight_styling)


def _teardown_file_dialog_focus_highlight_styling():

    global _file_dialog_focus_highlight_styler

    app = QApplication.instance()
    if app is not None and _file_dialog_focus_highlight_styler is not None:
        app.removeEventFilter(_file_dialog_focus_highlight_styler)

    _file_dialog_focus_highlight_styler = None


def _hide_system_overlay(control):
    control_palette = control.palette()
    control_palette.setColor(QPalette.Highlight, QColor("#222222"))
    control.setPalette(control_palette)


def _add_current_item_feedback_to_combo_boxes(parent):
    for combo_box in parent.findChildren(QComboBox):
        combo_box.setItemDelegate(_ComboBoxPopupDelegate(combo_box))


def _fit_combo_box_popups_to_their_contents(parent):
    for combo_box in parent.findChildren(QComboBox):
        popup_view = combo_box.view()
        content_width = popup_view.sizeHintForColumn(
            combo_box.modelColumn()
        )
        if content_width > 0:
            popup_view.setMinimumWidth(
                content_width
                + popup_view.frameWidth() * 2
                + _MACOS_COMBO_BOX_POPUP_HORIZONTAL_PADDING
            )


def _enable_macos_slider_wheel_events(parent):
    wheel_handler = _MacOSSliderWheelHandler(parent)
    for slider in parent.findChildren(QSlider):
        slider.installEventFilter(wheel_handler)
    parent._als_macos_slider_wheel_handler = wheel_handler


def _add_spacing_to_combo_box_items(parent):
    for combo_box in parent.findChildren(QComboBox):
        combo_box.view().setSpacing(_WINDOWS_COMBO_BOX_ITEM_SPACING)


def _remove_native_status_bar_cell_frames(parent):
    for status_bar in parent.findChildren(QStatusBar):
        for label in status_bar.findChildren(QLabel):
            label.setFrameStyle(QFrame.NoFrame)


def configure_session_log_font(session_log):
    if sys.platform in ("darwin", "win32"):
        log_font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        log_font.setPointSize(session_log.font().pointSize())
        session_log.setFont(log_font)
        return

    if platform.machine().strip().lower() != "aarch64":
        return

    font_database = QFontDatabase()
    log_font_family = _find_fixed_pitch_font_family(font_database)
    if log_font_family is None:
        return

    log_font = session_log.font()
    log_font.setFamily(log_font_family)
    session_log.setFont(log_font)


def _find_fixed_pitch_font_family(font_database):
    available_families = set(font_database.families())

    for family in _PREFERRED_FIXED_PITCH_FONT_FAMILIES:
        if (
                family in available_families
                and font_database.isFixedPitch(family)):
            return family

    return None


class _FileDialogFocusHighlightRemover(QObject):
    """Neutralize native focus overlays on Qt file-dialog buttons."""

    def eventFilter(self, watched, event):
        if (
                isinstance(watched, QFileDialog)
                and event.type() == QEvent.Show):
            for button in watched.findChildren(QPushButton):
                _hide_system_overlay(button)

        return False


class _MacOSSliderWheelHandler(QObject):
    """Apply mouse-wheel changes that macOS does not deliver to sliders."""

    def eventFilter(self, watched, event):
        if (
                isinstance(watched, QSlider)
                and event.type() == QEvent.Wheel):
            wheel_delta = event.angleDelta().y()
            if wheel_delta == 0:
                wheel_delta = event.pixelDelta().y()
            if wheel_delta == 0:
                return False

            direction = 1 if wheel_delta > 0 else -1
            if event.inverted():
                direction *= -1
            if watched.invertedControls():
                direction *= -1

            action = (
                QAbstractSlider.SliderSingleStepAdd
                if direction > 0
                else QAbstractSlider.SliderSingleStepSub
            )
            for _ in range(_MACOS_SLIDER_WHEEL_STEP_MULTIPLIER):
                watched.triggerAction(action)
            event.accept()
            return True

        return False



###################################################################################################
### Combobox popup menu styling


class _ComboBoxPopupDelegate(QStyledItemDelegate):
    """Draw a check marker beside the combo box's current popup item."""

    _MARKER_SIZE = 18
    _MARKER_LEFT_MARGIN = 4
    _TEXT_LEFT_MARGIN = 4
    _TEXT_RIGHT_MARGIN = 4

    def __init__(self, combo_box):
        super().__init__(combo_box)
        self._combo_box = combo_box
        self._marker = QIcon(":icons/tick-dark.svg")

    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        reserved_width = (
            self._MARKER_LEFT_MARGIN
            + self._MARKER_SIZE
            + self._TEXT_LEFT_MARGIN
        )
        return QSize(
            size.width() + reserved_width,
            max(size.height(), self._MARKER_SIZE)
        )

    def paint(self, painter, option, index):
        item_option = QStyleOptionViewItem(option)
        self.initStyleOption(item_option, index)
        is_hovered = bool(item_option.state & QStyle.State_MouseOver)
        is_selected = bool(item_option.state & QStyle.State_Selected)
        item_option.state &= ~(
            QStyle.State_HasFocus
            | QStyle.State_MouseOver
            | QStyle.State_Selected
        )
        item_option.palette.setColor(QPalette.Highlight, QColor("#454545"))
        item_text = item_option.text
        item_option.text = ""
        item_option.icon = QIcon()
        item_option.features &= ~QStyleOptionViewItem.HasDecoration

        style = (
            item_option.widget.style()
            if item_option.widget is not None
            else QApplication.style()
        )

        style.drawControl(
            QStyle.CE_ItemViewItem,
            item_option,
            painter,
            item_option.widget
        )
        if is_hovered or is_selected:
            painter.fillRect(item_option.rect, QColor("#454545"))

        marker_rect = QRect(
            item_option.rect.left() + self._MARKER_LEFT_MARGIN,
            item_option.rect.top()
            + (item_option.rect.height() - self._MARKER_SIZE) // 2,
            self._MARKER_SIZE,
            self._MARKER_SIZE
        )
        if index.row() == self._combo_box.currentIndex():
            self._marker.paint(painter, marker_rect)

        text_rect = item_option.rect.adjusted(
            self._MARKER_LEFT_MARGIN
            + self._MARKER_SIZE
            + self._TEXT_LEFT_MARGIN,
            0,
            -self._TEXT_RIGHT_MARGIN,
            0
        )
        elided_text = item_option.fontMetrics.elidedText(
            item_text,
            Qt.ElideRight,
            text_rect.width()
        )
        text_role = (
            QPalette.HighlightedText
            if is_hovered or is_selected
            else QPalette.Text
        )
        style.drawItemText(
            painter,
            text_rect,
            Qt.AlignLeft | Qt.AlignVCenter,
            item_option.palette,
            bool(item_option.state & QStyle.State_Enabled),
            elided_text,
            text_role
        )



###################################################################################################
### Windows title bar styling

_WINDOWS_11_MINIMUM_BUILD = 22000
_WINDOWS_BORDER_COLOR = 0x444444
_WINDOWS_CAPTION_COLOR = 0x333333
_WINDOWS_TEXT_COLOR = 0xB6B6B6

_DWMWA_USE_IMMERSIVE_DARK_MODE = 20
_DWMWA_BORDER_COLOR = 34
_DWMWA_CAPTION_COLOR = 35
_DWMWA_TEXT_COLOR = 36

class _WindowsTitleBarStyler(QObject):
    """Apply native dark title-bar colors when Qt creates a window."""


    def __init__(self, parent=None):
        super().__init__(parent)
        self._widgets_being_styled = set()
        self._supports_custom_colors = (
            sys.getwindowsversion().build >= _WINDOWS_11_MINIMUM_BUILD
        )
        self._set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
        self._set_window_attribute.argtypes = (
            ctypes.c_void_p,
            ctypes.c_uint32,
            ctypes.c_void_p,
            ctypes.c_uint32,
        )
        self._set_window_attribute.restype = ctypes.c_long

    def eventFilter(self, watched, event):
        if (
                isinstance(watched, QWidget)
                and watched.isWindow()
                and event.type() in (QEvent.Show, QEvent.WinIdChange)):
            self._apply_title_bar_colors(watched)

        return False

    @staticmethod
    def _build_color_ref(rgb_color):
        red = (rgb_color >> 16) & 0xFF
        green = (rgb_color >> 8) & 0xFF
        blue = rgb_color & 0xFF
        return red | (green << 8) | (blue << 16)

    def _apply_title_bar_colors(self, widget):
        widget_id = id(widget)
        if widget_id in self._widgets_being_styled:
            return

        self._widgets_being_styled.add(widget_id)
        try:
            native_window_id = widget.winId()
            if native_window_id is None:
                return

            window_handle = int(native_window_id)
            self._set_attribute(
                window_handle,
                _DWMWA_USE_IMMERSIVE_DARK_MODE,
                1
            )

            if not self._supports_custom_colors:
                return

            self._set_attribute(
                window_handle,
                _DWMWA_BORDER_COLOR,
                self._build_color_ref(_WINDOWS_BORDER_COLOR)
            )
            self._set_attribute(
                window_handle,
                _DWMWA_CAPTION_COLOR,
                self._build_color_ref(_WINDOWS_CAPTION_COLOR)
            )
            self._set_attribute(
                window_handle,
                _DWMWA_TEXT_COLOR,
                self._build_color_ref(_WINDOWS_TEXT_COLOR)
            )
        finally:
            self._widgets_being_styled.remove(widget_id)

    def _set_attribute(self, window_handle, attribute, raw_value):
        value = ctypes.c_uint32(raw_value)
        self._set_window_attribute(
            window_handle,
            attribute,
            ctypes.byref(value),
            ctypes.sizeof(value)
        )


def install_windows_title_bar_styling(app):
    """Style every native top-level window created by the application."""

    if sys.platform != "win32":
        return

    title_bar_styler = _WindowsTitleBarStyler(app)
    app.installEventFilter(title_bar_styler)
    app._als_windows_title_bar_styler = title_bar_styler

def set_groupbox_spacing(groupbox: QGroupBox):

    if sys.platform == "darwin":
        groupbox.layout().setSpacing(8)
        groupbox.layout().setContentsMargins(10, 8, 10, 8)
