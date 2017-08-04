"""dataset command line module."""

import os

import click

import dtoolcore

import pygments
import pygments.lexers
import pygments.formatters

from dtool_cli.cli import dataset_path_argument


@click.command()
@dataset_path_argument
def summary(dataset_path):
    """Echo a JSON summary of the dataset."""
    dataset = dtoolcore.DataSet.from_path(dataset_path)
    file_list = dataset.manifest["file_list"]
    total_size = sum([f["size"] for f in file_list])

    json_lines = [
        "{",
        '  "Name": "{}",'.format(dataset.name),
        '  "Creator": "{}",'.format(dataset.creator_username),
        '  "Number of files": {},'.format(len(file_list)),
        '  "Total size": {}'.format(total_size),
        "}",
    ]
    formatted_json = "\n".join(json_lines)
    colorful_json = pygments.highlight(
        formatted_json,
        pygments.lexers.JsonLexer(),
        pygments.formatters.TerminalFormatter())
    click.secho(colorful_json, nl=False)


@click.command()
@dataset_path_argument
def verify(dataset_path):
    """Verify the integrity of the dataset."""
    all_good = True
    dataset = dtoolcore.DataSet.from_path(dataset_path)
    manifest_data_paths = []
    for item in dataset.manifest["file_list"]:
        fpath = os.path.join(
            dataset._abs_path, dataset.data_directory, item["path"])

        manifest_data_paths.append(fpath)
        if not os.path.isfile(fpath):
            click.secho("Missing file: {}".format(fpath), fg="red")
            all_good = False
            continue
        calculated_hash = dataset._structural_metadata.hash_generator(fpath)
        if item["hash"] != calculated_hash:
            click.secho("Altered file: {}".format(fpath), fg="red")
            all_good = False
            continue

    abs_data_directory = os.path.join(dataset_path, dataset.data_directory)
    existing_data_paths = []
    for root, dirs, files in os.walk(abs_data_directory):
        for f in files:
            fpath = os.path.abspath(os.path.join(root, f))
            existing_data_paths.append(fpath)
    new_data_fpaths = set(existing_data_paths) - set(manifest_data_paths)
    for fpath in new_data_fpaths:
        all_good = False
        click.secho("Unknown file: {}".format(fpath), fg="yellow")

    if all_good:
        click.secho("All good :)".format(fpath), fg="green")
