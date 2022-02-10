import pytest

from dietpdf.filter import hex_to_bytes

__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"


def create_objects() -> list:
    return [
        (b"", b""),
        (b"7", b"p"),
        (b"6162636465666768696a6b6c6d6e6f70", b"abcdefghijklmnop"),
        (b"6162636465666768696a6b6c6d6e6f7", b"abcdefghijklmnop"),
        (b" 61 62 63 64 65 66 67 68 69 6a 6b 6c 6d 6e 6f 70",
         b"abcdefghijklmnop"),
        (b" 61 62 63 64 65 66 67 68 69 6a 6b 6c 6d 6e 6f 7  ",
         b"abcdefghijklmnop"),
        (b"282828295C29282929", b"\\(\\(\\(\\)\\\\\\)\\(\\)\\)"),
    ]


def test_hex_to_bytes():
    for (hexstring, result) in create_objects():
        assert hex_to_bytes(hexstring) == result
