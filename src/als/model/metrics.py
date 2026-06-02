"""
Runtime metrics models.
"""
import time
from typing import List, Tuple

from PyQt5.QtCore import QObject, pyqtSignal

from als.code_utilities import compact_log_value, log


def log_metrics(func):
    """
    Logs metrics methods with compact value formatting.

    :param func: function to decorate
    :return: decorated function
    """
    return log(func, value_formatter=compact_log_value)


class SystemMetrics(QObject):
    """
    Holds live system metrics for the current session window.
    """

    QUEUE_PRE_PROCESS = "pre-process"
    QUEUE_STACKER = "stacker"
    QUEUE_POST_PROCESS = "post-process"
    QUEUE_SAVE = "save"

    WORKER_PRE_PROCESS = "pre-process"
    WORKER_STACKER = "stacker"
    WORKER_POST_PROCESS = "post-process"
    WORKER_SAVE = "save"

    QUEUE_NAMES = (
        QUEUE_PRE_PROCESS,
        QUEUE_STACKER,
        QUEUE_POST_PROCESS,
        QUEUE_SAVE,
    )

    WORKER_NAMES = (
        WORKER_PRE_PROCESS,
        WORKER_STACKER,
        WORKER_POST_PROCESS,
        WORKER_SAVE,
    )

    updated_signal = pyqtSignal()

    @log_metrics
    def __init__(self, parent=None):
        super().__init__(parent)
        self._queue_samples = dict()
        self._worker_status_samples = dict()
        self._memory_samples = list()
        self.reset()

    @log_metrics
    def reset(self) -> None:
        """
        Resets session-scoped system metrics.
        """
        self._queue_samples = {
            queue_name: list()
            for queue_name in self.QUEUE_NAMES
        }
        self._worker_status_samples = {
            worker_name: list()
            for worker_name in self.WORKER_NAMES
        }
        self._memory_samples = list()
        self.updated_signal.emit()

    @log_metrics
    def record_queue_size(self, queue_name: str, size: int) -> None:
        """
        Records a queue size sample.

        :param queue_name: the queue being sampled
        :param size: current queue size
        """
        if queue_name not in self._queue_samples:
            return

        self._append_sample(
            self._queue_samples[queue_name],
            self._get_timestamp(),
            size)
        self.updated_signal.emit()

    @log_metrics
    def record_worker_status(self, worker_name: str, is_busy: bool) -> None:
        """
        Records a worker status sample.

        :param worker_name: the worker being sampled
        :param is_busy: True when worker is busy
        """
        if worker_name not in self._worker_status_samples:
            return

        self._append_sample(
            self._worker_status_samples[worker_name],
            self._get_timestamp(),
            int(is_busy))
        self.updated_signal.emit()

    @log_metrics
    def record_memory_status(
            self,
            available_byte_count: int,
            preserved_byte_count: int) -> None:
        """
        Records an aligned memory sample.

        :param available_byte_count: available memory in bytes
        :param preserved_byte_count: preserved memory margin in bytes
        """
        available_memory_megabytes = available_byte_count / 1024 / 1024
        preserved_memory_megabytes = preserved_byte_count / 1024 / 1024
        self._append_sample(
            self._memory_samples,
            self._get_timestamp(),
            (available_memory_megabytes, preserved_memory_megabytes))
        self.updated_signal.emit()

    @log_metrics
    def get_queue_series(self, queue_name: str) -> Tuple[List[float], List[int]]:
        """
        Gets queue samples for plotting.

        :param queue_name: queue name
        :return: sample timestamps and queue sizes
        """
        return self._split_samples(self._queue_samples.get(queue_name, list()))

    @log_metrics
    def get_available_memory_series(self) -> Tuple[List[float], List[float]]:
        """
        Gets available-memory samples for plotting.

        :return: sample timestamps and memory values in megabytes
        """
        timestamps, memory_values = self._split_samples(self._memory_samples)
        return timestamps, [sample[0] for sample in memory_values]

    @log_metrics
    def get_preserved_memory_series(self) -> Tuple[List[float], List[int]]:
        """
        Gets preserved-memory samples for plotting.

        :return: sample timestamps and preserved memory values in megabytes
        """
        timestamps, memory_values = self._split_samples(self._memory_samples)
        return timestamps, [sample[1] for sample in memory_values]

    @log_metrics
    def get_worker_status_series(self, worker_name: str) -> Tuple[List[float], List[int]]:
        """
        Gets worker status samples for plotting.

        :param worker_name: worker name
        :return: sample timestamps and worker statuses where 1 means busy
        """
        return self._split_samples(self._worker_status_samples.get(worker_name, list()))

    @log_metrics
    def get_time_range(self) -> Tuple[float, float]:
        """
        Gets the shared system metrics time range.

        :return: minimum and maximum timestamps
        """
        timestamps = list()
        timestamps.extend([sample[0] for sample in self._memory_samples])
        for queue_samples in self._queue_samples.values():
            timestamps.extend([sample[0] for sample in queue_samples])
        for status_samples in self._worker_status_samples.values():
            timestamps.extend([sample[0] for sample in status_samples])

        if not timestamps:
            current_timestamp = self.get_current_timestamp()
            return current_timestamp, current_timestamp + 1

        start = min(timestamps)
        end = max(max(timestamps), self.get_current_timestamp())
        if start == end:
            end = start + 1

        return start, end

    def get_log_summary(self) -> str:
        """
        Gets compact logging summary.

        :return: compact logging summary
        """
        queue_counts = {
            queue_name: len(samples)
            for queue_name, samples in self._queue_samples.items()
        }
        worker_counts = {
            worker_name: len(samples)
            for worker_name, samples in self._worker_status_samples.items()
        }
        return (
            "SystemMetrics("
            f"memory_samples={len(self._memory_samples)}, "
            f"queue_samples={queue_counts}, "
            f"worker_samples={worker_counts})"
        )

    @staticmethod
    @log_metrics
    def _append_sample(samples: list, timestamp: float, value) -> None:
        samples.append((timestamp, value))

    @staticmethod
    @log_metrics
    def _get_timestamp() -> float:
        return SystemMetrics.get_current_timestamp()

    @staticmethod
    @log_metrics
    def get_current_timestamp() -> float:
        """
        Gets the current system metrics timestamp.

        :return: current timestamp
        """
        return time.time()

    @staticmethod
    @log_metrics
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

    @log_metrics
    def __init__(self, parent=None):
        super().__init__(parent)
        self.reset()

    @log_metrics
    def reset(self) -> None:
        """
        Resets session astro metrics.
        """
        self.updated_signal.emit()

    def get_log_summary(self) -> str:
        """
        Gets compact logging summary.

        :return: compact logging summary
        """
        return "AstroSessionMetrics()"


class LiveMetrics(QObject):
    """
    Owns live metrics domains.
    """

    @log_metrics
    def __init__(self, parent=None):
        super().__init__(parent)
        self._system_metrics = SystemMetrics(self)
        self._astro_session_metrics = AstroSessionMetrics(self)

    @log_metrics
    def get_system_metrics(self) -> SystemMetrics:
        """
        Gets system metrics.

        :return: system metrics
        """
        return self._system_metrics

    @log_metrics
    def get_astro_session_metrics(self) -> AstroSessionMetrics:
        """
        Gets astro session metrics.

        :return: astro session metrics
        """
        return self._astro_session_metrics

    @log_metrics
    def reset_session_metrics(self) -> None:
        """
        Resets metrics scoped to the current session.
        """
        self._system_metrics.reset()
        self._astro_session_metrics.reset()

    def get_log_summary(self) -> str:
        """
        Gets compact logging summary.

        :return: compact logging summary
        """
        return (
            "LiveMetrics("
            f"system={self._system_metrics.get_log_summary()}, "
            f"astro={self._astro_session_metrics.get_log_summary()})"
        )
