# gimp-color-palettes

[![Build Status](https://travis-ci.org/Robert-96/gimp-color-palettes.svg?branch=main)](https://travis-ci.org/Robert-96/gimp-color-palettes)

A collection of color palettes for GIMP and Inkscape.

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