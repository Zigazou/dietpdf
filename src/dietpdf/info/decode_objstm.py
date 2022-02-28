__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from logging import getLogger

from ..parser.PDFParser import PDFParser
from ..processor.PDFProcessor import PDFProcessor
from ..item.PDFObject import PDFObject
from ..item.PDFDictionary import PDFDictionary
from ..item.PDFObjectStream import PDFObjectStream
from ..pdf.PDF import PDF

_logger = getLogger("decode_objstm")


def decode_objstm(stream: bytes, first: int) -> list:
    """Decodes an object stream into a list of objects.

    :param stream: The stream to decode
    :type stream: bytes
    :param first: The offset of the first object inside the stream
    :type first: int
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

    # Find objects without stream.
    def any_object_without_stream(_, item):
        if type(item) != PDFObject:
            return False

        if item.has_stream():
            return False

        if type(item.value) == PDFDictionary:
            if b"Linearized" in item:
                return False

        return True

    object_indices = {
        item.obj_num: index 
        for index, item in pdf.find(any_object_without_stream)
    }

    # Decode Objects stream
    def any_objstm(_, item):
        return (
            type(item) == PDFObject and
            type(item.value) == PDFDictionary and
            b"Type" in item and item[b"Type"] == b"ObjStm"
        )

    # Add the embedded objects to the stack.
    to_remove = []
    for index, item in pdf.find(any_objstm):
        to_remove.append(index)
        _logger.debug("Decoding object stream %d" % item.obj_num)
        objects = decode_objstm(item.decode_stream(), int(item[b"First"]))
        for object in objects:
            if object.obj_num in object_indices:
                # Make sure the object won't replace a newer object version.
                if object_indices[object.obj_num] < index:
                    object_indices[object.obj_num] = index
                    pdf.push(object)
            else:
                object_indices[object.obj_num] = index
                pdf.push(object)


    # Remove the objects streams.
    to_remove.sort(reverse=True)
    for index in to_remove:
        pdf.pop(index)


def create_objstm(pdf: PDF) -> int:
    """Groups all objects without stream to form an object stream.

    Once the object stream has been created, the objects are removed.

    :param pdf: The PDF file for which to convert objects streams.
    :type pdf: PDF
    :return: The object number of the object stream created
    :rtype: int
    """

    # Find the highest object number to attribute it to the new object stream.
    highest_object_number = 0

    def any_object(_, item):
        return type(item) == PDFObject

    for _, item in pdf.find(any_object):
        highest_object_number = max(item.obj_num, highest_object_number)

    # Find objects without stream.
    def any_object_without_stream(_, item):
        if type(item) != PDFObject:
            return False

        if item.has_stream():
            return False

        if type(item.value) == PDFDictionary:
            if b"Linearized" in item:
                return False

        return True

    # Move objects without stream to the object stream.
    objects = []
    to_remove = []
    for index, item in pdf.find(any_object_without_stream):
        objects.append(item)
        to_remove.append(index)

    to_remove.sort(reverse=True)
    for index in to_remove:
        pdf.pop(index)

    pdf.push(PDFObjectStream(highest_object_number + 1, 0, objects))

    return highest_object_number + 1
