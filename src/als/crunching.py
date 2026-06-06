# SPDX-FileCopyrightText: 2019-2026 The ALS Authors
# SPDX-License-Identifier: GPL-3.0-or-later

"""
A set of shared utilities for number crunching
"""
from logging import getLogger

import numpy as np

from als.code_utilities import log, AlsLogAdapter
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
