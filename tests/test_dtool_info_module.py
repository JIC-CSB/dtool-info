"""Test the dtool_info module."""


def test_version_is_string():
    import dtool_info
    assert isinstance(dtool_info.__version__, str)
