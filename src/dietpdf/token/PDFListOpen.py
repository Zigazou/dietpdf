__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from .PDFToken import PDFToken


class PDFListOpen(PDFToken):
    """Opening of a PDF list ([)

    A `PDFListOpen` should be removed from the stack upon creation of a
    `PDFList`.
    """

    def __eq__(self, other):
        """Equality operator for PDFListOpen.

        A PDFListOpen is:

          - equal to any other PDFListOpen
          - different from any other PDFToken subclass

        Comparing a PDFListOpen with anything else is not implemented.

        :param other: The object to compare to our current object
        :type other: any
        :return: True or False or NotImplemented
        :type: bool
        """
        if isinstance(other, PDFListOpen):
            return True
        elif isinstance(other, PDFToken):
            return False
        else:
            return NotImplemented

    def __bool__(self):
        """A PDFListOpen is always True."""
        return True

    def encode(self) -> bytes:
        return b"["
