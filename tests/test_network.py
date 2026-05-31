import asyncio
from collections import namedtuple
from concurrent.futures import Future
import socket
from typing import Any

import pytest

from als.streams.network import (
    ADVERTISED_ADDRESS_AUTO,
    WEB_SERVER_BIND_HOST,
    Server,
    advertised_address_preference,
    get_network_address_candidates,
    select_advertised_address,
)


Address = namedtuple("Address", ["family", "address"])
pytestmark = pytest.mark.filterwarnings(
    "ignore:Bare functions are deprecated:DeprecationWarning")


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


def test_auto_selection_uses_highest_ranked_candidate() -> None:
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
    )

    assert selected.ip == "10.42.0.1"


def test_empty_discovery_falls_back_to_loopback() -> None:
    candidates = get_network_address_candidates(8000, {})

    assert len(candidates) == 1
    assert candidates[0].ip == "127.0.0.1"


def test_server_start_reports_success_after_binding(
        monkeypatch: Any, tmp_path: Any) -> None:
    """
    Checks that server startup reports success only after site binding.
    """
    captured = {}

    class FakeSite:
        """
        Captures aiohttp site binding arguments.
        """

        def __init__(self, runner: Any, host: str, port: int) -> None:
            captured["host"] = host
            captured["port"] = port

        async def start(self) -> None:
            """
            Simulates successful aiohttp site binding.
            """
            captured["started"] = True

    monkeypatch.setattr("als.streams.network.web.TCPSite", FakeSite)
    server = Server(str(tmp_path))
    startup_future = Future()

    asyncio.set_event_loop(server._loop)
    server_task = server._loop.create_task(
        server._start_server(WEB_SERVER_BIND_HOST, 8000, startup_future))
    try:
        server._loop.run_until_complete(
            asyncio.wrap_future(startup_future, loop=server._loop))
        server_task.cancel()
        server._loop.run_until_complete(server_task)
        server._loop.run_until_complete(server._runner.cleanup())
    finally:
        server._loop.close()
        asyncio.set_event_loop(None)

    assert captured == {
        "host": WEB_SERVER_BIND_HOST,
        "port": 8000,
        "started": True,
    }


def test_server_start_reports_bind_failure(
        monkeypatch: Any, tmp_path: Any) -> None:
    """
    Checks that server startup reports aiohttp bind failures.
    """
    bind_error = OSError("port unavailable")

    class FakeSite:
        """
        Simulates aiohttp site binding failure.
        """

        def __init__(self, runner: Any, host: str, port: int) -> None:
            pass

        async def start(self) -> None:
            """
            Raises the simulated bind failure.
            """
            raise bind_error

    monkeypatch.setattr("als.streams.network.web.TCPSite", FakeSite)
    server = Server(str(tmp_path))
    startup_future = Future()

    asyncio.set_event_loop(server._loop)
    server_task = server._loop.create_task(
        server._start_server(WEB_SERVER_BIND_HOST, 8000, startup_future))

    try:
        with pytest.raises(OSError):
            server._loop.run_until_complete(server_task)
    finally:
        server._loop.close()
        asyncio.set_event_loop(None)

    assert startup_future.exception() is bind_error
