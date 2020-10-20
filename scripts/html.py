import os
import json
from distutils.dir_util import copy_tree

from jinja2 import Environment

from .convert import json_to_gpl


def _is_json_file(path, file_name):
    return os.path.isfile(os.path.join(path, file_name)) and os.path.splitext(file_name)[1] == ".json"


def _get_json_files(path):
    return [os.path.join(path, fileName) for fileName in os.listdir(path) if _is_json_file(path, fileName)]


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


def create_html():
    palettes = get_palettes()
    template = get_template()

    return render_template(template, palettes)


def render_html():
    html = create_html()

    try:
        os.mkdir("./dist")
    except FileExistsError:
        pass

    copy_tree("./templates/public", "./dist/public")

    with open("./dist/index.html", "w") as fp:
        fp.write(html)
