from pathlib import Path
from typing import Any, Generator

import pytest

from als import config


@pytest.fixture(autouse=True)
def reset_config_parser() -> Generator[None, None, None]:
    """
    Resets the in-memory config parser around each test.
    """
    config._CONFIG_PARSER.clear()
    config._CONFIG_PARSER.add_section(config._MAIN_SECTION_NAME)
    yield
    config._CONFIG_PARSER.clear()


def test_www_server_advertised_address_defaults_to_auto() -> None:
    """
    Checks the default advertised address preference.
    """
    assert config.get_www_server_advertised_address() == "auto"


def test_www_server_advertised_address_can_be_set() -> None:
    """
    Checks that an explicit advertised address preference is persisted.
    """
    config.set_www_server_advertised_address("ip:192.168.1.150")

    assert config.get_www_server_advertised_address() == "ip:192.168.1.150"


def test_www_server_advertised_address_survives_setup_cleanup(
        monkeypatch: Any, tmp_path: Path) -> None:
    """
    Checks that setup keeps the advertised address preference key.
    """
    monkeypatch.setattr(config, "_CONFIG_FILE_PATH", str(tmp_path / "als.cfg"))
    config.set_www_server_advertised_address("ip:192.168.1.150")
    config._CONFIG_PARSER.set(config._MAIN_SECTION_NAME, "obsolete", "value")

    config.setup()

    assert config.get_www_server_advertised_address() == "ip:192.168.1.150"
    assert not config._CONFIG_PARSER.has_option(
        config._MAIN_SECTION_NAME, "obsolete")
