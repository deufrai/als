import logging

import numpy as np

from als.code_utilities import log


def test_given_plain_log_when_logged_function_runs_then_values_are_not_condensed(caplog):
    """
    Checks that log condensation is opt-in.
    """
    @log
    def logged_function(value):
        return value

    value = np.array([1, 2, 3])

    with caplog.at_level(logging.DEBUG, logger=__name__):
        result = logged_function(value)

    assert result is value
    assert "array([1, 2, 3])" in caplog.text
    assert "ndarray(shape=(3,)" not in caplog.text


def test_given_condensed_log_when_small_numpy_array_is_logged_then_summary_includes_shape_dtype_and_stats(caplog):
    """
    Checks that small arrays keep useful stats without dumping values.
    """
    @log(condense=True)
    def logged_function(value):
        return value

    value = np.array([1, 2, 3])

    with caplog.at_level(logging.DEBUG, logger=__name__):
        result = logged_function(value)

    assert result is value
    assert "ndarray(shape=(3,), dtype=int64, min=1, max=3)" in caplog.text
    assert "array([1, 2, 3])" not in caplog.text


def test_given_condensed_log_when_large_numpy_array_is_logged_then_summary_omits_stats(caplog):
    """
    Checks that large arrays avoid full scans for min/max.
    """
    @log(condense=True)
    def logged_function(value):
        return value

    value = np.zeros((65, 65))

    with caplog.at_level(logging.DEBUG, logger=__name__):
        result = logged_function(value)

    assert result is value
    assert "ndarray(shape=(65, 65), dtype=float64)" in caplog.text
    assert "min=" not in caplog.text
    assert "max=" not in caplog.text
