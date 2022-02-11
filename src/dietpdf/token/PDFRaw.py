__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from .PDFToken import PDFToken


class PDFRaw(PDFToken):
    """Raw bytes in a PDF file"""

    def __init__(self, raw: bytes):
        assert type(raw) == bytes

        self.raw = raw

    def __bool__(self):
        """A PDFRaw is True if it contains characteres, False otherwise."""
        return self.raw != None and len(self.raw) > 0

    def __eq__(self, other):
        """Equality operator for PDFRaw.

        A PDFRaw is:

          - equal to any other PDFRaw with the same byte string
          - equal to any byte string with the same byte string
          - different from any other PDFItem subclass

        Comparing a PDFRaw with anything else is not implemented.

        :param other: The object to compare to our current object
        :type other: any
        :return: True or False or NotImplemented
        :type: bool
        """
        if isinstance(other, PDFRaw):
            return self.raw == other.raw
        elif isinstance(other, bytes):
            return self.raw == other
        elif isinstance(other, PDFToken):
            return False
        else:
            return NotImplemented

    def pretty(self) -> str:
        return self._pretty("Raw(%d)" % (len(self.raw),))

    def encode(self) -> bytes:
        return self.raw
