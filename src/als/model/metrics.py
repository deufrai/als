"""
Runtime metrics models.
"""
import time
from typing import List, Tuple

from PyQt5.QtCore import QObject, pyqtSignal

from als.code_utilities import log


class SystemMetrics(QObject):
    """
    Holds live system metrics for the current session window.
    """

    QUEUE_PRE_PROCESS = "pre-process"
    QUEUE_STACKER = "stacker"
    QUEUE_POST_PROCESS = "post-process"
    QUEUE_SAVE = "save"

    QUEUE_NAMES = (
        QUEUE_PRE_PROCESS,
        QUEUE_STACKER,
        QUEUE_POST_PROCESS,
        QUEUE_SAVE,
    )

    updated_signal = pyqtSignal()

    _MAX_QUEUE_SAMPLES = 300
    _MAX_MEMORY_SAMPLES = 120

    @log
    def __init__(self, parent=None):
        super().__init__(parent)
        self._queue_samples = dict()
        self._available_memory_samples = list()
        self.reset()

    @log
    def reset(self) -> None:
        """
        Resets session-scoped system metrics.
        """
        self._queue_samples = {
            queue_name: list()
            for queue_name in self.QUEUE_NAMES
        }
        self._available_memory_samples = list()
        self.updated_signal.emit()

    @log
    def record_queue_size(self, queue_name: str, size: int) -> None:
        """
        Records a queue size sample.

        :param queue_name: the queue being sampled
        :param size: current queue size
        """
        if queue_name not in self._queue_samples:
            return

        self._append_bounded_sample(
            self._queue_samples[queue_name],
            self._get_timestamp(),
            size,
            self._MAX_QUEUE_SAMPLES)
        self.updated_signal.emit()

    @log
    def record_available_memory(self, byte_count: int) -> None:
        """
        Records an available-memory sample.

        :param byte_count: available memory in bytes
        """
        memory_megabytes = byte_count / 1024 / 1024
        self._append_bounded_sample(
            self._available_memory_samples,
            self._get_timestamp(),
            memory_megabytes,
            self._MAX_MEMORY_SAMPLES)
        self.updated_signal.emit()

    @log
    def get_queue_series(self, queue_name: str) -> Tuple[List[float], List[int]]:
        """
        Gets queue samples for plotting.

        :param queue_name: queue name
        :return: sample timestamps and queue sizes
        """
        return self._split_samples(self._queue_samples.get(queue_name, list()))

    @log
    def get_available_memory_series(self) -> Tuple[List[float], List[float]]:
        """
        Gets available-memory samples for plotting.

        :return: sample timestamps and memory values in megabytes
        """
        return self._split_samples(self._available_memory_samples)

    @staticmethod
    @log
    def _append_bounded_sample(samples: list, timestamp: float, value, max_length: int) -> None:
        samples.append((timestamp, value))
        if len(samples) > max_length:
            del samples[0]

    @staticmethod
    @log
    def _get_timestamp() -> float:
        return time.time()

    @staticmethod
    @log
    def _split_samples(samples: List[Tuple[float, object]]):
        if not samples:
            return list(), list()

        x_values, y_values = zip(*samples)
        return list(x_values), list(y_values)


class AstroSessionMetrics(QObject):
    """
    Holds live astro metrics for the current session.
    """

    updated_signal = pyqtSignal()

    @log
    def __init__(self, parent=None):
        super().__init__(parent)
        self.reset()

    @log
    def reset(self) -> None:
        """
        Resets session astro metrics.
        """
        self.updated_signal.emit()


class LiveMetrics(QObject):
    """
    Owns live metrics domains.
    """

    @log
    def __init__(self, parent=None):
        super().__init__(parent)
        self._system_metrics = SystemMetrics(self)
        self._astro_session_metrics = AstroSessionMetrics(self)

    @log
    def get_system_metrics(self) -> SystemMetrics:
        """
        Gets system metrics.

        :return: system metrics
        """
        return self._system_metrics

    @log
    def get_astro_session_metrics(self) -> AstroSessionMetrics:
        """
        Gets astro session metrics.

        :return: astro session metrics
        """
        return self._astro_session_metrics

    @log
    def reset_session_metrics(self) -> None:
        """
        Resets metrics scoped to the current session.
        """
        self._system_metrics.reset()
        self._astro_session_metrics.reset()
