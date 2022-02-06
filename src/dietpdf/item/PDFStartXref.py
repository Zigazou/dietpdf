__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from .PDFItem import PDFItem

class PDFStartXref(PDFItem):
    """A PDF startxref"""

    def __init__(self, offset: int):
        self.offset = offset

    def __bool__(self):
        return self.offset != None and self.offset != 0

    def __eq__(self, other):
        if isinstance(other, PDFStartXref):
            return self.offset == other.offset
        elif isinstance(other, int):
            return self.offset == other
        elif isinstance(other, PDFItem):
            return False
        else:
            return NotImplemented

    def pretty(self) -> str:
        return self._pretty("StartXref(%d)" % (self.offset,))

    def encode(self) -> bytes:
        return b"startxref\n%d\n" % (self.offset,)
