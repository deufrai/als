# SPDX-FileCopyrightText: 2019-2026 The ALS Authors
# SPDX-License-Identifier: GPL-3.0-or-later

"""
A set of shared utilities for number crunching
"""
from logging import getLogger
from typing import Optional

import numpy as np
from PyQt5.QtCore import QT_TRANSLATE_NOOP

from als.code_utilities import AlsLogAdapter, log
from als.messaging import MESSAGE_HUB
from als.model.base import Image
from als.model.data import HistogramContainer

_LOGGER = AlsLogAdapter(getLogger(__name__), {})


@log
def compute_histograms_for_display(image, bin_count):
    """
    Compute histograms
    """
    container = HistogramContainer()

    if image.is_color():
        for channel in range(3):
            container.add_histogram(_compute_single_channel_histogram_for_display(image.data[:, :, channel], bin_count))
    else:
        container.add_histogram(_compute_single_channel_histogram_for_display(image.data, bin_count))

    container.global_maximum = max([histo.max() for histo in container.get_histograms()])

    return container


@log(condense=True)
def _compute_single_channel_histogram_for_display(channel_data, bin_count):

    histogram = np.histogram(channel_data, bin_count, range=(0, 2**16 - 1))[0]

    # we set extremity bins' values to 0 to prevent wrong display on clipped histograms
    histogram[0] = 0

    for current_bin in reversed(range(0, bin_count)):
        if histogram[current_bin] > 0:
            histogram[current_bin] = 0
            break

    return histogram


def _normalize_bayer_flat(flat: Image, master_flat_path: str, bayer_pattern: str) -> Optional[Image]:
    """
    Normalizes a Bayer flat per CFA position using per-channel robust scales.

    :param flat: the flat image to normalize
    :type flat: Image
    :param master_flat_path: path to the master flat file (for logging)
    :type master_flat_path: str
    :param bayer_pattern: the Bayer pattern string (length 4)
    :type bayer_pattern: str
    :return: the flat with normalized data or None if normalization cannot proceed
    :rtype: Optional[Image]
    """
    normalized_flat_data = _sanitize_flat_data(flat.data, master_flat_path)
    pattern = bayer_pattern.upper()

    if len(pattern) != 4:
        MESSAGE_HUB.dispatch_warning(
            __name__,
            QT_TRANSLATE_NOOP("", "Unsupported Bayer pattern {}. Flat division is SKIPPED"),
            [bayer_pattern]
        )
        return None

    row_slices = [slice(0, None, 2), slice(1, None, 2)]
    col_slices = [slice(0, None, 2), slice(1, None, 2)]
    cfa_positions = [
        (pattern[0], row_slices[0], col_slices[0]),
        (pattern[1], row_slices[0], col_slices[1]),
        (pattern[2], row_slices[1], col_slices[0]),
        (pattern[3], row_slices[1], col_slices[1]),
    ]

    for position_index, (channel_name, row_slice, col_slice) in enumerate(cfa_positions):
        channel_view = normalized_flat_data[row_slice, col_slice]
        scale = _compute_robust_scale(channel_view)

        if scale <= 0 or not np.isfinite(scale):
            MESSAGE_HUB.dispatch_warning(
                __name__,
                QT_TRANSLATE_NOOP("", "Master flat {} has insufficient signal for channel {}. Flat division is SKIPPED"),
                [master_flat_path, f"{channel_name}-{position_index}"]
            )
            return None

        epsilon = max(scale * _NORMALIZATION_EPSILON_FACTOR, _NORMALIZATION_EPSILON_MIN)
        np.maximum(channel_view, epsilon, out=channel_view)
        channel_view /= scale

    flat.data = normalized_flat_data
    return flat


def _normalize_global_flat(flat: Image, master_flat_path: str) -> Optional[Image]:
    """
    Normalizes a mono flat using a global robust scale.

    :param flat: the flat image to normalize
    :type flat: Image
    :param master_flat_path: path to the master flat file (for logging)
    :type master_flat_path: str
    :return: the flat with normalized data or None if normalization cannot proceed
    :rtype: Optional[Image]
    """
    normalized_flat_data = _sanitize_flat_data(flat.data, master_flat_path)
    scale = _compute_robust_scale(normalized_flat_data)

    if scale <= 0 or not np.isfinite(scale):
        MESSAGE_HUB.dispatch_warning(
            __name__,
            QT_TRANSLATE_NOOP("", "Master flat {} contains no valid signal. Flat division is SKIPPED"),
            [master_flat_path]
        )
        return None

    epsilon = max(scale * _NORMALIZATION_EPSILON_FACTOR, _NORMALIZATION_EPSILON_MIN)
    np.maximum(normalized_flat_data, epsilon, out=normalized_flat_data)
    normalized_flat_data /= scale

    flat.data = normalized_flat_data
    return flat


@log
def _sanitize_flat_data(flat_data: np.ndarray, master_flat_path: str) -> np.ndarray:
    """
    Converts flat data to float32 and replaces non-finite values with zero, warning the user.

    :param flat_data: raw flat data array
    :type flat_data: numpy.ndarray
    :param master_flat_path: path to the master flat file (for logging)
    :type master_flat_path: str
    :return: sanitized float32 flat data
    :rtype: numpy.ndarray
    """
    sanitized_data = flat_data.astype(np.float32, copy=False)

    if not np.isfinite(sanitized_data).all():
        MESSAGE_HUB.dispatch_warning(
            __name__,
            QT_TRANSLATE_NOOP("", "Master flat {} contains invalid values. Replacing NaN/Inf with 0 before normalization"),
            [master_flat_path]
        )
        sanitized_data = np.where(np.isfinite(sanitized_data), sanitized_data, 0.0)

    return sanitized_data


def _compute_robust_scale(values: np.ndarray) -> float:
    """
    Computes a robust scale using median with an upper percentile clamp to limit hot pixel influence.

    :param values: data values for which scale is computed
    :type values: numpy.ndarray
    :return: the computed scale
    :rtype: float
    """
    finite_values = values[np.isfinite(values)]

    if finite_values.size == 0:
        return 0.0

    percentile_cap = np.percentile(finite_values, _CHANNEL_SCALE_PERCENTILE_CLIP)
    clipped_values = np.clip(finite_values, None, percentile_cap)

    return float(np.median(clipped_values))


_NORMALIZATION_EPSILON_FACTOR = 1e-6
_NORMALIZATION_EPSILON_MIN = 1e-8
_CHANNEL_SCALE_PERCENTILE_CLIP = 99.9
