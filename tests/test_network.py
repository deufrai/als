import socket
from collections import namedtuple
from typing import Any

import pytest

from als.streams.network import (
    ADVERTISED_ADDRESS_AUTO,
    build_advertised_address_preference,
    build_network_address_candidates,
    select_advertised_address,
)

PsutilAddress = namedtuple("PsutilAddress", ["family", "address"])
pytestmark = pytest.mark.filterwarnings(
    "ignore:Bare functions are deprecated:DeprecationWarning")


def _addr(ip: str) -> Any:
    return PsutilAddress(socket.AF_INET, ip)


def test_given_private_link_local_and_loopback_addresses_when_candidates_are_discovered_then_private_addresses_are_ranked_first() -> None:
    candidates = build_network_address_candidates(
        8000,
        {
            "Loopback": [_addr("127.0.0.1")],
            "Wi-Fi": [_addr("192.168.1.42")],
            "Ethernet": [_addr("169.254.10.2")],
        },
    )

    assert [candidate.ip for candidate in candidates] == [
        "192.168.1.42",
        "169.254.10.2",
        "127.0.0.1",
    ]
    assert candidates[0].url == "http://192.168.1.42:8000"
    assert candidates[0].label == "Wi-Fi - 192.168.1.42"


def test_given_auto_preference_when_address_is_selected_then_highest_ranked_candidate_is_used() -> None:
    candidates = build_network_address_candidates(
        8000,
        {
            "Wi-Fi": [_addr("192.168.1.42")],
            "wlan0": [_addr("10.42.0.1")],
        },
    )

    selected = select_advertised_address(
        ADVERTISED_ADDRESS_AUTO,
        candidates,
    )

    assert selected.ip == "10.42.0.1"
    assert selected.interface_name == "wlan0"
    assert selected.label == "Wi-Fi - 10.42.0.1"


def test_given_ip_preference_when_candidate_exists_then_matching_address_is_selected() -> None:
    candidates = build_network_address_candidates(
        8000,
        {
            "Wi-Fi": [_addr("192.168.1.42")],
            "wlan0": [_addr("10.42.0.1")],
        },
    )

    selected = select_advertised_address(
        build_advertised_address_preference("10.42.0.1"),
        candidates,
    )

    assert selected.ip == "10.42.0.1"


def test_given_ip_preference_when_candidate_is_missing_then_auto_candidate_is_selected() -> None:
    candidates = build_network_address_candidates(
        8000,
        {
            "Wi-Fi": [_addr("192.168.1.42")],
            "wlan0": [_addr("10.42.0.1")],
        },
    )

    selected = select_advertised_address(
        build_advertised_address_preference("192.168.50.50"),
        candidates,
    )

    assert selected.ip == "10.42.0.1"


def test_given_no_discovered_addresses_when_candidates_are_requested_then_loopback_candidate_is_returned() -> None:
    candidates = build_network_address_candidates(8000, {})

    assert len(candidates) == 1
    assert candidates[0].ip == "127.0.0.1"
