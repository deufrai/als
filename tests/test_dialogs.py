from collections import namedtuple
import socket
from typing import Generator

import pytest

from als.model.data import DYNAMIC_DATA
from als.streams.network import (
    ADVERTISED_ADDRESS_AUTO, advertised_address_preference,
    get_network_address_candidates
)
from als.ui.dialogs import (
    QRDisplay, _address_preference_index, _address_preference_items,
    _qr_address_index, _qr_address_items
)


Address = namedtuple("Address", ["family", "address"])


@pytest.fixture(autouse=True)
def reset_qr_runtime_state() -> Generator[None, None, None]:
    """
    Resets QR runtime state touched by dialog tests.
    """
    DYNAMIC_DATA.web_server_qr_url = ""
    yield
    DYNAMIC_DATA.web_server_qr_url = ""


def _addr(ip: str) -> Address:
    """
    Builds a minimal psutil-like network address.

    :param ip: IP address
    :return: address tuple
    """
    return Address(socket.AF_INET, ip)


def test_address_preference_items_include_auto_and_candidate_data() -> None:
    """
    Checks that Preferences stores stable preference values in item data.
    """
    candidates = get_network_address_candidates(
        8000,
        {
            "Wi-Fi": [_addr("192.168.1.42")],
            "wlan0": [_addr("10.42.0.1")],
        },
    )

    address_items = _address_preference_items(candidates)

    assert address_items == [
        ("Auto - recommended", ADVERTISED_ADDRESS_AUTO),
        ("Wi-Fi - 10.42.0.1",
         advertised_address_preference("10.42.0.1")),
        ("Wi-Fi - 192.168.1.42",
         advertised_address_preference("192.168.1.42")),
    ]


def test_address_preference_index_falls_back_to_auto_when_missing() -> None:
    """
    Checks that stale configured addresses select Auto in Preferences.
    """
    address_items = [
        ("Auto - recommended", ADVERTISED_ADDRESS_AUTO),
        ("Wi-Fi - 192.168.1.42",
         advertised_address_preference("192.168.1.42")),
    ]

    selected_index = _address_preference_index(
        advertised_address_preference("10.42.0.1"), address_items)

    assert selected_index == 0


def test_qr_address_items_use_runtime_candidates() -> None:
    """
    Checks that QR address choices expose all current runtime candidates.
    """
    candidates = get_network_address_candidates(
        8000,
        {
            "Wi-Fi": [_addr("192.168.1.42")],
            "wlan0": [_addr("10.42.0.1")],
        },
    )

    address_items = _qr_address_items(candidates, "", "")

    assert address_items == [
        ("Wi-Fi - 10.42.0.1", "10.42.0.1", "http://10.42.0.1:8000"),
        ("Wi-Fi - 192.168.1.42",
         "192.168.1.42",
         "http://192.168.1.42:8000"),
    ]


def test_qr_address_items_fall_back_to_advertised_url() -> None:
    """
    Checks that the QR dropdown can still display the advertised URL.
    """
    address_items = _qr_address_items(
        [],
        "192.168.1.42",
        "http://192.168.1.42:8000")

    assert address_items == [
        ("Current address - 192.168.1.42",
         "192.168.1.42",
         "http://192.168.1.42:8000"),
    ]


def test_qr_address_index_keeps_runtime_choice() -> None:
    """
    Checks that reopening the QR dialog can keep the last runtime URL.
    """
    address_items = [
        ("Wi-Fi - 192.168.1.42",
         "192.168.1.42",
         "http://192.168.1.42:8000"),
        ("Wi-Fi - 10.42.0.1", "10.42.0.1", "http://10.42.0.1:8000"),
    ]

    selected_index = _qr_address_index(
        "http://10.42.0.1:8000", address_items)

    assert selected_index == 1


def test_qr_display_stores_selected_runtime_address() -> None:
    """
    Checks that QR dropdown selection is stored in runtime data.
    """
    display = QRDisplay.__new__(QRDisplay)
    display._ui = _FakeQrUi("10.42.0.1", "http://10.42.0.1:8000")

    QRDisplay._store_selected_qr_address(display)

    assert DYNAMIC_DATA.web_server_qr_url == "http://10.42.0.1:8000"


class _FakeQrUi:
    """
    Minimal QR UI double for runtime selection tests.
    """

    def __init__(self, ip: str, url: str) -> None:
        self.cmb_qr_address = _FakeCombo(ip, url)


class _FakeCombo:
    """
    Minimal combo-box double exposing selected item data.
    """

    def __init__(self, ip: str, url: str) -> None:
        self._data = (ip, url)

    def currentData(self):
        """
        Returns current combo item data.
        """
        return self._data
