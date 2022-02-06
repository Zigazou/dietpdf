__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from .PDFItem import PDFItem
from .PDFDictionary import PDFDictionary

class PDFTrailer(PDFItem):
    """A PDF trailer"""

    def __init__(self, dictionary: PDFDictionary):
        self.dictionary = dictionary

    def __bool__(self):
        return self.dictionary != None and self.dictionary

    def __eq__(self, other):
        if isinstance(other, PDFTrailer):
            return self.dictionary == other.dictionary
        elif isinstance(other, dict):
            return self.dictionary == other
        elif isinstance(other, PDFItem):
            return False
        else:
            return NotImplemented

    def encode(self) -> bytes:
        return b"trailer\n" + self.dictionary.encode() + b"\n"
