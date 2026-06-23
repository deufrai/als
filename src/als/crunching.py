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
from als.model.base import Image, HistogramContainer

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
    Normalizes a Bayer flat into a color-neutral correction field.

    Each CFA position is first normalized by its own robust scale so the
    sensor/filter response does not leak into the flat correction. The four
    normalized CFA positions are then merged into a shared 2x2-cell correction
    and written back to every phase. This keeps luminance vignetting and dust
    correction while preventing the master flat from adding spatial color
    balance shifts.

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

    phase_views = [
        normalized_flat_data[row_slice, col_slice]
        for _channel_name, row_slice, col_slice in cfa_positions
    ]
    phase_labels = [
        "{}-{}".format(channel_name, position_index)
        for position_index, (channel_name, _row_slice, _col_slice) in enumerate(cfa_positions)
    ]

    if not _normalize_flat_channel_views(phase_views, master_flat_path, phase_labels):
        return None

    flat.data = normalized_flat_data
    return flat


def _normalize_global_flat(flat: Image, master_flat_path: str) -> Optional[Image]:
    """
    Normalizes a mono or color flat into a correction field.

    Mono flats are normalized using a global robust scale. Color flats are
    normalized per channel, then merged into a shared luminance correction and
    written back to every channel to avoid adding color imbalance.

    :param flat: the flat image to normalize
    :type flat: Image
    :param master_flat_path: path to the master flat file (for logging)
    :type master_flat_path: str
    :return: the flat with normalized data or None if normalization cannot proceed
    :rtype: Optional[Image]
    """
    normalized_flat_data = _sanitize_flat_data(flat.data, master_flat_path)

    if normalized_flat_data.ndim > 2:
        return _normalize_color_flat(flat, normalized_flat_data, master_flat_path)

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


def _normalize_color_flat(flat: Image, normalized_flat_data: np.ndarray, master_flat_path: str) -> Optional[Image]:
    """
    Normalizes a color flat into a shared correction field for all channels.

    :param flat: the flat image to normalize
    :type flat: Image
    :param normalized_flat_data: sanitized flat data
    :type normalized_flat_data: numpy.ndarray
    :param master_flat_path: path to the master flat file
    :type master_flat_path: str
    :return: the flat with normalized data or None if normalization cannot proceed
    :rtype: Optional[Image]
    """
    channel_views = [
        normalized_flat_data[:, :, channel_index]
        for channel_index in range(normalized_flat_data.shape[2])
    ]

    if not _normalize_flat_channel_views(channel_views, master_flat_path):
        return None

    flat.data = normalized_flat_data
    return flat


def _normalize_bayer_dark(dark: Image, master_dark_path: str, bayer_pattern: str) -> Optional[Image]:
    """
    Normalizes Bayer dark phase baselines without removing dark structure.

    :param dark: the dark image to normalize
    :type dark: Image
    :param master_dark_path: path to the master dark file
    :type master_dark_path: str
    :param bayer_pattern: the Bayer pattern string (length 4)
    :type bayer_pattern: str
    :return: the dark with normalized data or None if normalization cannot proceed
    :rtype: Optional[Image]
    """
    normalized_dark_data = _as_working_dark_data(dark.data)
    pattern = bayer_pattern.upper()

    if len(pattern) != 4:
        MESSAGE_HUB.dispatch_warning(
            __name__,
            QT_TRANSLATE_NOOP("", "Unsupported Bayer pattern {}. Dark subtraction is SKIPPED"),
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
    phase_views = [
        normalized_dark_data[row_slice, col_slice]
        for _channel_name, row_slice, col_slice in cfa_positions
    ]
    phase_labels = [
        "{}-{}".format(channel_name, position_index)
        for position_index, (channel_name, _row_slice, _col_slice) in enumerate(cfa_positions)
    ]

    if not _normalize_dark_channel_baselines(phase_views, master_dark_path, phase_labels):
        return None

    dark.data = _restore_dark_data_type(normalized_dark_data, dark.data.dtype)
    return dark


def _normalize_global_dark(dark: Image, master_dark_path: str) -> Optional[Image]:
    """
    Normalizes color dark baselines and leaves mono darks unchanged.

    :param dark: the dark image to normalize
    :type dark: Image
    :param master_dark_path: path to the master dark file
    :type master_dark_path: str
    :return: the dark with normalized data or None if normalization cannot proceed
    :rtype: Optional[Image]
    """
    if dark.data.ndim <= 2:
        return dark

    normalized_dark_data = _as_working_dark_data(dark.data)
    channel_views = [
        normalized_dark_data[:, :, channel_index]
        for channel_index in range(normalized_dark_data.shape[2])
    ]

    if not _normalize_dark_channel_baselines(channel_views, master_dark_path):
        return None

    dark.data = _restore_dark_data_type(normalized_dark_data, dark.data.dtype)
    return dark


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


def _as_working_dark_data(dark_data: np.ndarray) -> np.ndarray:
    """
    Converts dark data to a signed working representation for baseline updates.

    :param dark_data: raw dark data array
    :type dark_data: numpy.ndarray
    :return: dark data as float32
    :rtype: numpy.ndarray
    """
    return dark_data.astype(np.float32, copy=True)


def _restore_dark_data_type(dark_data: np.ndarray, original_dtype: np.dtype) -> np.ndarray:
    """
    Clips normalized dark data back to its original dtype range.

    :param dark_data: normalized dark data
    :type dark_data: numpy.ndarray
    :param original_dtype: original dark dtype
    :type original_dtype: numpy.dtype
    :return: restored dark data
    :rtype: numpy.ndarray
    """
    if issubclass(original_dtype.type, np.integer):
        limits = np.iinfo(original_dtype)
        return np.clip(dark_data, limits.min, limits.max).astype(original_dtype)

    return dark_data.astype(original_dtype, copy=False)


def _normalize_dark_channel_baselines(channel_views, master_dark_path: str, channel_labels=None) -> bool:
    """
    Makes dark channel medians match while preserving local dark structure.

    :param channel_views: writable 2D views into dark data
    :type channel_views: list[numpy.ndarray]
    :param master_dark_path: path to the master dark file
    :type master_dark_path: str
    :param channel_labels: warning labels for channel views
    :type channel_labels: list[str] or None
    :return: True if normalization succeeded, False otherwise
    :rtype: bool
    """
    if channel_labels is None:
        channel_labels = list(range(len(channel_views)))

    medians = []
    for channel_index, channel_view in enumerate(channel_views):
        median = _compute_robust_median(channel_view)

        if not np.isfinite(median):
            MESSAGE_HUB.dispatch_warning(
                __name__,
                QT_TRANSLATE_NOOP("", "Master dark {} has no valid signal for channel {}. Dark subtraction is SKIPPED"),
                [master_dark_path, channel_labels[channel_index]]
            )
            return False

        medians.append(median)

    common_median = float(np.median(medians))
    _warn_if_dark_has_chromatic_baseline(medians, common_median, master_dark_path)

    for channel_view, median in zip(channel_views, medians):
        channel_view += common_median - median

    return True


def _normalize_flat_channel_views(channel_views, master_flat_path: str, channel_labels=None) -> bool:
    """
    Normalizes channel views in-place and replaces them with a shared correction.

    :param channel_views: writable 2D views into flat data
    :type channel_views: list[numpy.ndarray]
    :param master_flat_path: path to the master flat file
    :type master_flat_path: str
    :param channel_labels: warning labels for channel views
    :type channel_labels: list[str] or None
    :return: True if normalization succeeded, False otherwise
    :rtype: bool
    """
    if channel_labels is None:
        channel_labels = list(range(len(channel_views)))

    for channel_index, channel_view in enumerate(channel_views):
        scale = _compute_robust_scale(channel_view)

        if scale <= 0 or not np.isfinite(scale):
            MESSAGE_HUB.dispatch_warning(
                __name__,
                QT_TRANSLATE_NOOP("", "Master flat {} has insufficient signal for channel {}. Flat division is SKIPPED"),
                [master_flat_path, channel_labels[channel_index]]
            )
            return False

        epsilon = max(scale * _NORMALIZATION_EPSILON_FACTOR, _NORMALIZATION_EPSILON_MIN)
        np.maximum(channel_view, epsilon, out=channel_view)
        channel_view /= scale

    common_height = min(channel_view.shape[0] for channel_view in channel_views)
    common_width = min(channel_view.shape[1] for channel_view in channel_views)
    common_shape_views = [
        channel_view[:common_height, :common_width]
        for channel_view in channel_views
    ]
    stacked_views = np.stack(common_shape_views, axis=0)
    common_correction = np.median(stacked_views, axis=0).astype(np.float32)
    np.maximum(common_correction, _NORMALIZATION_EPSILON_MIN, out=common_correction)

    _warn_if_flat_has_chromatic_shading(
        stacked_views,
        common_correction,
        master_flat_path
    )

    for channel_view in channel_views:
        channel_view[:common_height, :common_width] = common_correction

    return True


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


def _compute_robust_median(values: np.ndarray) -> float:
    """
    Computes a robust median on finite values.

    :param values: data values for which median is computed
    :type values: numpy.ndarray
    :return: the computed median, or NaN when no finite values exist
    :rtype: float
    """
    finite_values = values[np.isfinite(values)]

    if finite_values.size == 0:
        return float("nan")

    return float(np.median(finite_values))


def _warn_if_flat_has_chromatic_shading(
        normalized_phase_data: np.ndarray,
        common_correction: np.ndarray,
        master_flat_path: str) -> None:
    """
    Warns when flat channels disagree after global channel normalization.

    :param normalized_phase_data: normalized channel data with shape (n, y, x)
    :type normalized_phase_data: numpy.ndarray
    :param common_correction: shared color-neutral correction field
    :type common_correction: numpy.ndarray
    :param master_flat_path: path to the master flat file
    :type master_flat_path: str
    """
    safe_common_correction = np.maximum(common_correction, _NORMALIZATION_EPSILON_MIN)
    relative_deviation = np.abs(normalized_phase_data - common_correction) / safe_common_correction
    chromatic_deviation = float(np.percentile(np.max(relative_deviation, axis=0), 95))

    if chromatic_deviation > _FLAT_CHROMA_WARNING_THRESHOLD:
        MESSAGE_HUB.dispatch_warning(
            __name__,
            QT_TRANSLATE_NOOP(
                "",
                "Master flat {} contains {:.1f}% chromatic shading. "
                "Applying color-neutral flat correction to avoid color imbalance."
            ),
            [master_flat_path, chromatic_deviation * 100.0]
        )


def _warn_if_dark_has_chromatic_baseline(medians, common_median: float, master_dark_path: str) -> None:
    """
    Warns when dark channel baselines differ enough to affect color balance.

    :param medians: robust channel medians
    :type medians: list[float]
    :param common_median: shared median applied to channels
    :type common_median: float
    :param master_dark_path: path to the master dark file
    :type master_dark_path: str
    """
    if common_median == 0:
        max_relative_deviation = 0.0
    else:
        max_relative_deviation = max(
            abs(median - common_median) / abs(common_median)
            for median in medians
        )

    max_absolute_deviation = max(abs(median - common_median) for median in medians)

    if (max_relative_deviation > _DARK_CHROMA_WARNING_THRESHOLD
            and max_absolute_deviation > _DARK_CHROMA_WARNING_MIN_DELTA):
        MESSAGE_HUB.dispatch_warning(
            __name__,
            QT_TRANSLATE_NOOP(
                "",
                "Master dark {} contains {:.1f}% chromatic baseline offset. "
                "Applying color-neutral dark correction to avoid color imbalance."
            ),
            [master_dark_path, max_relative_deviation * 100.0]
        )


_NORMALIZATION_EPSILON_FACTOR = 1e-6
_NORMALIZATION_EPSILON_MIN = 1e-8
_CHANNEL_SCALE_PERCENTILE_CLIP = 99.9
_FLAT_CHROMA_WARNING_THRESHOLD = 0.02
_DARK_CHROMA_WARNING_THRESHOLD = 0.02
_DARK_CHROMA_WARNING_MIN_DELTA = 8.0
