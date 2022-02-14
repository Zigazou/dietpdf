__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from zlib import compress, decompress
from logging import getLogger

from sympy import O

from dietpdf.filter import zopfli_deflate

from dietpdf.token import PDFToken, PDFName, PDFNumber

from .content_stream import optimize_content_stream
from .PDFItem import PDFItem
from .PDFStream import PDFStream
from .PDFList import PDFList
from .PDFNull import PDFNull
from .PDFDictionary import PDFDictionary

_logger = getLogger("PDFObjectStream")

class PDFObjectStream(PDFItem):
    """A PDF object"""

    def __init__(self, obj_num: int, gen_num: int, objects: list):
        assert type(obj_num) == int
        assert type(gen_num) == int
        assert type(objects) == list

        self.obj_num = obj_num
        self.gen_num = gen_num
        self.objects = objects
        self.source_code = False

    def __bool__(self):
        """A PDFObjectStream is True if it has objects False otherwise.
        """
        return bool(self.objects)

    def __eq__(self, other):
        """Equality operator for PDFObject.

        A PDFObject is:

          - equal to any other PDFObject with the same object and generation
            numbers, the same value and the same stream
          - different from any other PDFToken subclass

        Comparing a PDFObject with anything else is not implemented.

        :param other: The object to compare to our current object
        :type other: any
        :return: True or False or NotImplemented
        :type: bool
        """
        if isinstance(other, PDFObjectStream):
            return (
                self.obj_num == other.obj_num and
                self.gen_num == other.gen_num and
                self.objects == other.objects
            )
        elif isinstance(other, PDFToken):
            return False
        else:
            return NotImplemented

    def __contains__(self, obj_num: int):
        """A PDFObjectStream implements the __contains__ method.

        An object stream is indexed by object number.
        """
        assert type(obj_num) == int

        return self.objects.__contains__(obj_num)

    def __getitem__(self, key: int):
        """A PDFObject implements the __getitem__ method when its value is a
        PDFDictionary.

        PDFDictionary keys are PDFName. If anything else than a PDFName is used,
        this method will try to convert it to a PDFNmae.

        It allows to directly use byte strings as key for example.

        Using this method on PDFObject having other values than PDFDictionary
        will lead to incorrect results or exceptions.
        """
        assert type(key) == int

        return self.objects.__getitem__(key)

    def pretty(self) -> str:
        return self._pretty(
            "ObjectStream(%d, %d) embedding %d objects" %
            (self.obj_num, self.gen_num, len(self.objects))
        )

    def encode(self) -> bytes:
        object_offsets = {}

        # Encode each embedded object (only their value).
        encoded_objects = {
            object.obj_num: object.value.encode()
            for object in self.objects
            if not object.has_stream()
        }

        # Create the stream of the object values.
        objects_stream = b"".join(
            [encoded_objects[object.obj_num] for object in self.objects]
        )

        # Calculate the offset of each object inside the stream.
        offset = 0
        for object in self.objects:
            object_offsets[object.obj_num] = offset
            offset += len(encoded_objects[object.obj_num])

        # Create the stream of the offsets.
        offsets_stream = b" ".join([
            b"%d %d" % (object.obj_num, object_offsets[object.obj_num])
            for object in self.objects
        ])

        first_offset = len(offsets_stream) + 1
        deflate_stream = zopfli_deflate(
            b"%s %s" % (offsets_stream, objects_stream)
        )

        return (
            b"%d %d obj<</Type/ObjStm/N %d/First %d/Filter/FlateDecode/Length %d>>"
            b"stream\n%s\nendstream\nendobj\n"
        ) % (
            self.obj_num, self.gen_num, len(self.objects), first_offset,
            len(deflate_stream), deflate_stream
        )
