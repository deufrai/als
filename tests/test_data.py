from als.model.data import DynamicData


def test_dynamic_data_initializes_web_server_runtime_fields() -> None:
    """
    Checks default web server runtime fields on fresh dynamic data.
    """
    dynamic_data = DynamicData()

    assert dynamic_data.web_server_is_running is False
    assert dynamic_data.web_server_ip == ""
    assert dynamic_data.web_server_bind_host == ""
    assert dynamic_data.web_server_advertised_ip == ""
    assert dynamic_data.web_server_advertised_url == ""
    assert dynamic_data.web_server_qr_ip == ""
    assert dynamic_data.web_server_qr_url == ""
    assert dynamic_data.web_server_address_candidates == []


def test_dynamic_data_uses_distinct_candidate_lists() -> None:
    """
    Checks that address candidate lists are not shared between instances.
    """
    first_dynamic_data = DynamicData()
    second_dynamic_data = DynamicData()

    first_dynamic_data.web_server_address_candidates.append(object())

    assert second_dynamic_data.web_server_address_candidates == []
