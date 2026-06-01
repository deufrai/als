import socket
from collections import namedtuple
from typing import Any, Generator

import pytest

from als import config
from als.logic import Controller
from als.model.data import DYNAMIC_DATA
from als.streams.network import NetworkAddress, get_network_address_candidates

Address = namedtuple("Address", ["family", "address"])


def _addr(ip: str) -> Address:
    """
    Builds a minimal psutil-like network address.

    :param ip: IP address
    :return: address tuple
    """
    return Address(socket.AF_INET, ip)


@pytest.fixture(autouse=True)
def reset_config_parser() -> Generator[None, None, None]:
    """
    Resets in-memory config and web runtime state around each test.
    """
    config._CONFIG_PARSER.clear()
    config._CONFIG_PARSER.add_section(config._MAIN_SECTION_NAME)
    _reset_web_server_runtime_state()
    yield
    config._CONFIG_PARSER.clear()
    _reset_web_server_runtime_state()


def test_update_web_server_advertised_address_uses_configured_ip(
        monkeypatch: Any) -> None:
    """
    Checks that the configured advertised IP wins when present.
    """
    monkeypatch.setattr(
        "als.logic.get_network_address_candidates",
        lambda port: [
            _network_address("wlan0", "10.42.0.1", port),
            _network_address("Wi-Fi", "192.168.1.42", port),
        ])
    config.set_www_server_advertised_address("ip:10.42.0.1")

    advertised_address = Controller.update_web_server_advertised_address()

    assert advertised_address.ip == "10.42.0.1"
    assert advertised_address.url == "http://10.42.0.1:8000"
    candidate_ips = [
        candidate.ip
        for candidate in DYNAMIC_DATA.web_server_address_candidates
    ]
    assert candidate_ips == [
        "10.42.0.1",
        "192.168.1.42",
    ]


def test_update_web_server_advertised_address_falls_back_to_auto(
        monkeypatch: Any) -> None:
    """
    Checks that a missing configured IP falls back to Auto selection.
    """
    monkeypatch.setattr(
        "als.logic.get_network_address_candidates",
        lambda port: [
            _network_address("wlan0", "10.42.0.1", port),
            _network_address("Wi-Fi", "192.168.1.42", port),
        ])
    config.set_www_server_advertised_address("ip:192.168.50.50")

    advertised_address = Controller.update_web_server_advertised_address()

    assert advertised_address.ip == "10.42.0.1"


def _network_address(interface_name: str, ip: str, port: int) -> NetworkAddress:
    """
    Builds a network address candidate using production discovery code.

    :param interface_name: network interface name
    :param ip: IP address
    :param port: web server port number
    :return: network address candidate
    """
    return get_network_address_candidates(
        port, {interface_name: [_addr(ip)]})[0]


def _reset_web_server_runtime_state() -> None:
    """
    Resets web server runtime fields touched by these tests.
    """
    DYNAMIC_DATA.web_server_is_running = False
    DYNAMIC_DATA.web_server_advertised_ip = ""
    DYNAMIC_DATA.web_server_advertised_url = ""
    DYNAMIC_DATA.web_server_address_candidates = []
