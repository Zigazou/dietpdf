__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from .PDFItem import PDFItem


class PDFListClose(PDFItem):
    """Closing of a PDF list (])

    Upon pushing on a stack, this item should initiate the creation of a
    `PDFList`.
    """

    def __eq__(self, other):
        """Equality operator for PDFListClose.

        A PDFListClose is:

          - equal to any other PDFListClose
          - different from any other PDFItem subclass

        Comparing a PDFListClose with anything else is not implemented.

        :param other: The object to compare to our current object
        :type other: any
        :return: True or False or NotImplemented
        :type: bool
        """
        if isinstance(other, PDFListClose):
            return True
        elif isinstance(other, PDFItem):
            return False
        else:
            return NotImplemented

    def __bool__(self):
        """A PDFListClose is always True."""
        return True
