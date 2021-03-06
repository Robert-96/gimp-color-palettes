import os
import json

import click
from click_help_colors import HelpColorsGroup

from .build import buid_project
from .convert import json_to_gpl


CONTEXT_SETTINGS = dict(help_option_names=["--help", "-h"])


@click.group(
    context_settings=CONTEXT_SETTINGS,
    cls=HelpColorsGroup,
    help_headers_color='yellow',
    help_options_color='green'
)
@click.version_option(None, "--version", "-v")
def cli():
    """A CLI tool for converting JSON into GIMP color palettes."""


@cli.command()
def build():
    """Build the project."""

    buid_project()


@cli.command()
def start():
    """Build the project and start an development server."""

    buid_project(develop=True)


@cli.command()
@click.argument("input_path", type=click.Path(exists=True, dir_okay=False))
@click.option("--gpl", "output_path", type=click.Path(exists=False, dir_okay=False),
              help="The path for the GIMP color palette output.")
@click.option("--verbose/--quiet", default=False,
              help="Print GIMP color palette.")
def convert(input_path, output_path, verbose):
    """Convert JSON into GIMP color palette."""

    click.secho("Convert {} into a GIMP color palette...".format(input_path), bold=True, fg="bright_black")

    with open(input_path) as fp:
        palette = json.load(fp)

    if not output_path:
        file_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join("./palettes", file_name + ".gpl")

    with open(output_path, "w+") as fp:
        gpl = json_to_gpl(palette)
        fp.write(gpl)

        if verbose:
            click.secho("GIMP color palette:\n", bold=True, fg="bright_black")
            click.echo(gpl)

    click.echo()
    click.secho("GIMP color palette create at {}.".format(output_path), bold=True, fg="green")


if __name__ == "__main__":
    cli()
