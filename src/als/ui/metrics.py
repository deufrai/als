"""
Live metrics UI.
"""
import pyqtgraph as pg
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog, QVBoxLayout

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
        self.resize(900, 500)

        self._live_metrics = live_metrics
        self._system_metrics = live_metrics.get_system_metrics()
        self._geometry = self.geometry()

        layout = QVBoxLayout(self)

        self._queue_plot = pg.PlotWidget()
        self._queue_plot.setTitle(self.tr("Queue sizes"))
        self._queue_plot.setLabel("bottom", self.tr("Sample"))
        self._queue_plot.setLabel("left", self.tr("Queue size"))
        self._queue_plot.addLegend()
        layout.addWidget(self._queue_plot)

        self._memory_plot = pg.PlotWidget()
        self._memory_plot.setTitle(self.tr("Available memory"))
        self._memory_plot.setLabel("bottom", self.tr("Sample"))
        self._memory_plot.setLabel("left", self.tr("Memory"), units="MB")
        layout.addWidget(self._memory_plot)

        self._queue_curves = self._build_queue_curves()
        self._memory_curve = self._memory_plot.plot(
            pen=pg.mkPen("#3366CC", width=2))

        self._system_metrics.updated_signal.connect(self.update_display)
        self.update_display()

    @log
    def _build_queue_curves(self):
        """
        Builds one curve per monitored queue.

        :return: curves keyed by queue name
        """
        queue_pens = {
            SystemMetrics.QUEUE_PRE_PROCESS: pg.mkPen("#CC3333", width=2),
            SystemMetrics.QUEUE_STACKER: pg.mkPen("#33AA55", width=2),
            SystemMetrics.QUEUE_POST_PROCESS: pg.mkPen("#3366CC", width=2),
            SystemMetrics.QUEUE_SAVE: pg.mkPen("#AA6633", width=2),
        }

        return {
            queue_name: self._queue_plot.plot(
                name=queue_name,
                pen=queue_pens[queue_name])
            for queue_name in SystemMetrics.QUEUE_NAMES
        }

    @log
    def update_display(self) -> None:
        """
        Updates plots from current metrics.
        """
        for queue_name, curve in self._queue_curves.items():
            x_values, y_values = self._system_metrics.get_queue_series(queue_name)
            curve.setData(x_values, y_values)

        x_values, y_values = self._system_metrics.get_available_memory_series()
        self._memory_curve.setData(x_values, y_values)

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
