__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from .PDFItem import PDFItem

class PDFNumber(PDFItem):
    """A PDF number (either an integer or a float)"""

    def __init__(self, value: bytes):
        if type(value) == float or type(value) == int:
            self.value = value
        elif ord('.') in value:
            self.value = float(value)
        else:
            self.value = int(value)

    def __eq__(self, other):
        if isinstance(other, PDFNumber):
            return self.value == other.value
        elif isinstance(other, int) or isinstance(other, float):
            return self.value == other
        elif isinstance(other, PDFItem):
            return False
        else:
            return NotImplemented

    def __int__(self) -> int:
        return int(self.value)

    def __float__(self) -> float:
        return float(self.value)

    def __bool__(self):
        return self.value != None and float(self.value) != 0.0

    def pretty(self) -> str:
        return self._pretty("Number(%s)" % (self.value,))

    def encode(self) -> bytes:
        return str(self.value).encode('ascii')
