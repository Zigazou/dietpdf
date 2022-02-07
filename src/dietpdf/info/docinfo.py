__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

import logging

from ..item import PDFReference, PDFDictionary
from ..processor import PDFProcessor

_logger = logging.getLogger("content_objects")


def docinfo(pdf: PDFProcessor) -> dict:
    """Get info about a parsed PDF

    :param pdf PDFProcessor: 
    :return: A dictionary of informations about the PDF file
    :rtpe: dict
    """

    assert isinstance(pdf, PDFProcessor)

    info = {}

    # Look for root object
    root = None
    for object in pdf.stack:
        # Ignore non dictionary object
        if not isinstance(object.value, PDFDictionary):
            continue

        # Look for root object
        if b"Root" in object:
            root = object[b"Root"].obj_num
            break

    if root:
        root_object = pdf.objects[root]

        if b"Pages" in root_object:
            


    return info
