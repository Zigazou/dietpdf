__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from dietpdf.token import PDFToken

from .PDFItem import PDFItem


class PDFNull(PDFItem):
    """A null value (null)."""

    def __eq__(self, other):
        """Equality operator for PDFNull.

        A PDFNull is:

          - equal to any other PDFNull
          - different from any other PDFToken subclass

        Comparing a PDFNull with anything else is not implemented.

        :param other: The object to compare to our current object
        :type other: any
        :return: True or False or NotImplemented
        :type: bool
        """
        if isinstance(other, PDFNull) or other == None:
            return True
        elif isinstance(other, PDFToken):
            return False
        else:
            return NotImplemented

    def __bool__(self):
        """A PDFNull is always False."""
        return False

    def encode(self) -> bytes:
        return b"null"
