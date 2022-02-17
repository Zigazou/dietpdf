__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from subprocess import Popen, PIPE
from shutil import which


class UnableToLZWEncode(Exception):
    pass


class UnableToLZWDecode(Exception):
    pass


def lzw_encode(content: bytes) -> bytes:
    """Compress a byte string using LZW."""
    """
    assert type(content) == bytes

    output = b""
    code_length = 9

    def emit_code(code):
        output += 

    CLEAR_TABLE_MARKER = 256
    END_OF_DATA_MARKER = 257

    lzw_table = {
        code: (b"%c" % code) if code < 256 else b""
        for code in range(0, END_OF_DATA_MARKER + 1)
    }


    output = b""
    """

def lzw_decode(content: bytes) -> bytes:
    """Uncompress a byte string using LZW."""

    assert type(content) == bytes

