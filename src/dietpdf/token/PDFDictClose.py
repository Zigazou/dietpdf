__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from .PDFToken import PDFToken


class PDFDictClose(PDFToken):
    """Closing of a PDF dictionary (>>)

    Upon pushing on a stack, this item should initiate the creation of a
    `PDFDictionary`.
    """

    def __eq__(self, other):
        """Equality operator for PDFDictClose.

        A PDFDictClose is:

          - equal to any other PDFDictClose
          - different from any other PDFToken subclass

        Comparing a PDFDictClose with anything else is not implemented.

        :param other: The object to compare to our current object
        :type other: any
        :return: True or False or NotImplemented
        :type: bool
        """
        if isinstance(other, PDFDictClose):
            return True
        elif isinstance(other, PDFToken):
            return False
        else:
            return NotImplemented

    def __bool__(self):
        """A PDFDictClose is always True"""
        return True

    def encode(self) -> bytes:
        return b">>"
