__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

import re

from .PDFItem import PDFItem

class PDFHexString(PDFItem):
    """A PDF hexadecimal string (between < and >)"""

    def __init__(self, hexstring: bytes):
        self.hexstring = hexstring

    def __bool__(self):
        return self.hexstring != None and len(self.hexstring) > 0

    def __eq__(self, other):
        if isinstance(other, PDFHexString):
            return self.hexstring == other.hexstring
        elif isinstance(other, bytes):
            return self.hexstring == other
        elif isinstance(other, PDFItem):
            return False
        else:
            return NotImplemented

    def pretty(self) -> str:
        return self._pretty("HexString(%s)" % (self.hexstring.decode('ascii'),))

    def encode(self) -> bytes:
        return b"<%s>" % re.sub(b"[^0-9A-Za-z]+", b"", self.hexstring)
