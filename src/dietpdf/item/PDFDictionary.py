__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from ..token.PDFToken import PDFToken
from ..token.PDFName import PDFName

from .PDFItem import PDFItem


# Hints when there is no need to insert a space between a PDFName and a value
# when encoding.
NO_SPACE = [
    "PDFDictionary", "PDFList", "PDFName", "PDFString", "PDFHexString",
]


class PDFDictionary(PDFItem):
    """A PDF dictionary"""

    def __init__(self, items: dict):
        assert type(items) == dict

        self.items = items

    def __bool__(self):
        """A PDFDictionary is True it contains elements, False otherwise."""
        return self.items != None and len(self.items) > 0

    def __eq__(self, other):
        """Equality operator for PDFDictionary.

        A PDFDictionary is:

          - equal to any other PDFDictionary with the same dictionary
          - equal to dictionary with the same dictionary
          - different from any other PDFToken subclass

        Comparing a PDFDictionary with anything else is not implemented.

        :param other: The object to compare to our current object
        :type other: any
        :return: True or False or NotImplemented
        :type: bool
        """
        if isinstance(other, PDFDictionary):
            return self.items == other.items
        elif isinstance(other, dict):
            return self.items == other
        elif isinstance(other, PDFToken):
            return False
        else:
            return NotImplemented

    def __contains__(self, key):
        """Check if a key is contained in a PDFDictionary.

        PDFDictionary keys are PDFName. If anything else than a PDFName is used,
        this method will try to convert it to a PDFNmae.

        It allows to directly use byte strings as key for example.
        """
        if not isinstance(key, PDFName):
            key = PDFName(key)

        return self.items.__contains__(key)

    def __getitem__(self, key):
        """Retrieve entry in a PDFDictionary given its key.

        PDFDictionary keys are PDFName. If anything else than a PDFName is used,
        this method will try to convert it to a PDFNmae.

        It allows to directly use byte strings as key for example.
        """
        if not isinstance(key, PDFName):
            key = PDFName(key)

        return self.items.__getitem__(key)

    def __setitem__(self, key, value):
        """Set entry in a PDFDictionary given its key.

        PDFDictionary keys are PDFName. If anything else than a PDFName is used,
        this method will try to convert it to a PDFNmae.

        It allows to directly use byte strings as key for example.
        """
        if not isinstance(key, PDFName):
            key = PDFName(key)

        self.items.__setitem__(key, value)

    def __iter__(self):
        return self.items.__iter__()

    def __next__(self):
        return self.items.__next__()

    def encode(self) -> bytes:
        output = b"<<"

        for key in self.items:
            value = self.items[key]

            if value.__class__.__name__ in NO_SPACE:
                output += b"%s%s" % (key.encode(), value.encode())
            else:
                output += b"%s %s" % (key.encode(), value.encode())

        output += b">>"

        return output
