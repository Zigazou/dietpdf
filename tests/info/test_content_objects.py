from dietpdf.item import (
    PDFObject, PDFDictionary, PDFReference, PDFName, PDFString
)

from dietpdf.info.content_objects import content_objects

__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"


def create_object_dictionary() -> dict:
    return {
        1: PDFObject(1, 0,
                     PDFDictionary({
                         PDFName(b"Contents"): PDFReference(2, 0)
                     }),
                     None
                     ),

        2: PDFObject(2, 0, PDFString(b"Object 2"), None),
        3: PDFObject(3, 0, PDFString(b"Object 3"), None),
        4: PDFObject(4, 0, PDFString(b"Object 4"), None),
        5: PDFObject(5, 0, PDFString(b"Object 5"), None),

        6: PDFObject(6, 0,
                     PDFDictionary({
                         PDFName(b"Dummy1"): PDFReference(4, 0),
                         PDFName(b"Dummy2"): PDFString(b"Dummy2")
                     }),
                     None
                     ),

        7: PDFObject(7, 0,
                     PDFDictionary({
                         PDFName(b"Contents"): PDFReference(3, 0)
                     }),
                     None
                     ),

        8: PDFObject(8, 0,
                     PDFDictionary({
                         PDFName(b"Contents"): PDFReference(3, 0)
                     }),
                     None
                     ),
    }


def test_content_objects():
    object_dictionary = create_object_dictionary()

    objects = content_objects(object_dictionary)

    assert 2 in objects
    assert 3 in objects
    assert not (4 in objects)
