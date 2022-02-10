__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from .PDFToken import PDFToken


class PDFDictOpen(PDFToken):
    """Opening of a PDF dictionary (<<)

    A `PDFDictOpen` should be removed from the stack upon creation of a
    `PDFDictionary`.
    """

    def __eq__(self, other):
        """Equality operator for PDFDictOpen.

        A PDFDictOpen is:

          - equal to any other PDFDictOpen
          - different from any other PDFToken subclass

        Comparing a PDFDictOpen with anything else is not implemented.

        :param other: The object to compare to our current object
        :type other: any
        :return: True or False or NotImplemented
        :type: bool
        """
        if isinstance(other, PDFDictOpen):
            return True
        elif isinstance(other, PDFToken):
            return False
        else:
            return NotImplemented

    def __bool__(self):
        """A PDFDictOpen is always True"""
        return True

    def encode(self) -> bytes:
        return b"<<"
