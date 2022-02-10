__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from dietpdf.filter.hex_to_bytes import hex_to_bytes

from .PDFHexString import PDFHexString
from .PDFString import PDFString


def hexstring_to_string(hexstring: PDFHexString) -> PDFString:
    """Converts a PDFHexString to a PDFString"""

    assert type(hexstring) == PDFHexString

    return PDFString(hex_to_bytes(hexstring.hexstring))
