__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from dietpdf.parser.PDFParser import PDFParser
from dietpdf.processor.PDFProcessor import PDFProcessor
from dietpdf.item import PDFObject, PDFDictionary
from dietpdf.pdf import PDF


def decode_objstm(stream: bytes, first: int) -> list:
    """Convert a hexadecimal string to a byte string.

    This allows to render space-friendly byte strings when encoding.

    :param hexstring: The hexadecimal string to convert
    :type hexstring: bytes
    :return: The converted string
    :rtype: bytes
    """

    assert type(stream) == bytes
    assert type(first) == int

    # Parse object number and relative offsets.
    processor = PDFProcessor()
    PDFParser(processor).parse(stream[:first])

    obj_nums = [
        processor.tokens.stack_at(index)
        for index in range(0, processor.tokens.stack_size(), 2)
    ]

    # Retrieve objects
    processor = PDFProcessor()
    PDFParser(processor).parse(stream[first:])

    return [
        PDFObject(
            int(obj_nums[index]),
            0,
            processor.tokens.stack_at(index),
            None
        )
        for index in range(len(obj_nums))
    ]


def convert_objstm(pdf: PDF):
    """Converts the Objects streams contained in a PDF document.

    The conversion adds objects extracted from all the objects streams at the
    end of the stack.

    Once objects have been extracted, the objects streams are removed.

    :param pdf: The PDF file for which to convert objects streams.
    :type pdf: PDF
    """
    # Decode Objects stream
    def any_objstm(_, item):
        return (
            type(item) == PDFObject and
            type(item.value) == PDFDictionary and
            b"Type" in item and item[b"Type"] == b"ObjStm"
        )

    # Add the embedded objects to the stack.
    for _, item in pdf.find(any_objstm):
        objects = decode_objstm(item.decode_stream(), int(item[b"First"]))
        for object in objects:
            pdf.push(object)

    # Remove the objects streams.
    for index, _ in pdf.find(any_objstm):
        pdf.pop(index)
