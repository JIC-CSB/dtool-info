"""dataset command line module."""

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
