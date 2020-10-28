import os
import json
import shutil
from zipfile import ZipFile

from jinja2 import Environment

from .convert import json_to_gpl


def _has_extension(path, file_name, extension=".json"):
    return os.path.isfile(os.path.join(path, file_name)) and os.path.splitext(file_name)[1] == extension


def _get_file_by_extension(path, extension=".json"):
    return [os.path.join(path, fileName) for fileName in os.listdir(path) if _has_extension(path, fileName, extension=extension)]


def _get_json_files(path):
    return _get_file_by_extension(path, extension=".json")


def _get_gpl_files(path):
    return _get_file_by_extension(path, extension=".gpl")


def get_palettes():
    palettes = list()
    json_files = _get_json_files("./data")

    for json_file in json_files:
        with open(json_file, "r") as fp:
            palettes.append(json.loads(fp.read()))

    return palettes


def get_template():
    with open("./templates/index.html", "r") as fp:
        template_content = fp.read()

    return template_content


def render_template(template, palettes):
    env = Environment(trim_blocks=True, lstrip_blocks=True)
    template = env.from_string(template)

    return template.render({
        'palettes': palettes,
        'gpl': {palette.get("id"): json_to_gpl(palette) for palette in palettes}
    })


def generate_html():
    palettes = get_palettes()
    template = get_template()

    return render_template(template, palettes)


def clear_build():
    shutil.rmtree("./dist")
    os.mkdir("./dist")


def create_index():
    html = generate_html()

    with open("./dist/index.html", "w") as fp:
        fp.write(html)


def create_archive():
    os.mkdir("./dist/archive")

    with ZipFile('./dist/archive/gimp-color-palettes.zip', 'w') as archive:
        for path in _get_gpl_files('./palettes'):
            archive.write(path)


def copy_assets():
    shutil.copytree("./templates/public", "./dist/public")


def buid_project():
    clear_build()
    create_index()
    create_archive()
    copy_assets()
