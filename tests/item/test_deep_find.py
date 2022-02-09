import pytest

from dietpdf.item import (
    deep_find, PDFObject, PDFDictionary, PDFName, PDFString, PDFNumber,
    PDFList, PDFItem
)

__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"


def create_object() -> PDFObject:
    return PDFObject(11, 0,
                     PDFDictionary({
                         PDFName(b"Type"): PDFName(b"Annot"),
                         PDFName(b"Subtype"): PDFName(b"Link"),
                         PDFName(b"Border"): PDFList([
                             PDFNumber(0), PDFNumber(0), PDFNumber(0)
                         ]),
                         PDFName(b"Rect"): PDFList([
                             PDFNumber(56.693), PDFNumber(743.789),
                             PDFNumber(170.407), PDFNumber(757.589),
                         ]),
                         PDFName(b"A"): PDFDictionary({
                             PDFName(b"Type"): PDFName(b"Action"),
                             PDFName(b"S"): PDFName(b"URI"),
                             PDFName(b"URI"): PDFString(b"http://example.com/2"),
                         }),
                         PDFName(b"StructParent"): PDFNumber(2),
                     }),
                     None
                     )


def test_deep_find_number():
    object = create_object()

    def any_number(path: list, item: PDFItem) -> bool:
        return type(item) == PDFNumber

    all_numbers = deep_find(object, any_number)
    print(all_numbers)
    assert len(all_numbers) == 8

def test_deep_find_string():
    object = create_object()

    def any_string(path: list, item: PDFItem) -> bool:
        return type(item) == PDFString

    all_strings = deep_find(object, any_string)
    print(all_strings)
    assert len(all_strings) == 1
    assert all_strings[0][1] == b"http://example.com/2"
    assert all_strings[0][0] == ["A", "URI"]

def test_deep_find_uri():
    object = create_object()

    def any_uri(path: list, item: PDFItem) -> bool:
        return type(item) == PDFString and path and path[-1] == "URI"

    all_uri = deep_find(object, any_uri)
    print(all_uri)
    assert len(all_uri) == 1
    assert all_uri[0][1] == b"http://example.com/2"
    assert all_uri[0][0] == ["A", "URI"]

def test_deep_find_dummy():
    object = create_object()

    def any_name_dummy(path: list, item: PDFItem) -> bool:
        return type(item) == PDFName and item == b"Dummy"

    all_name_dummy = deep_find(object, any_name_dummy)
    assert len(all_name_dummy) == 0
