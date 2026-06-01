from als.model.data import DynamicData


def test_given_fresh_dynamic_data_when_initialized_then_web_server_runtime_fields_are_defaulted() -> None:
    """
    Checks default web server runtime fields on fresh dynamic data.
    """
    dynamic_data = DynamicData()

    assert dynamic_data.web_server_is_running is False
    assert dynamic_data.web_server_advertised_ip == ""
    assert dynamic_data.web_server_advertised_url == ""
    assert dynamic_data.web_server_address_candidates == []


def test_given_multiple_dynamic_data_instances_when_candidate_list_is_changed_then_instances_do_not_share_candidates() -> None:
    """
    Checks that address candidate lists are not shared between instances.
    """
    first_dynamic_data = DynamicData()
    second_dynamic_data = DynamicData()

    first_dynamic_data.web_server_address_candidates.append(object())

    assert second_dynamic_data.web_server_address_candidates == []
