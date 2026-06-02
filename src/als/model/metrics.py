"""
Runtime session metrics.
"""
from typing import List, Tuple

from PyQt5.QtCore import QObject, pyqtSignal

from als.code_utilities import log


class SessionMetrics(QObject):
    """
    Holds bounded live metrics for the current application runtime.
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
        self._queue_sample_index = 0
        self._memory_sample_index = 0
        self._queue_samples = {
            queue_name: list()
            for queue_name in self.QUEUE_NAMES
        }
        self._available_memory_samples = list()

    @log
    def record_queue_size(self, queue_name: str, size: int) -> None:
        """
        Records a queue size sample.

        :param queue_name: the queue being sampled
        :param size: current queue size
        """
        if queue_name not in self._queue_samples:
            return

        self._queue_sample_index += 1
        self._append_bounded_sample(
            self._queue_samples[queue_name],
            self._queue_sample_index,
            size,
            self._MAX_QUEUE_SAMPLES)
        self.updated_signal.emit()

    @log
    def record_available_memory(self, byte_count: int) -> None:
        """
        Records an available-memory sample.

        :param byte_count: available memory in bytes
        """
        self._memory_sample_index += 1
        memory_megabytes = byte_count / 1024 / 1024
        self._append_bounded_sample(
            self._available_memory_samples,
            self._memory_sample_index,
            memory_megabytes,
            self._MAX_MEMORY_SAMPLES)
        self.updated_signal.emit()

    @log
    def get_queue_series(self, queue_name: str) -> Tuple[List[int], List[int]]:
        """
        Gets queue samples for plotting.

        :param queue_name: queue name
        :return: sample indexes and queue sizes
        """
        return self._split_samples(self._queue_samples.get(queue_name, list()))

    @log
    def get_available_memory_series(self) -> Tuple[List[int], List[float]]:
        """
        Gets available-memory samples for plotting.

        :return: sample indexes and memory values in megabytes
        """
        return self._split_samples(self._available_memory_samples)

    @staticmethod
    @log
    def _append_bounded_sample(samples: list, sample_index: int, value, max_length: int) -> None:
        samples.append((sample_index, value))
        if len(samples) > max_length:
            del samples[0]

    @staticmethod
    @log
    def _split_samples(samples: List[Tuple[int, object]]):
        if not samples:
            return list(), list()

        x_values, y_values = zip(*samples)
        return list(x_values), list(y_values)
