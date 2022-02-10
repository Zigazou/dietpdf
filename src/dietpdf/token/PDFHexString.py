__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

import re

from .PDFToken import PDFToken


class PDFHexString(PDFToken):
    """A PDF hexadecimal string (between < and >)"""

    def __init__(self, hexstring: bytes):
        assert type(hexstring) == bytes

        self.hexstring = hexstring

    def __bool__(self):
        """A PDFHexString is True if its string is not empty."""
        return self.hexstring != None and len(self.hexstring) > 0

    def __eq__(self, other):
        """Equality operator for PDFHexString.

        A PDFHexString is:

          - equal to any other PDFHexString with the bytestring
          - equal to byte string with the byte string
          - different from any other PDFToken subclass

        Comparing a PDFHexString with anything else is not implemented.

        :param other: The object to compare to our current object
        :type other: any
        :return: True or False or NotImplemented
        :type: bool
        """
        if isinstance(other, PDFHexString):
            return self.hexstring == other.hexstring
        elif isinstance(other, bytes):
            return self.hexstring == other
        elif isinstance(other, PDFToken):
            return False
        else:
            return NotImplemented

    def pretty(self) -> str:
        return self._pretty("HexString(%s)" % (self.hexstring.decode('ascii'),))

    def encode(self) -> bytes:
        return b"<%s>" % re.sub(b"[^0-9A-Za-z]+", b"", self.hexstring)
