def hex_to_rgb(color):
    """Convert the color from HEX to RGB."""

    color = color.lstrip('#')
    size = 1 if len(color) == 3 else 2
    factor = 2 if len(color) == 3 else 1

    return tuple(int(color[i * size:i * size + size] * factor, 16) for i in range(3))


def rgb_to_hex(r, g, b):
    """Convert the color from RGB to HEX."""

    return f"#{r:02x}{g:02x}{b:02x}"


def _format_color(color):
    return "{:>3}  {:>3}  {:>3}  {}".format(*hex_to_rgb(color["hex"]), color.get("name", "Unknown"))


def json_to_gpl(palette):
    """Convert the palette from JSON format to GPL format."""

    gpl = [
        "GIMP Palette",
        "Name: {}".format(palette.get("name")),
        "Columns: {}".format(palette.get("columns", 16)),
    ]

    if palette.get("url"):
        gpl.append("# {}".format(palette.get("url")))

    for color in palette.get("colors", []):
        gpl.append(_format_color(color))

    return "\n".join(gpl)
