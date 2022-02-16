__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from ..token.PDFToken import PDFToken

from .PDFItem import PDFItem


class PDFXref(PDFItem):
    """A PDF cross-reference section.

    It is composed of subsections of cross reference tables.
    """

    def __init__(self):
        self.subsections = []
        self.first_entry_offset = None

    def __bool__(self):
        """A PDFXref is True if it contains some subsections, False
        otherwise.
        """
        return self.subsections != None and len(self.subsections) > 0

    def __eq__(self, other):
        """Equality operator for PDFXref.

        A PDFXref is:

          - equal to any other PDFXref with the same subsections
          - equal to any list of subsections with the same subsections
          - different from any other PDFToken subclass

        Comparing a PDFXref with anything else is not implemented.

        :param other: The object to compare to our current object
        :type other: any
        :return: True or False or NotImplemented
        :type: bool
        """
        if isinstance(other, PDFXref):
            return self.subsections == other.subsections
        elif isinstance(other, list):
            return self.subsections == other
        elif isinstance(other, PDFToken):
            return False
        else:
            return NotImplemented

    def encode(self) -> bytes:
        output = b"xref\n"
        for subsection in self.subsections:
            output += subsection.encode()

        if len(self.subsections) > 0:
            self.first_entry_offset = (
                len(b"xref\n") + self.subsections[0].first_entry_offset
            )
        else:
            self.first_entry_offset = None

        return output

    def pretty(self) -> str:
        return self._pretty("XREF(%d)" % (len(self.subsections),))
