from als.updates import find_available_update


def test_given_equal_stable_versions_when_update_is_checked_then_no_update_is_available():
    assert find_available_update("1.0", "1.0") is None


def test_given_newer_numeric_version_when_update_is_checked_then_update_is_available():
    assert find_available_update("1.0.9", "1.0.10") == "1.0.10"


def test_given_older_remote_version_when_update_is_checked_then_no_update_is_available():
    assert find_available_update("1.1", "1.0.10") is None


def test_given_equivalent_numeric_versions_when_update_is_checked_then_no_update_is_available():
    assert find_available_update("1.0", "1.0.0") is None


def test_given_alpha_versions_when_update_is_checked_then_qualifier_number_is_compared_numerically():
    assert find_available_update("1.0-alpha2", "1.0-alpha10") == "1.0-alpha10"


def test_given_alpha_and_beta_versions_when_update_is_checked_then_beta_is_newer():
    assert find_available_update("1.0-alpha10", "1.0-beta1") == "1.0-beta1"


def test_given_beta_and_stable_versions_when_update_is_checked_then_stable_is_newer():
    assert find_available_update("1.0-beta10", "1.0") == "1.0"


def test_given_version_with_prefix_and_whitespace_when_update_is_checked_then_version_is_normalized():
    assert find_available_update("v1.0-beta1", " \nv1.0\n") == "1.0"


def test_given_invalid_remote_version_when_update_is_checked_then_remote_value_is_ignored():
    assert find_available_update("1.0", "latest") is None


def test_given_remote_development_version_when_update_is_checked_then_remote_value_is_ignored():
    assert find_available_update("1.0", "1.1-dev-abc-bld123") is None


def test_given_unsupported_remote_qualifier_when_update_is_checked_then_remote_value_is_ignored():
    assert find_available_update("1.0-beta1", "1.0-rc1") is None


def test_given_unnumbered_remote_qualifier_when_update_is_checked_then_remote_value_is_ignored():
    assert find_available_update("1.0-alpha1", "1.0-beta") is None


def test_given_same_base_local_development_build_when_stable_is_published_then_update_is_available():
    assert find_available_update("1.0-dev-abc-bld123", "1.0") == "1.0"


def test_given_same_base_local_development_build_when_beta_is_published_then_update_is_available():
    assert find_available_update("1.0-dev", "1.0-beta1") == "1.0-beta1"


def test_given_newer_base_local_development_build_when_update_is_checked_then_no_update_is_available():
    assert find_available_update("1.1-dev-abc-bld123", "1.0") is None


def test_given_setuptools_scm_development_build_when_newer_release_exists_then_update_is_available():
    assert find_available_update(
        "0.7.post0.dev332+g861b6f1",
        "1.0"
    ) == "1.0"
