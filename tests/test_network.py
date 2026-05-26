from collections import namedtuple
import socket
from typing import Any

from als.streams.network import (
    ADVERTISED_ADDRESS_AUTO,
    advertised_address_preference,
    get_network_address_candidates,
    select_advertised_address,
)


Address = namedtuple("Address", ["family", "address"])


def _addr(ip: str) -> Any:
    return Address(socket.AF_INET, ip)


def test_private_addresses_are_ranked_before_link_local_and_loopback() -> None:
    candidates = get_network_address_candidates(
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


def test_auto_selection_prefers_route_address_when_available() -> None:
    candidates = get_network_address_candidates(
        8000,
        {
            "Wi-Fi": [_addr("192.168.1.42")],
            "wlan0": [_addr("10.42.0.1")],
        },
    )

    selected = select_advertised_address(
        ADVERTISED_ADDRESS_AUTO,
        candidates,
        route_ip="10.42.0.1",
    )

    assert selected.ip == "10.42.0.1"
    assert selected.interface_name == "wlan0"
    assert selected.label == "Wi-Fi - 10.42.0.1"


def test_ip_preference_selects_matching_candidate() -> None:
    candidates = get_network_address_candidates(
        8000,
        {
            "Wi-Fi": [_addr("192.168.1.42")],
            "wlan0": [_addr("10.42.0.1")],
        },
    )

    selected = select_advertised_address(
        advertised_address_preference("10.42.0.1"),
        candidates,
        route_ip="192.168.1.42",
    )

    assert selected.ip == "10.42.0.1"


def test_missing_ip_preference_falls_back_to_auto() -> None:
    candidates = get_network_address_candidates(
        8000,
        {
            "Wi-Fi": [_addr("192.168.1.42")],
            "wlan0": [_addr("10.42.0.1")],
        },
    )

    selected = select_advertised_address(
        advertised_address_preference("192.168.50.50"),
        candidates,
        route_ip="10.42.0.1",
    )

    assert selected.ip == "10.42.0.1"


def test_empty_discovery_falls_back_to_loopback() -> None:
    candidates = get_network_address_candidates(8000, {})

    assert len(candidates) == 1
    assert candidates[0].ip == "127.0.0.1"
