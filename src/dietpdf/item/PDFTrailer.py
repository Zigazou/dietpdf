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
        assert type(dictionary) == PDFDictionary

        self.dictionary = dictionary

    def __bool__(self):
        """A PDFTrailer is True if its dictionary has some elements, False
        otherwise.
        """
        return self.dictionary != None and bool(self.dictionary)

    def __eq__(self, other):
        """Equality operator for PDFTrailer.

        A PDFTrailer is:

          - equal to any other PDFTrailer with the same object and dictionary
          - equal to any dictionary with the same dictionary
          - different from any other PDFItem subclass

        Comparing a PDFTrailer with anything else is not implemented.

        :param other: The object to compare to our current object
        :type other: any
        :return: True or False or NotImplemented
        :type: bool
        """
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
