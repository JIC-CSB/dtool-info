"""dataset command line module."""

import os

import click

import dtoolcore

import pygments
import pygments.lexers
import pygments.formatters

from dtool_cli.cli import dataset_path_argument

def number_of_files(dataset):
    """Return number of items in dataset."""
    return len(dataset.identifiers)

def total_size(dataset):
    """Return total size in bytes of dataset."""
    total_size = 0
    for i in dataset.identifiers:
        properties = dataset.item_properties(i)
        total_size += properties["size_in_bytes"]
    return total_size

def creator_username(dataset):
    """Return dataset creator username."""
    return dataset._admin_metadata["creator_username"]


@click.command()
@dataset_path_argument
def summary(dataset_path):
    """Echo a JSON summary of the dataset."""
    dataset = dtoolcore.DataSet.from_uri(dataset_path)

    json_lines = [
        "{",
        '  "Name": "{}",'.format(dataset.name),
        '  "Creator": "{}",'.format(creator_username(dataset)),
        '  "Number of files": {},'.format(number_of_files(dataset)),
        '  "Total size": {}'.format(total_size(dataset)),
        "}",
    ]
    formatted_json = "\n".join(json_lines)
    colorful_json = pygments.highlight(
        formatted_json,
        pygments.lexers.JsonLexer(),
        pygments.formatters.TerminalFormatter())
    click.secho(colorful_json, nl=False)
