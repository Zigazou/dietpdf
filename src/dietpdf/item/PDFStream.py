__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from zlib import decompress

from dietpdf.token import PDFToken

from .PDFItem import PDFItem


class PDFStream(PDFItem):
    """A PDF stream"""

    def __init__(self, stream: bytes):
        assert type(stream) == bytes

        self.stream = stream

    def __bytes__(self):
        return self.stream

    def __bool__(self):
        return self.stream != None and len(self.stream) > 0

    def __eq__(self, other):
        """Equality operator for PDFStream.

        A PDFStream is:

          - equal to any other PDFStream with the same byte string
          - equal to any byte string with the same byte string
          - different from any other PDFToken subclass

        Comparing a PDFStream with anything else is not implemented.

        :param other: The object to compare to our current object
        :type other: any
        :return: True or False or NotImplemented
        :type: bool
        """
        if isinstance(other, PDFStream):
            return self.stream == other.stream
        elif isinstance(other, bytes):
            return self.stream == other
        elif isinstance(other, PDFToken):
            return False
        else:
            return NotImplemented

    def __len__(self):
        if self.stream:
            return self.stream.__len__()
        else:
            return 0

    def pretty(self) -> str:
        return self._pretty("Stream(%d)" % (len(self.stream),))

    def encode(self) -> bytes:
        return self.stream
