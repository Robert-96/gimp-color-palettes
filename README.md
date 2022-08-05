# gimp-color-palettes

A collection of RGB color palettes for [GIMP](https://www.gimp.org/) and [Inkscape](https://inkscape.org/) (but also [Aseprite](https://www.aseprite.org/), [Drawpile](https://drawpile.net/), [Krita](https://krita.org/) and [MyPaint](http://mypaint.org/)).

You can preview and download all these palettes [directly in the browser](https://robert-96.github.io/gimp-color-palettes/).

![Screenshot](/screenshots/screenshot.png)

## Table of Contents

* [GIMP's Palettes Format](#gimps-palettes-format)
* [Importing the palettes](#importing-the-palettes)
  * [GIMP](#gimp)
  * [Inkscape](#inkscape)
* [License](#license)

## GIMP's Palettes Format

GIMP palettes are stored using a special file format, in files with the extension `.gpl`.

Every palette must have the following structure:

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
* `Columns: <number>` - is just an indication for displaying the palette inside GIMP.
* `# <comment>` - comments must start with a `#`. All comments are ignored by GIMP.
* `  0    0    0  Black` - RGB values for the color followed by the color name.

Here is an simple example:

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

> **Note**: The RGB values don't need to line up.

## Importing the palettes

### GIMP

Copy the `.gpl` file in the folder `/palettes`, which you create in the folder indicated at **Edit ‣ Preferences ‣ Folders ‣ Palettes**.

Restart GIMP to see the new palette in the list.

### Inkscape

Copy the `.gpl` file in the folder indicated at **Edit ‣ Preferences ‣ System: User palettes**.

Restart Inkscape to see the new palette in the list.

## License

This project is licensed under the [MIT License](./LICENSE).
