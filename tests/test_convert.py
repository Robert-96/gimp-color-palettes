import pytest

from scripts.convert import _hex_to_rgb, _format_color, json_to_gpl


@pytest.mark.parametrize(
    "color, expected",
    [
        ("#000000", (0, 0, 0)),
        ("#000", (0, 0, 0)),
        ("#111111", (17, 17, 17)),
        ("#111", (17, 17, 17)),
        ("#AAAAAA", (170, 170, 170)),
        ("#AAA", (170, 170, 170)),
        ("#FFFFFF", (255, 255, 255)),
        ("#FFF", (255, 255, 255)),
    ]
)
def test_hex_to_rgb(color, expected):
    assert _hex_to_rgb(color) == expected


@pytest.mark.parametrize(
    "long, short",
    [
        ("#000000", "#000"),
        ("#111111", "#111"),
        ("#AAAAAA", "#AAA"),
        ("#FFFFFF", "#FFF"),
        ("#AABBCC", "#ABC"),
        ("#11BB22", "#1B2"),

    ]
)
def test_hex_to_rgb_equality(long, short):
    assert _hex_to_rgb(long) == _hex_to_rgb(short)


@pytest.mark.parametrize(
    "color, expected",
    [
        ({"hex": "#000000", "name": "black"},  "  0    0    0  black"),
        ({"hex": "#FFFFFF", "name": "white"},  "255  255  255  white"),
        ({"hex": "#FF0000", "name": "red"},    "255    0    0  red"),
        ({"hex": "#0000FF", "name": "blue"},   "  0    0  255  blue"),
        ({"hex": "#00FF00", "name": "green"},  "  0  255    0  green"),
        ({"hex": "#FFFF00", "name": "yellow"}, "255  255    0  yellow"),
        ({"hex": "#EE82EE", "name": "violet"}, "238  130  238  violet"),
        ({"hex": "#800080", "name": "purple"}, "128    0  128  purple"),
    ]
)
def test_format_color(color, expected):
    assert _format_color(color) == expected


def test_json_to_gpl():
    json = {
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

    gpl = [
        "GIMP Palette",
        "Name: Color Palette Name",
        "Columns: 8",
        "  0    0    0  Black",
        "255  255  255  White"
    ]

    assert json_to_gpl(json), gpl
