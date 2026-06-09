# SPDX-FileCopyrightText: 2019-2026 The ALS Authors
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Provides application update version comparison.
"""
import re
from typing import Optional, Tuple

from als.code_utilities import log

_PUBLISHED_VERSION_PATTERN = re.compile(
    r"^v?(?P<base>[0-9]+(?:\.[0-9]+)+)"
    r"(?:-(?P<qualifier>alpha|beta)(?P<qualifier_number>[0-9]+))?$"
)
_LOCAL_DASH_DEV_PATTERN = re.compile(
    r"^v?(?P<base>[0-9]+(?:\.[0-9]+)+)-dev(?:[-+._].*)?$"
)
_LOCAL_SCM_DEV_PATTERN = re.compile(
    r"^v?(?P<base>[0-9]+(?:\.[0-9]+)+)"
    r"(?:\.post[0-9]+)?\.dev[0-9]+(?:\+.*)?$"
)

_DEVELOPMENT_STAGE = 0
_ALPHA_STAGE = 1
_BETA_STAGE = 2
_RELEASE_STAGE = 3

_Version = Tuple[Tuple[int, ...], int, int]

@log
def find_available_update(
        local_version: str,
        remote_version_content: str) -> Optional[str]:
    """
    Returns the published remote version when it is newer than the local build.

    Invalid remote values, including development versions, are ignored.

    :param local_version: running ALS version
    :param remote_version_content: content retrieved from the version endpoint
    :return: normalized newer remote version, or None
    """
    remote_text = remote_version_content.strip()
    remote_version = _parse_published_version(remote_text)
    local_parsed_version = _parse_local_version(local_version.strip())

    if remote_version is None or local_parsed_version is None:
        return None

    if _compare_versions(remote_version, local_parsed_version) > 0:
        return remote_text[1:] if remote_text.startswith("v") else remote_text

    return None


@log
def _parse_published_version(version: str) -> Optional[_Version]:
    match = _PUBLISHED_VERSION_PATTERN.match(version)
    if match is None:
        return None

    qualifier = match.group("qualifier")
    if qualifier == "alpha":
        stage = _ALPHA_STAGE
    elif qualifier == "beta":
        stage = _BETA_STAGE
    else:
        stage = _RELEASE_STAGE

    qualifier_number = int(match.group("qualifier_number") or 0)
    return (
        _parse_components(match.group("base")),
        stage,
        qualifier_number
    )


@log
def _parse_local_version(version: str) -> Optional[_Version]:
    published_version = _parse_published_version(version)
    if published_version is not None:
        return published_version

    for pattern in (_LOCAL_DASH_DEV_PATTERN, _LOCAL_SCM_DEV_PATTERN):
        match = pattern.match(version)
        if match is not None:
            return (
                _parse_components(match.group("base")),
                _DEVELOPMENT_STAGE,
                0
            )

    return None


@log
def _parse_components(base_version: str) -> Tuple[int, ...]:
    components = tuple(int(component) for component in base_version.split("."))

    while len(components) > 1 and components[-1] == 0:
        components = components[:-1]

    return components


@log
def _compare_versions(first: _Version, second: _Version) -> int:
    first_components, first_stage, first_qualifier_number = first
    second_components, second_stage, second_qualifier_number = second
    component_count = max(len(first_components), len(second_components))
    first_components += (0,) * (component_count - len(first_components))
    second_components += (0,) * (component_count - len(second_components))

    first_key = (
        first_components,
        first_stage,
        first_qualifier_number
    )
    second_key = (
        second_components,
        second_stage,
        second_qualifier_number
    )

    return (first_key > second_key) - (first_key < second_key)
