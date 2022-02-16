__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from ..token.PDFToken import PDFToken

from .PDFItem import PDFItem

# Hints when there is no need to insert a space between two items when encoding.
NO_SPACE = {
    "": [
        "PDFNull", "PDFCommand", "PDFList", "PDFList", "PDFName",
        "PDFString", "PDFHexString", "PDFReference", "PDFNumber"
    ],
    "PDFNumber": [
        "PDFCommand", "PDFNull", "PDFList", "PDFList", "PDFName",
        "PDFString", "PDFHexString",
    ],
    "PDFList": [
        "PDFNull", "PDFCommand", "PDFList", "PDFList", "PDFName",
        "PDFString", "PDFHexString", "PDFReference", "PDFNumber"
    ],
    "PDFList": [
        "PDFNull", "PDFCommand", "PDFList", "PDFList", "PDFName",
        "PDFString", "PDFHexString", "PDFReference", "PDFNumber"
    ],
    "PDFString": [
        "PDFNull", "PDFCommand", "PDFList", "PDFList", "PDFName",
        "PDFString", "PDFHexString", "PDFReference", "PDFNumber"
    ],
    "PDFHexString": [
        "PDFNull", "PDFCommand", "PDFList", "PDFList", "PDFName",
        "PDFString", "PDFHexString", "PDFReference", "PDFNumber"
    ],
    "PDFName": [
        "PDFList", "PDFList", "PDFName", "PDFString", "PDFHexString",
    ],
    "PDFCommand": [
        "PDFList", "PDFList", "PDFName", "PDFString", "PDFHexString",
    ],
    "PDFNull": [
        "PDFList", "PDFList", "PDFName", "PDFString", "PDFHexString",
    ],
}


class PDFList(PDFItem):
    """A PDF list"""

    def __init__(self, items: list):
        """Creates a PDF list.

        If the items parameter is not a list, it is placed in a list that will
        become the list of the PDFList object.

        :param items: The items of the list
        :type items: list or other type
        """
        if type(items) != list:
            items = [items]

        self.items = items

    def __eq__(self, other):
        """Equality operator for PDFList.

        A PDFList is:

          - equal to any other PDFList with the same list
          - equal to list with the same list
          - different from any other PDFToken subclass

        Comparing a PDFList with anything else is not implemented.

        :param other: The object to compare to our current object
        :type other: any
        :return: True or False or NotImplemented
        :type: bool
        """
        if isinstance(other, PDFList):
            return self.items == other.items
        elif isinstance(other, list):
            return self.items == other
        elif isinstance(other, PDFToken):
            return False
        else:
            return NotImplemented

    def __bool__(self):
        """A PDFList is True if it contains items, False otherwise."""
        return self.items != None and len(self.items) > 0

    def __len__(self):
        return self.items.__len__()

    def __getitem__(self, items):
        return self.items.__getitem__(items)

    def __iter__(self):
        return self.items.__iter__()

    def __next__(self):
        return self.items.__next__()

    def encode(self) -> bytes:
        output = b"["

        previous = ""
        for value in self.items:
            current = value.__class__.__name__

            if previous in NO_SPACE and current in NO_SPACE[previous]:
                output += b"%s" % value.encode()
            else:
                output += b" %s" % value.encode()

            previous = current

        output += b"]"

        return output
