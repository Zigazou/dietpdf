__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from .PDFItem import PDFItem

# Hints when there is no need to insert a space between two items when encoding.
NO_SPACE = {
    "": [
        "PDFNull", "PDFCommand", "PDFDictionary", "PDFList", "PDFName",
        "PDFString", "PDFHexString", "PDFReference", "PDFNumber"
    ],
    "PDFNumber": [
        "PDFCommand", "PDFNull", "PDFDictionary", "PDFList", "PDFName",
        "PDFString", "PDFHexString",
    ],
    "PDFList": [
        "PDFNull", "PDFCommand", "PDFDictionary", "PDFList", "PDFName",
        "PDFString", "PDFHexString", "PDFReference", "PDFNumber"
    ],
    "PDFDictionary": [
        "PDFNull", "PDFCommand", "PDFDictionary", "PDFList", "PDFName",
        "PDFString", "PDFHexString", "PDFReference", "PDFNumber"
    ],
    "PDFString": [
        "PDFNull", "PDFCommand", "PDFDictionary", "PDFList", "PDFName",
        "PDFString", "PDFHexString", "PDFReference", "PDFNumber"
    ],
    "PDFHexString": [
        "PDFNull", "PDFCommand", "PDFDictionary", "PDFList", "PDFName",
        "PDFString", "PDFHexString", "PDFReference", "PDFNumber"
    ],
    "PDFName": [
        "PDFDictionary", "PDFList", "PDFName", "PDFString", "PDFHexString",
    ],
    "PDFCommand": [
        "PDFDictionary", "PDFList", "PDFName", "PDFString", "PDFHexString",
    ],
    "PDFNull": [
        "PDFDictionary", "PDFList", "PDFName", "PDFString", "PDFHexString",
    ],
}


class PDFList(PDFItem):
    """A PDF list"""

    def __init__(self, items: list):
        if type(items) != list:
            items = [items]

        self.items = items

    def __eq__(self, other):
        if isinstance(other, PDFList):
            return self.items == other.items
        elif isinstance(other, list):
            return self.items == other
        elif isinstance(other, PDFItem):
            return False
        else:
            return NotImplemented

    def __bool__(self):
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
