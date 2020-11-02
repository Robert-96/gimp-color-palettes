import os
import json

import pytest
from click.testing import CliRunner

from scripts.cli import cli


JSON = {
    "name": "Color Palette Name",
    "columns": 8,
    "url": "https://github.com/",
    "colors": [
        {
            "name": "Black",
            "hex": "#000000"
        },
        {
            "name": "White",
            "hex": "#FFFFFF"
        }
    ]
}

GPL = [
    "GIMP Palette",
    "Name: Color Palette Name",
    "Columns: 8",
    "# https://github.com/",
    "  0    0    0  Black",
    "255  255  255  White"
]
GPL = "\n".join(GPL)


def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli, [])

    assert result.exit_code == 0
    assert result.output != ''


def test_convert(tmpdir):
    input_path = os.path.join(tmpdir, 'palette.json')
    output_path = os.path.join(tmpdir, 'palette.gpl')

    with open(input_path, 'w') as fp:
        fp.write(json.dumps(JSON))

    runner = CliRunner()
    result = runner.invoke(cli, ['convert', input_path, '--gpl', output_path])

    with open(output_path) as fp:
        output = fp.read()

    assert output == GPL
    assert result.exit_code == 0
    assert result.output != ''


def test_convert_no_input(tmpdir):
    output_path = os.path.join(tmpdir, 'palette.gpl')

    runner = CliRunner()
    result = runner.invoke(cli, ['convert', '--gpl', output_path])

    assert not os.path.isfile(output_path)
    assert result.exit_code == 2
    assert result.output != ''


def test_convert_verbose(tmpdir):
    input_path = os.path.join(tmpdir, 'palette.json')
    output_path = os.path.join(tmpdir, 'palette.gpl')

    with open(input_path, 'w') as fp:
        fp.write(json.dumps(JSON))

    runner = CliRunner()
    result = runner.invoke(cli, ['convert', input_path, '--gpl', output_path, "--verbose"])

    assert result.exit_code == 0
    assert GPL in result.output


def test_convert_quiet(tmpdir):
    input_path = os.path.join(tmpdir, 'palette.json')
    output_path = os.path.join(tmpdir, 'palette.gpl')

    with open(input_path, 'w') as fp:
        fp.write(json.dumps(JSON))

    runner = CliRunner()
    result = runner.invoke(cli, ['convert', input_path, '--gpl', output_path, "--quiet"])

    assert result.exit_code == 0
    assert GPL not in result.output