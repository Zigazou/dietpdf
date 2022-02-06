__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from zlib import decompress

from .PDFItem import PDFItem

class PDFStream(PDFItem):
    """A PDF stream"""

    def __init__(self, stream: bytes):
        self.stream = stream

    def __bytes__(self):
        return self.stream

    def __bool__(self):
        return self.stream != None and len(self.stream) > 0

    def __eq__(self, other):
        if isinstance(other, PDFStream):
            return self.stream == other.stream
        elif isinstance(other, bytes):
            return self.stream == other
        elif isinstance(other, PDFItem):
            return False
        else:
            return NotImplemented

    def __len__(self):
        if self.stream != None:
            return self.stream.__len__()
        else:
            return 0

    def pretty(self) -> str:
        return self._pretty("Stream(%d)" % (len(self.stream),))

    def encode(self) -> bytes:
        return self.stream
