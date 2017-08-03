"""Test the dtool dataset verify command."""

import os

from click.testing import CliRunner

from . import dataset_fixture  # NOQA


def test_dataset_verify(dataset_fixture):  # NOQA
    from dtool_info.dataset import verify
    import dtoolcore

    runner = CliRunner()

    result = runner.invoke(verify, [dataset_fixture])
    assert result.exit_code == 0

    assert result.output.strip() == "All good :)"

    # Add a unknown file to the data directory.
    fpath = os.path.join(dataset_fixture, "data", "unknown.txt")
    with open(fpath, "w") as fh:
        fh.write("this file is not indexed")

    result = runner.invoke(verify, [dataset_fixture])
    assert result.exit_code == 0
    assert result.output.strip() == "Unknown file: {}".format(fpath)

    os.unlink(fpath)

    # Remove an indexed file.
    dataset = dtoolcore.DataSet.from_path(dataset_fixture)
    identifier = dataset.manifest["file_list"][0]["hash"]
    fpath = dataset.abspath_from_identifier(identifier)
    os.unlink(fpath)

    result = runner.invoke(verify, [dataset_fixture])
    assert result.exit_code == 0
    assert result.output.strip() == "Missing file: {}".format(fpath)

    # Alter the content of an indexed file.
    with open(fpath, "w") as fh:
        fh.write("different content")

    result = runner.invoke(verify, [dataset_fixture])
    assert result.exit_code == 0
    assert result.output.strip() == "Altered file: {}".format(fpath)
