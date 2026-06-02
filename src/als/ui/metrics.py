"""
Live metrics UI.
"""
import datetime

from PyQt5.QtCore import Qt, pyqtSignal, QRectF
from PyQt5.QtGui import QColor, QPainter, QPen, QBrush, QFontMetrics
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QWidget, QScrollArea, QToolButton

from als.code_utilities import log
from als.model.metrics import LiveMetrics, SystemMetrics


class LiveMetricsWindow(QDialog):
    """
    Tool window showing live metrics.
    """

    visibility_changed_signal = pyqtSignal(bool)

    @log
    def __init__(self, live_metrics: LiveMetrics, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.Tool)
        self.setWindowTitle(self.tr("Session metrics"))
        self.resize(1000, 700)

        self._system_metrics = live_metrics.get_system_metrics()
        self._geometry = self.geometry()

        layout = QVBoxLayout(self)
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        content = QWidget(scroll_area)
        self._content_layout = QVBoxLayout(content)
        scroll_area.setWidget(content)

        self._system_widgets = list()
        self._build_system_section()
        self._content_layout.addStretch()

        self._system_metrics.updated_signal.connect(self.update_display)
        self.update_display()

    @log
    def _build_system_section(self) -> None:
        """
        Builds the system metrics section.
        """
        section = CollapsibleSection(self.tr("System"), self)
        self._system_section = section
        section.expanded_signal[bool].connect(self.on_system_section_expanded)
        self._content_layout.addWidget(section)

        memory_widget = MemoryTimelineWidget(
            self._system_metrics,
            self.tr("Memory"),
            self.tr("Available"),
            self.tr("Preserved"),
            self)
        self._system_widgets.append(memory_widget)
        section.add_widget(memory_widget)

        for worker_name in SystemMetrics.WORKER_NAMES:
            worker_widget = WorkerTimelineWidget(
                self._system_metrics,
                worker_name,
                self._get_worker_label(worker_name),
                self)
            self._system_widgets.append(worker_widget)
            section.add_widget(worker_widget)

    @log
    def _get_worker_label(self, worker_name: str) -> str:
        """
        Gets the display label for a worker.

        :param worker_name: worker name
        :return: localized worker label
        """
        worker_labels = {
            SystemMetrics.WORKER_PRE_PROCESS: self.tr("Pre-process"),
            SystemMetrics.WORKER_STACKER: self.tr("Stacker"),
            SystemMetrics.WORKER_POST_PROCESS: self.tr("Post-process"),
            SystemMetrics.WORKER_SAVE: self.tr("Saver"),
        }
        return worker_labels[worker_name]

    @log
    def update_display(self) -> None:
        """
        Updates plots from current metrics.
        """
        if not self._system_section.is_expanded():
            return

        start_time, end_time = self._system_metrics.get_time_range()
        for widget in self._system_widgets:
            widget.set_time_range(start_time, end_time)
            widget.update()

    @log
    def on_system_section_expanded(self, expanded: bool) -> None:
        """
        System section expansion changed.

        :param expanded: True when section is expanded
        """
        if expanded:
            self.update_display()

    @log
    def setVisible(self, visible: bool):
        """
        Set our visibility.

        :param visible: True if window must be shown
        """
        old_state = self.isVisible()
        if visible:
            self.setGeometry(self._geometry)
            self.update_display()
        else:
            self._geometry = self.geometry()

        if old_state != visible:
            self.visibility_changed_signal.emit(visible)

        super().setVisible(visible)


class TimelineWidget(QWidget):
    """
    Base widget for timestamp-aligned metrics timelines.
    """

    _LEFT_MARGIN = 74
    _RIGHT_MARGIN = 16
    _TOP_MARGIN = 24
    _BOTTOM_MARGIN = 24

    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self._title = title
        self._start_time = 0
        self._end_time = 1
        self.setMinimumHeight(170)

    @log
    def set_time_range(self, start_time: float, end_time: float) -> None:
        """
        Sets the shared X-axis time range.

        :param start_time: minimum timestamp
        :param end_time: maximum timestamp
        """
        self._start_time = start_time
        self._end_time = max(end_time, start_time + 1)

    def _plot_rect(self):
        return self.rect().adjusted(
            self._LEFT_MARGIN,
            self._TOP_MARGIN,
            -self._RIGHT_MARGIN,
            -self._BOTTOM_MARGIN)

    def _timestamp_to_x(self, timestamp: float, plot_rect) -> int:
        span = max(self._end_time - self._start_time, 1)
        ratio = (timestamp - self._start_time) / span
        ratio = min(max(ratio, 0), 1)
        return int(plot_rect.left() + ratio * plot_rect.width())

    def _draw_frame(self, painter: QPainter, plot_rect) -> None:
        painter.setPen(QPen(QColor("#CCCCCC")))
        painter.drawRect(plot_rect)

        painter.setPen(QPen(QColor("#222222")))
        painter.drawText(8, 16, self._title)
        painter.drawText(
            plot_rect.left(),
            self.height() - 6,
            self._format_time(self._start_time))
        end_label = self._format_time(self._end_time)
        label_width = QFontMetrics(painter.font()).width(end_label)
        painter.drawText(
            plot_rect.right() - label_width,
            self.height() - 6,
            end_label)

    @staticmethod
    def _format_time(timestamp: float) -> str:
        return datetime.datetime.fromtimestamp(timestamp).strftime("%H:%M:%S")


class MemoryTimelineWidget(TimelineWidget):
    """
    Draws memory metrics.
    """

    def __init__(
            self,
            system_metrics: SystemMetrics,
            title: str,
            available_label: str,
            preserved_label: str,
            parent=None):
        super().__init__(title, parent)
        self._system_metrics = system_metrics
        self._available_label = available_label
        self._preserved_label = preserved_label

    def paintEvent(self, event):  # pylint: disable=unused-argument
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, False)
        plot_rect = self._plot_rect()
        self._draw_frame(painter, plot_rect)

        available_timestamps, available_values = self._system_metrics.get_available_memory_series()
        preserved_timestamps, preserved_values = self._system_metrics.get_preserved_memory_series()
        max_value = max(available_values + preserved_values + [1])

        self._draw_line(
            painter,
            plot_rect,
            available_timestamps,
            available_values,
            max_value,
            QColor("#3366CC"))
        self._draw_line(
            painter,
            plot_rect,
            preserved_timestamps,
            preserved_values,
            max_value,
            QColor("#CC3333"))
        self._draw_legend(painter, plot_rect)

    def _draw_line(self, painter, plot_rect, timestamps, values, max_value, color):
        if len(timestamps) < 2:
            return

        painter.setPen(QPen(color, 2))
        previous = None
        for timestamp, value in zip(timestamps, values):
            x_position = self._timestamp_to_x(timestamp, plot_rect)
            y_position = int(plot_rect.bottom() - (value / max_value) * plot_rect.height())
            current = (x_position, y_position)
            if previous is not None:
                painter.drawLine(previous[0], previous[1], current[0], current[1])
            previous = current

    def _draw_legend(self, painter, plot_rect) -> None:
        painter.setPen(QPen(QColor("#3366CC"), 2))
        painter.drawLine(plot_rect.left(), 20, plot_rect.left() + 18, 20)
        painter.setPen(QPen(QColor("#222222")))
        painter.drawText(plot_rect.left() + 24, 24, self._available_label)

        second_left = plot_rect.left() + 140
        painter.setPen(QPen(QColor("#CC3333"), 2))
        painter.drawLine(second_left, 20, second_left + 18, 20)
        painter.setPen(QPen(QColor("#222222")))
        painter.drawText(second_left + 24, 24, self._preserved_label)


class WorkerTimelineWidget(TimelineWidget):
    """
    Draws worker queue size and status metrics.
    """

    _STATUS_HEIGHT = 14

    def __init__(
            self,
            system_metrics: SystemMetrics,
            worker_name: str,
            worker_label: str,
            parent=None):
        super().__init__(worker_label, parent)
        self._system_metrics = system_metrics
        self._worker_name = worker_name

    def paintEvent(self, event):  # pylint: disable=unused-argument
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, False)
        plot_rect = self._plot_rect()
        self._draw_frame(painter, plot_rect)
        self._draw_status_intervals(painter, plot_rect)
        self._draw_queue_bars(painter, plot_rect)

    def _draw_status_intervals(self, painter: QPainter, plot_rect) -> None:
        timestamps, statuses = self._system_metrics.get_worker_status_series(self._worker_name)
        if not timestamps:
            return

        current_time = SystemMetrics.get_current_timestamp()
        status_top = plot_rect.top() + 4

        for index, timestamp in enumerate(timestamps):
            next_timestamp = timestamps[index + 1] if index + 1 < len(timestamps) else current_time
            left = self._timestamp_to_x(timestamp, plot_rect)
            right = max(self._timestamp_to_x(next_timestamp, plot_rect), left + 1)
            color = QColor("#33AA55") if statuses[index] else QColor("#CCCCCC")
            painter.fillRect(
                QRectF(left, status_top, right - left, self._STATUS_HEIGHT),
                QBrush(color))

    def _draw_queue_bars(self, painter: QPainter, plot_rect) -> None:
        timestamps, queue_sizes = self._system_metrics.get_queue_series(self._worker_name)
        if not timestamps:
            return

        max_queue_size = max(queue_sizes + [1])
        queue_top = plot_rect.top() + self._STATUS_HEIGHT + 10
        queue_height = max(plot_rect.bottom() - queue_top, 1)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor("#3366CC")))

        for index, timestamp in enumerate(timestamps):
            next_timestamp = (
                timestamps[index + 1]
                if index + 1 < len(timestamps)
                else self._end_time)
            left = self._timestamp_to_x(timestamp, plot_rect)
            right = max(self._timestamp_to_x(next_timestamp, plot_rect), left + 1)
            height = int((queue_sizes[index] / max_queue_size) * queue_height)
            painter.drawRect(left, plot_rect.bottom() - height, right - left, height)


class CollapsibleSection(QWidget):
    """
    Simple collapsible section.
    """

    expanded_signal = pyqtSignal(bool)

    @log
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self._toggle_button = QToolButton(self)
        self._toggle_button.setText(title)
        self._toggle_button.setCheckable(True)
        self._toggle_button.setChecked(True)
        self._toggle_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self._toggle_button.setArrowType(Qt.DownArrow)
        self._toggle_button.toggled[bool].connect(self.on_toggled)
        layout.addWidget(self._toggle_button)

        self._content = QWidget(self)
        self._content_layout = QVBoxLayout(self._content)
        layout.addWidget(self._content)

    @log
    def add_widget(self, widget: QWidget) -> None:
        """
        Adds a widget to the section.

        :param widget: widget to add
        """
        self._content_layout.addWidget(widget)

    @log
    def is_expanded(self) -> bool:
        """
        Checks whether the section is expanded.

        :return: True when section is expanded
        """
        return self._content.isVisible()

    @log
    def on_toggled(self, checked: bool) -> None:
        """
        Section toggle changed.

        :param checked: True when expanded
        """
        self._content.setVisible(checked)
        self._toggle_button.setArrowType(Qt.DownArrow if checked else Qt.RightArrow)
        self.expanded_signal.emit(checked)
