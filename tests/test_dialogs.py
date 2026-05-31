from collections import namedtuple
import socket
from typing import Generator

import pytest

from als.model.data import I18n
from als.streams.network import (
    ADVERTISED_ADDRESS_AUTO, advertised_address_preference,
    get_network_address_candidates
)
from als.ui.dialogs import (
    _address_candidate_label, _address_preference_index,
    _address_preference_items, _set_web_server_port_controls_enabled
)


Address = namedtuple("Address", ["family", "address"])


@pytest.fixture(autouse=True)
def reset_i18n() -> Generator[None, None, None]:
    """
    Resets global state touched by dialog tests.
    """
    I18n().setup()
    yield


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


def test_address_candidate_label_translates_generic_network_adapter() -> None:
    """
    Checks that generic adapter display text goes through I18n.
    """
    candidates = get_network_address_candidates(
        8000,
        {
            "": [_addr("192.168.1.42")],
        },
    )

    assert _address_candidate_label(candidates[0]) == (
        "Network adapter - 192.168.1.42")


def test_set_web_server_port_controls_enabled_only_toggles_port_controls() -> None:
    """
    Checks that address selection can remain available while the server runs.
    """
    ui = _FakePrefsUi()

    _set_web_server_port_controls_enabled(ui, False)

    assert ui.lbl_server_port.enabled is False
    assert ui.ln_web_server_port.enabled is False
    assert ui.label_4.enabled is False
    assert ui.serverBox.enabled is True
    assert ui.cmb_web_server_address.enabled is True


class _FakePrefsUi:
    """
    Minimal Preferences UI double for server control enablement tests.
    """

    def __init__(self) -> None:
        self.serverBox = _FakeWidget()
        self.cmb_web_server_address = _FakeWidget()
        self.lbl_server_port = _FakeWidget()
        self.ln_web_server_port = _FakeWidget()
        self.label_4 = _FakeWidget()


class _FakeWidget:
    """
    Minimal widget double exposing enabled state.
    """

    def __init__(self) -> None:
        self.enabled = True

    def setEnabled(self, enabled: bool) -> None:
        """
        Stores the requested enabled state.
        """
        self.enabled = enabled
