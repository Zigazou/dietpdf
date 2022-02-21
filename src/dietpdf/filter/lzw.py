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


CLEAR_TABLE_MARKER = 256
END_OF_DATA_MARKER = 257

BITS_SLICES = {
    9: [
        ([0xff, 0x80], 7),
        ([0x7f, 0xc0], 6),
        ([0x3f, 0xe0], 5),
        ([0x1f, 0xf0], 4),
        ([0x0f, 0xf8], 3),
        ([0x07, 0xfc], 2),
        ([0x03, 0xfe], 1),
        ([0x01, 0xff], 0),
    ],
    10: [
        ([0xff, 0xc0], 6),
        ([0x7f, 0xe0], 5),
        ([0x3f, 0xf0], 4),
        ([0x1f, 0xf8], 3),
        ([0x0f, 0xfc], 2),
        ([0x07, 0xfe], 1),
        ([0x03, 0xff], 0),
        ([0x01, 0xff, 0x80], 7),
    ],
    11: [
        ([0xff, 0xe0], 5),
        ([0x7f, 0xf0], 4),
        ([0x3f, 0xf8], 3),
        ([0x1f, 0xfc], 2),
        ([0x0f, 0xfe], 1),
        ([0x07, 0xff], 0),
        ([0x03, 0xff, 0x80], 7),
        ([0x01, 0xff, 0xc0], 6),
    ],
    12: [
        ([0xff, 0xf0], 4),
        ([0x7f, 0xf8], 3),
        ([0x3f, 0xfc], 2),
        ([0x1f, 0xfe], 1),
        ([0x0f, 0xff], 0),
        ([0x07, 0xff, 0x80], 7),
        ([0x03, 0xff, 0xc0], 6),
        ([0x01, 0xff, 0xe0], 5),
    ],
}


def _lzw_next_code(content, bits_per_code, bit_position):
    (offset, bit_number) = (bit_position >> 3, bit_position & 7)
    (masks, shift) = BITS_SLICES[bits_per_code][bit_number]

    if offset > len(content) - len(masks):
        return None

    if len(masks) == 2:
        return (
            ((content[offset] & masks[0]) << 8) +
            (content[offset + 1] & masks[1])
        ) >> shift
    else:
        return (
            ((content[offset] & masks[0]) << 16) +
            ((content[offset + 1] & masks[1]) << 8) +
            (content[offset + 2] & masks[2])
        ) >> shift


def lzw_decode(content: bytes) -> bytes:
    """Uncompress a byte string using LZW."""

    assert type(content) == bytes

    dictionary = {index: b"%c" % index for index in range(256)}
    dictionary_length = 258
    bits_per_code = 9
    bit_position = 0

    current_word = CLEAR_TABLE_MARKER
    previous_word = 0
    output = b""
    while True:
        previous_word = current_word
        current_word = _lzw_next_code(content, bits_per_code, bit_position)
        bit_position += bits_per_code

        if current_word == None:
            raise UnableToLZWDecode("Stop code not found in LZWDecode")

        if current_word == END_OF_DATA_MARKER:
            break
        elif current_word == CLEAR_TABLE_MARKER:
            dictionary_length = 258
            bits_per_code = 9
        elif previous_word == CLEAR_TABLE_MARKER:
            output += dictionary[current_word]
        else:
            if current_word < dictionary_length:
                output += dictionary[current_word]
                dictionary[dictionary_length] = b"%s%c" % (
                    dictionary[previous_word],
                    dictionary[current_word][0]
                )
            else:
                new_word = b"%s%c" % (
                    dictionary[previous_word],
                    dictionary[previous_word][0]
                )
                output += new_word
                dictionary[dictionary_length] = new_word

            dictionary_length += 1

            if dictionary_length >= (1 << bits_per_code) - 1 and bits_per_code < 12:
                bits_per_code += 1

    return output
