import os
import json
import shutil
from zipfile import ZipFile

from .__version__ import VERSION
from .convert import json_to_gpl, hex_to_rgb
from .generator import JinjaGenerator


def _has_extension(file_name, extension=".json"):
    """Check if a file has an extension."""

    return os.path.splitext(file_name)[1] == extension


def _get_file_by_extension(path, extension=".json"):
    return (os.path.join(path, file_name) for file_name in os.listdir(path)
            if _has_extension(file_name, extension=extension))


def _get_json_files(path):
    return _get_file_by_extension(path, extension=".json")


def _get_gpl_files(path):
    return _get_file_by_extension(path, extension=".gpl")


def get_palettes():
    palettes = list()

    for path in _get_json_files("./data"):
        with open(path, "r") as fp:
            palettes.append(json.loads(fp.read()))

    return palettes


def get_context():
    palettes = get_palettes()

    return {
        'version': VERSION,
        'palettes': sorted(palettes, key=lambda x: x.get('name')),
        'gpl': {palette.get("id"): json_to_gpl(palette) for palette in palettes}
    }


def create_gpl_palettes(palettes=None):
    palettes = palettes or get_palettes()

    for palette in palettes:
        file_name = '{}.gpl'.format(palette['id'])
        gpl = json_to_gpl(palette)

        with open(os.path.join('palettes', file_name), 'w+') as fp:
            fp.write(gpl)


def copy_palettes(*args, outpath=None, **kwargs):
    shutil.copytree("palettes", os.path.join(outpath, "palettes"))


def create_archive(*args, outpath=None, **kwargs):
    archive_path = os.path.join(outpath, "archive")
    os.mkdir(archive_path)

    with ZipFile(os.path.join(archive_path, 'gimp-color-palettes-{}.zip'.format(VERSION)), 'w') as archive:
        for path in _get_gpl_files('./palettes'):
            archive.write(path)


def before_build(*args, **kwargs):
    create_gpl_palettes()


def after_build(*args, outpath=None, **kwargs):
    copy_palettes(*args, outpath=outpath, **kwargs)
    create_archive(*args, outpath=outpath, **kwargs)


def buid_project(develop=False):
    generator = JinjaGenerator(
        staticpaths=['public'],
        contexts=[
            ('.', get_context)
        ],
        filters={
            'rgb': lambda x: 'rgb({rgb[0]}, {rgb[1]}, {rgb[2]})'.format(rgb=hex_to_rgb(x))
        },
        before_callback=before_build,
        after_callback=after_build
    )

    if develop:
        generator.start(monitorpaths=['data'])
    else:
        generator.build()


if __name__ == "__main__":
    buid_project(develop=True)
