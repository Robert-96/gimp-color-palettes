import os
import time
import json
import shutil
from zipfile import ZipFile

import click
from jinja2 import Environment, FileSystemLoader

from .__version__ import VERSION
from .convert import json_to_gpl, hex_to_rgb
from .monitor import FileMonitor
from .server import WebServer


def _has_extension(file_name, extension=".json"):
    return os.path.splitext(file_name)[1] == extension


def _get_file_by_extension(path, extension=".json"):
    return [
        os.path.join(path, fileName) for fileName in os.listdir(path) if _has_extension(fileName, extension=extension)
    ]


def _get_json_files(path):
    return _get_file_by_extension(path, extension=".json")


def _get_gpl_files(path):
    return _get_file_by_extension(path, extension=".gpl")


class JinjaGenerator:

    def __init__(self, searchpath="templates", outpath="dist", staticpaths=None, context=None, filters=None,
                 before_callback=None, after_callback=None):
        self.searchpath = searchpath
        self.outpath = outpath
        self.staticpaths = staticpaths or []

        self.before_callback = before_callback
        self.after_callback = after_callback

        self.context = context or {}
        self.filters = filters or {}

        self.env = Environment(
            loader=FileSystemLoader('./templates'),
            trim_blocks=True,
            lstrip_blocks=True
        )
        self.env.filters.update(self.filters)

    def __repr__(self):
        return "{}('{}', '{}')".format(type(self).__name__, self.searchpath, self.outpath)

    @property
    def template_names(self):
        return self.env.list_templates(filter_func=self.is_template)

    @property
    def templates(self):
        for template_name in self.template_names:
            yield self.get_template(template_name)

    def get_template(self, template_name):
        try:
            return self.env.get_template(template_name)
        except UnicodeDecodeError as e:
            raise UnicodeError('Unable to decode {}: {}'.format(template_name, e))

    def is_static(self, template_name):
        return any(template_name.startswith(path) for path in self.staticpaths)

    def is_partial(self, template_name):
        return any((path.startswith("_") for path in template_name.split("/")))

    def is_ignored(self, template_name):
        return any((path.startswith(".") for path in template_name.split("/")))

    def is_template(self, filename):
        if self.is_partial(filename):
            return False
        if self.is_ignored(filename):
            return False
        if self.is_static(filename):
            return False
        return True

    def clear_build(self):
        """Clear previous build."""

        shutil.rmtree(self.outpath, ignore_errors=True)
        os.mkdir(self.outpath)

    def copy_assets(self):
        """Copy static assets such as CSS or JavaScript."""

        for path in self.staticpaths:
            source = os.path.join(self.searchpath, path)
            target = os.path.join(self.outpath, path)

            if os.path.isdir(source):
                shutil.copytree(source, target)
            if os.path.isfile(source):
                shutil.copy2(source, target)

    def render_template(self, template):
        filepath = os.path.join(self.outpath, template.name)
        template.stream(self.context).dump(filepath)

    def render_templates(self):
        for template in self.templates:
            self.render_template(template)

    def build(self):
        """Render the Jinja2 templates."""

        click.secho("Build project...", bold=True, fg="bright_black")

        self.clear_build()

        if self.before_callback:
            self.before_callback(searchpath=self.searchpath, outpath=self.outpath)

        self.copy_assets()
        self.render_templates()

        if self.after_callback:
            self.after_callback(searchpath=self.searchpath, outpath=self.outpath)

        click.secho("Project successfully build.\n", bold=True, fg="green")

    def start(self, monitorpaths=None):
        self.build()

        monitorpaths = monitorpaths or []
        reloader = FileMonitor([self.searchpath, *monitorpaths], self.build)
        reloader.start()

        server = WebServer(directory=self.outpath)
        server.start()

        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            reloader.stop()
            server.stop()


def get_palettes():
    palettes = list()
    json_files = _get_json_files("./data")

    for json_file in json_files:
        with open(json_file, "r") as fp:
            palettes.append(json.loads(fp.read()))

    return palettes


def create_archive(*args, outpath=None, **kwargs):
    archive_path = os.path.join(outpath, "archive")
    os.mkdir(archive_path)

    with ZipFile(os.path.join(archive_path, 'gimp-color-palettes-{}.zip'.format(VERSION)), 'w') as archive:
        for path in _get_gpl_files('./palettes'):
            archive.write(path)


def buid_project(develop=False):
    palettes = get_palettes()

    generator = JinjaGenerator(
        staticpaths=['public'],
        context={
            'version': VERSION,
            'palettes': palettes,
            'gpl': {palette.get("id"): json_to_gpl(palette) for palette in palettes}
        },
        filters={
            'rgb': lambda x: 'rgb({rgb[0]}, {rgb[1]}, {rgb[2]})'.format(rgb=hex_to_rgb(x))
        },
        after_callback=create_archive
    )

    if develop:
        generator.start(monitorpaths=['data'])
    else:
        generator.build()


if __name__ == "__main__":
    buid_project()
