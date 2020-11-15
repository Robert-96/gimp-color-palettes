from scripts.build import _has_extension

import pytest


@pytest.mark.parametrize(
    "file, extension, expected",
    [
        ("palette.gpl", ".gpl", True),
        ("palette.json", ".json", True),
        ("palette.txt", ".txt", True),
        ("palette.gpl", ".txt", False),
        ("palette.gpl", ".json", False),
    ]
)
def test_has_extension(file, extension, expected):
    assert _has_extension(file, extension=extension) == expected
