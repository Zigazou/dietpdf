__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from ..pdf.PDF import PDF
from ..item.PDFObject import PDFObject
from ..item.PDFDictionary import PDFDictionary
from ..item.PDFReference import PDFReference


def all_source_codes(pdf: PDF) -> list:
    """Find all source codes that could be optimized
    
    Source codes are contained in streams and are optimizable text content.
    :param pdf: The document to search for source codes in.
    :type pdf: PDF
    :return: A list of of object numbers
    :rtype: list
    """

    assert type(pdf) == PDF

    source_codes = set()

    # Find Form XObject
    any_form_xobject = lambda _, item: (
        type(item) == PDFObject and
        type(item.value) == PDFDictionary and
        b"Type" in item and
        item[b"Type"] == b"XObject" and
        b"Subtype" in item and
        item[b"Subtype"] == b"Form"
    )

    for _, object in pdf.find(any_form_xobject):
        source_codes.add(object.obj_num)

    # Find content streams
    any_contents = lambda _, item: (
        type(item) == PDFObject and
        type(item.value) == PDFDictionary and
        b"Contents" in item and
        type(item[b"Contents"]) == PDFReference
    )

    for _, object in pdf.find(any_contents):
        source_codes.add(object[b"Contents"].obj_num)

    # Find CMap
    any_cmap = lambda _, item: (
        type(item) == PDFObject and
        type(item.value) == PDFDictionary and
        b"Type" in item and item[b"Type"] == b"CMap"
    )

    for _, object in pdf.find(any_cmap):
        source_codes.add(object.obj_num)

    # Find ToUnicode streams
    any_tounicode = lambda _, item: (
        type(item) == PDFObject and
        type(item.value) == PDFDictionary and
        b"ToUnicode" in item and type(item[b"ToUnicode"]) == PDFReference
    )

    for _, object in pdf.find(any_tounicode):
        source_codes.add(object[b"ToUnicode"].obj_num)

    return list(source_codes)
