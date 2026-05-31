import logging

import numpy as np

from als.code_utilities import compact_log_value, log


def test_log_accepts_value_formatter(caplog):
    """
    Checks that log formatting is opt-in and does not alter return values.
    """
    formatter_calls = []

    def formatter(value):
        formatter_calls.append(value)
        return "formatted"

    @log(value_formatter=formatter)
    def logged_function(value):
        return value

    with caplog.at_level(logging.DEBUG, logger=__name__):
        result = logged_function("original")

    assert result == "original"
    assert len(formatter_calls) == 3
    assert "formatted" in caplog.text
    assert "original" not in caplog.text


def test_compact_log_value_summarizes_small_arrays():
    """
    Checks that small arrays keep useful stats without dumping values.
    """
    value = compact_log_value(np.array([1, 2, 3]))

    assert repr(value) == "ndarray(shape=(3,), dtype=int64, min=1, max=3)"


def test_compact_log_value_summarizes_large_arrays_without_stats():
    """
    Checks that large arrays avoid full scans for min/max.
    """
    value = compact_log_value(np.zeros((65, 65)))

    assert repr(value) == "ndarray(shape=(65, 65), dtype=float64)"
