"""Test the dtool dataset summary command."""

from click.testing import CliRunner

from . import dataset_fixture  # NOQA


def test_dataset_summary(dataset_fixture):  # NOQA
    from dtool_info.dataset import summary
    import json
    import getpass

    runner = CliRunner()

    result = runner.invoke(summary, [dataset_fixture])
    assert result.exit_code == 0

    summary = json.loads(result.output)
    expected = {
        "Name": "test",
        "Creator": getpass.getuser(),
        "Number of files": 2,
        "Total size": 10,
    }
    assert summary == expected
