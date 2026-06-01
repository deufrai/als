import logging

import numpy as np

from als.code_utilities import compact_log_value, log


def test_given_value_formatter_when_logged_function_runs_then_logs_use_formatted_values_without_changing_result(caplog):
    """
    Checks that log formatting is opt-in and does not alter return values.
    """
    def formatter(value):
        return "formatted"

    @log(value_formatter=formatter)
    def logged_function(value):
        return value

    with caplog.at_level(logging.DEBUG, logger=__name__):
        result = logged_function("original")

    assert result == "original"
    assert "formatted" in caplog.text
    assert "original" not in caplog.text


def test_given_small_numpy_array_when_compacted_for_logging_then_summary_includes_shape_dtype_and_stats():
    """
    Checks that small arrays keep useful stats without dumping values.
    """
    value = compact_log_value(np.array([1, 2, 3]))

    assert repr(value) == "ndarray(shape=(3,), dtype=int64, min=1, max=3)"


def test_given_large_numpy_array_when_compacted_for_logging_then_summary_omits_stats():
    """
    Checks that large arrays avoid full scans for min/max.
    """
    value = compact_log_value(np.zeros((65, 65)))

    assert repr(value) == "ndarray(shape=(65, 65), dtype=float64)"
