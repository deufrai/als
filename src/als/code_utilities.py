# SPDX-FileCopyrightText: 2019-2026 The ALS Authors
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Provides a set of utilities aimed at app developpers
"""
import logging
from datetime import datetime
from functools import wraps
from logging import LoggerAdapter
from queue import Queue
from time import time
from typing import Any, Callable, TypeVar

import psutil
from PyQt5.QtCore import QObject, pyqtSignal, QFile, QIODevice, QTextStream


class AlsLogAdapter(LoggerAdapter):

    def process(self, msg, kwargs):
        msg = f"{get_timestamp()} {msg}"
        return super().process(msg, kwargs)



_T = TypeVar("_T")


class LogValueSummary:
    """
    Compact representation for values that are too noisy in detailed logs.

    This intentionally wraps summary text instead of returning a plain string so
    tuple/list/dict logging uses the unquoted ``repr()`` form. That keeps values
    looking like compact object summaries instead of string literals.
    """
    def __init__(self, text: str):
        self._text = text

    def __repr__(self) -> str:
        return self._text

    def __str__(self) -> str:
        return self._text


def _compact_log_value(value: Any) -> Any:
    """
    Replaces numpy arrays with compact summaries for logging.

    Full image arrays are summarized by shape and dtype only. Small arrays, such
    as histogram bins, also include min/max because that is cheap and useful.

    :param value: value to summarize
    :return: original value or a logging-only summary
    """
    if _is_numpy_array(value):
        return _summarize_numpy_array(value)

    if isinstance(value, tuple):
        return tuple(_compact_log_value(item) for item in value)

    if isinstance(value, list):
        return [_compact_log_value(item) for item in value]

    if isinstance(value, dict):
        return {
            key: _compact_log_value(item)
            for key, item in value.items()
        }

    return value


def _is_numpy_array(value: Any) -> bool:
    return (
        value.__class__.__module__ == "numpy"
        and value.__class__.__name__ == "ndarray"
    )


def _summarize_numpy_array(value: Any) -> LogValueSummary:
    parts = [
        f"shape={value.shape}",
        f"dtype={value.dtype}",
    ]

    if value.size <= 4096:
        parts.extend([
            f"min={value.min()}",
            f"max={value.max()}",
        ])

    return LogValueSummary(f"ndarray({', '.join(parts)})")


def log(func: Callable[..., _T] = None, *, condense: bool = False) -> Callable[..., _T]:
    """
    Decorates a function to add logging.

    A log entry (DEBUG level) is printed with decorated function's qualified name and all its params.

    If the decorated function returns anything, a log entry (DEBUG level) is printed with decorated
    function's qualified name and return value(s).

    Logs are issued using the logger named after the decorated function's enclosing module. Logging
    only runs when DEBUG is enabled for that logger to keep overhead minimal otherwise.

    :param func: The function to decorate
    :param condense: When True, noisy values are compacted in log entries.
    :return: The decorated function
    """
    if func is None:
        return lambda decorated_func: log(decorated_func, condense=condense)

    function_name = func.__qualname__
    logger = AlsLogAdapter(logging.getLogger(func.__module__), {})

    @wraps(func)
    def wrapped(*args: Any, **kwargs: Any) -> _T:
        if logger.isEnabledFor(logging.DEBUG):
            logged_args = _compact_log_value(args) if condense else args
            logged_kwargs = _compact_log_value(kwargs) if condense else kwargs
            logger.debug("%s() called with : %s - %s", function_name, logged_args, logged_kwargs)
            start_time = time()
            result = func(*args, **kwargs)
            elapsed_ms = (time() - start_time) * 1000
            logged_result = _compact_log_value(result) if condense else result
            logger.debug("%s() returned %s in %.3f ms", function_name, logged_result, elapsed_ms)
            return result
        return func(*args, **kwargs)

    return wrapped


# pylint: disable=W0201
class Timer:
    """
    A context manager, timing any portion of code it encloses.

    Basic usage :

    .. code-block:: python

        with Timer() as t:

            # your code here
            # it can be many lines
            pass

        _LOGGER.info(f"code ran in {t.elapsed_in_milli} ms.")

    The context manager exposes 2 attributes :

        - elapsed_in_milli (float) = elapsed time
        - elapsed_in_milli_as_str (str) = string representation of elapsed time with only 3 decimal positions

    """
    def __enter__(self):
        self.start = time()
        return self

    def __exit__(self, *args):
        self.end = time()
        self.elapsed_in_milli = (self.end - self.start) * 1000
        self.elapsed_in_milli_as_str = "%0.3f" % self.elapsed_in_milli


class AlsException(Exception):
    """
    Base class for all custom errors
    """
    @log
    def __init__(self, message, details):
        Exception.__init__(self)
        self.message = message
        self.details = details


class SignalingQueue(Queue, QObject):
    """
    Queue subclass that emits a Qt signal when items are added or removed from the queue.

    Signal is :

      - size_changed_signal

    and carries the new queue size
    """

    size_changed_signal = pyqtSignal(int)
    """
    Qt signal stating that a new item has just been pushed to the queue.

    :param: the new size of the queue
    :type: int
    """

    @log
    def __init__(self, maxsize=0):
        Queue.__init__(self, maxsize)
        QObject.__init__(self)

    @log
    def get(self, block=True, timeout=None):
        item = super().get(block, timeout)
        self.size_changed_signal.emit(self.qsize())
        return item

    @log
    def get_nowait(self):
        item = super().get_nowait()
        self.size_changed_signal.emit(self.qsize())
        return item

    @log
    def put(self, item, block=True, timeout=None):
        super().put(item, block, timeout)
        self.size_changed_signal.emit(self.qsize())

    @log
    def put_nowait(self, item):
        super().put_nowait(item)
        self.size_changed_signal.emit(self.qsize())


def get_timestamp():
    """
    Return a timestamp built from current date and time

    :return: the timestamp
    :rtype: str
    """
    timestamp = str(datetime.fromtimestamp(datetime.timestamp(datetime.now())))
    return timestamp


def human_readable_byte_size(num):
    """
    returns a human readable representation of a raw number of bytes

    :param num: how nay bytes ?
    :return: a human readable representation of given bytes
    :rtype: str
    """
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.3f %sB" % (num, unit)
        num /= 1024.0
    return "%.3f %sB" % (num, 'Yi')


@log
def get_text_content_of_resource(resource_uri: str):
    """
    Get text content of a file stored inside Qt resources

    :param resource_uri: URI if said resource
    :type resource_uri: str

    :return: textual content or empty-string if an OS error occurred
    :rtype: str
    """
    try:
        fake_file = QFile(resource_uri)
        fake_file.open(QIODevice.ReadOnly | QFile.Text)
        return QTextStream(fake_file).readAll()
    except OSError:
        return ""


def available_memory():
    """
    Get system available memory in bytes
    :return: available memory (bytes)
    :rtype: int
    """
    return psutil.virtual_memory().available
