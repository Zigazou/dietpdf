__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from dietpdf.token import PDFToken

from .PDFItem import PDFItem


class PDFStartXref(PDFItem):
    """A PDF startxref"""

    def __init__(self, offset: int):
        assert type(offset) == int
        self.offset = offset

    def __bool__(self):
        """A PDFStartXref is always True."""
        return True

    def __eq__(self, other):
        """Equality operator for PDFStartXref.

        A PDFStartXref is:

          - equal to any other PDFStartXref with the same offset
          - equal to any int with the same value as the offset
          - different from any other PDFToken subclass

        Comparing a PDFStartXref with anything else is not implemented.

        :param other: The object to compare to our current object
        :type other: any
        :return: True or False or NotImplemented
        :type: bool
        """
        if isinstance(other, PDFStartXref):
            return self.offset == other.offset
        elif isinstance(other, int):
            return self.offset == other
        elif isinstance(other, PDFToken):
            return False
        else:
            return NotImplemented

    def pretty(self) -> str:
        return self._pretty("StartXref(%d)" % (self.offset,))

    def encode(self) -> bytes:
        return b"startxref\n%d\n" % (self.offset,)
