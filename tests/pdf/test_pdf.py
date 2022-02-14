__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

import pytest

from dietpdf.token import PDFName, PDFString, PDFNumber, PDFComment
from dietpdf.item import (
    PDFObject, PDFDictionary, PDFReference, PDFList, PDFNull
)

from dietpdf.pdf.PDF import PDF


def create_objects() -> list:
    return [
        PDFObject(1, 0,
                  PDFDictionary({
                      PDFName(b"Contents"): PDFReference(2, 0),
                      PDFName(b"Dummy1"): PDFReference(7, 0)
                  }),
                  None
                  ),

        PDFObject(2, 0, PDFString(b"Object 2"), None),
        PDFObject(3, 0, PDFString(b"Object 3"), None),
        PDFObject(4, 0, PDFString(b"Object 4"), None),
        PDFObject(5, 0, PDFString(b"Object 5"), None),

        PDFObject(6, 0,
                  PDFDictionary({
                      PDFName(b"Dummy1"): PDFReference(4, 0),
                      PDFName(b"Dummy2"): PDFString(b"Dummy2")
                  }),
                  None
                  ),

        PDFObject(7, 0,
                  PDFDictionary({
                      PDFName(b"Contents"): PDFReference(3, 0)
                  }),
                  None
                  ),

        PDFObject(8, 0,
                  PDFDictionary({
                      PDFName(b"Contents"): PDFReference(3, 0),
                      PDFName(b"A"): PDFDictionary({
                          PDFName(b"URI"): PDFString(b"http://example.com")
                      })
                  }),
                  None
                  ),
        PDFObject(9, 0,
                  PDFList([
                      PDFNumber(0),
                      PDFNumber(1),
                      PDFNumber(2),
                      PDFNumber(3),
                      PDFNumber(4),
                      PDFNumber(5),
                  ]),
                  None
                  ),
        PDFObject(10, 0,
                  PDFList([
                      PDFReference(1, 0),
                      PDFReference(2, 0),
                      PDFReference(3, 0),
                      PDFReference(4, 0),
                      PDFReference(5, 0),
                  ]),
                  None
                  ),
        PDFObject(11, 0,
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
    ]


def test_pdf_get():
    all_objects = create_objects()
    pdf = PDF()

    # Add all objects to the PDF.
    for object in all_objects:
        pdf.push(object)

    assert len(pdf.objects) == len(all_objects)

    # Without path.
    with pytest.raises(ValueError):
        _ = pdf.get("Dummy")
    assert pdf.get(0) == None
    assert pdf.get(2).value == b"Object 2"
    assert pdf.get(7).obj_num == 7
    assert pdf.get(PDFReference(7, 0)).obj_num == 7

    # With path.
    assert pdf.get(0, [1, 2, 3]) == None
    assert pdf.get(7, ["Contents"]).value == b"Object 3"
    assert pdf.get(1, ["Dummy1", "Contents"]).value == b"Object 3"
    assert pdf.get(1, ["Dummy1", "Dummy2", "Dummy3"]) == None
    assert pdf.get(6, ["Dummy2"]).string == b"Dummy2"
    assert pdf.get(7, ["Contents"]) == pdf.get(8, ["Contents"])
    assert pdf.get(9, [2]) == PDFNumber(2)
    assert pdf.get(8, ["A", "URI"]) == b"http://example.com"
    assert pdf.get(11, ["A", "URI"]) == b"http://example.com/2"

    assert pdf.get(10, [0]).obj_num == 1
    assert pdf.get(10, [0, "Dummy1"]).obj_num == 7
    assert pdf.get(10, [0, "Dummy1", "Contents"]).value == b"Object 3"


def test_pdf_push_pop():
    pdf = PDF()

    # Push duplicated comments, no exception should occur.
    comment = PDFComment(b"Hello world!")
    pdf.push(comment)
    pdf.push(comment)

    # Can only push PDFItem or any subclass
    with pytest.raises(TypeError):
        pdf.push(3)

    # Push one object.
    null_object1 = PDFObject(1, 0, PDFNull(), None)
    null_object2 = PDFObject(2, 0, PDFNull(), None)
    pdf.push(null_object1)
    assert len(pdf.objects) == 1

    count_before = len(pdf.objects)
    pdf.push(null_object1)
    count_after = len(pdf.objects)
    assert count_before == count_after

    pdf.push(null_object2)
    assert len(pdf.objects) == 2

    # Pop one object.
    popped_object = pdf.pop()
    assert popped_object == null_object2
    assert len(pdf.objects) == 1
    assert pdf.get(1) == null_object1


def test_pdf_find():
    def any_comment(_, item): return type(item) == PDFComment

    all_objects = create_objects()
    pdf = PDF()

    # Add all objects to the PDF.
    for object in all_objects:
        pdf.push(object)

    with pytest.raises(TypeError):
        for _ in pdf.find(2022):
            continue

    # Add comments
    for comment_count in range(1, 10):
        pdf.push(PDFComment(b"Comment %d" % comment_count))

        for _, item in pdf.find(any_comment):
            assert type(item) == PDFComment

        comments = [comment for _, comment in pdf.find(any_comment)]
        assert len(comments) == comment_count

    # Check last comment
    assert pdf.find_all(any_comment)[-1].content == b"Comment 9"

    # Find first comment
    assert pdf.find_first(any_comment).content == b"Comment 1"


def test_pdf_push_pop_insert():
    def any_string(_, item): return (
        type(item) == PDFObject and
        type(item.value) == PDFString
    )

    all_objects = create_objects()
    pdf = PDF()

    # Add all objects to the PDF.
    for object in all_objects:
        pdf.push(object)

    # Replace consecutive PDFString with a PDFComment
    for index, _ in pdf.find(any_string):
        while any_string(0, pdf.stack_at(index)):
            pdf.pop(index)

        pdf.insert(index, PDFComment(b"Comment"))

    assert len(pdf.find_all(any_string)) == 0
