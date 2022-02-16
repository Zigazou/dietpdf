__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

import re


def hex_to_bytes(hexstring: bytes) -> bytes:
    """Convert a hexadecimal string to a byte string.

    This allows to render space-friendly byte strings when encoding.

    :param hexstring: The hexadecimal string to convert
    :type hexstring: bytes
    :return: The converted string
    :rtype: bytes
    """

    assert type(hexstring) == bytes

    # Remove any spaces
    cleaned = b"%s" % re.sub(b"[^0-9A-Za-z]+", b"", hexstring)

    # If there is only one digit in the last slot, add a 0
    if len(cleaned) >= 1 and len(cleaned) % 2 == 1:
        cleaned += b"0"

    # Convert hexdecimal characters to bytes
    cleaned = bytes.fromhex(cleaned.decode('ascii'))

    # Escape special characters
    cleaned = cleaned.replace(b"\\", b"\\\\")
    cleaned = cleaned.replace(b"(", b"\\(")
    cleaned = cleaned.replace(b")", b"\\)")
    cleaned = cleaned.replace(b"\r", b"\\r")

    return cleaned