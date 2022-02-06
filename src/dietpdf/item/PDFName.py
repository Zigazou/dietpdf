__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from .PDFItem import PDFItem

class PDFName(PDFItem):
    """A PDF name (starting with /)"""

    def __init__(self, name: bytes):
        self.name = name

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, PDFName):
            return self.name == other.name
        elif isinstance(other, bytes):
            return self.name == other
        elif isinstance(other, PDFItem):
            return False
        else:
            return NotImplemented

    def __str__(self) -> str:
        return self.name.decode('ascii')

    def __bool__(self):
        return self.name != None and len(self.name) > 0

    def pretty(self) -> str:
        return self._pretty("Name(%s)" % (self.name.decode('ascii'),))

    def encode(self) -> bytes:
        return b"/" + self.name
