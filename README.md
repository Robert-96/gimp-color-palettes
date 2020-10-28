# gimp-color-palettes

[![GitHub](https://img.shields.io/github/license/robert-96/gimp-color-palettes)](./LICENSE)
[![Build Status](https://travis-ci.org/Robert-96/gimp-color-palettes.svg?branch=main)](https://travis-ci.org/Robert-96/gimp-color-palettes)
[![Website](https://img.shields.io/website?url=https%3A%2F%2Frobert-96.github.io%2Fgimp-color-palettes%2F)](https://robert-96.github.io/gimp-color-palettes/)

A collection of color palettes for [GIMP](https://www.gimp.org/) and [Inkscape](https://inkscape.org/) (but also [Aseprite](https://www.aseprite.org/), [Drawpile](https://drawpile.net/), [Krita](https://krita.org/), [MyPaint](http://mypaint.org/)).

You can preview and download all these palettes [directly in the browser](https://robert-96.github.io/gimp-color-palettes/).

## Format

GIMP palettes are stored using a special file format, in files with the extension `.gpl`.

```
GIMP Palette
Name: <name>
Columns: <number>
# <comment>
  0    0    0  Black
255  255  255  White
```

* `GIMP Palette` - it must be the first line of the file.
* `Name: <name>` - sets the name of the color palette.
* `Columns: <number>` - is just an indication for display.
* `# <comment>` - comments must start with a `#`.
* `  0    0    0  Black` - RGB values for the color followed by the color name.

```
GIMP Palette
Name: Example
Columns: 2
# A simple example
  0    0    0  Black
255  255  255  White
255    0    0  Red
  0  255    0  Green
  0    0  255  Blue
```

## Adding the palettes

### Inkscape

Copy the `.gpl` file in the folder `/palettes`, which you create in the folder indicated at **Edit ‣ Preferences ‣ System: User config**.

Restart Inkscape to see the new palette in the list.

### GIMP

Copy the `.gpl` file in the folder `/palettes`, which you create in the folder indicated at **Edit ‣ Preferences ‣ Folders ‣ Palettes**.

Restart GIMP to see the new palette in the list.

## License

This project is licensed under the [MIT License](./LICENSE).