__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from .PDFItem import PDFItem

class PDFXref(PDFItem):
    """A PDF cross-reference section"""

    def __init__(self):
        self.subsections = []
        self.first_entry_offset = None

    def __bool__(self):
        return self.subsections != None and len(self.subsections) > 0

    def __eq__(self, other):
        if isinstance(other, PDFXref):
            return self.subsections == other.subsections
        elif isinstance(other, list):
            return self.subsections == other
        elif isinstance(other, PDFItem):
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
