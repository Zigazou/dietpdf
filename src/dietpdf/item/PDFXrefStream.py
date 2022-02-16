__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from math import log, ceil

from dietpdf.filter.zopfli import zopfli_deflate
from dietpdf.filter.predictor import (
    predictor_png_encode, PREDICTOR_PNG_UP, ROW_UP
)
from dietpdf.token import PDFToken

from .PDFItem import PDFItem


class PDFXrefStream(PDFItem):
    """A PDF cross-reference stream.
    """

    def __init__(self, obj_num: int, gen_num: int, references: dict):
        assert type(obj_num) == int
        assert type(gen_num) == int
        assert type(references) == dict

        self.obj_num = obj_num
        self.gen_num = gen_num
        self.source_code = False
        self.references = references
        self.trailer_info = None
        self.trailer_root = None
        self.first_entry_offset = None

    def __bool__(self):
        """A PDFXrefStream is True if it contains some references, False
        otherwise.
        """
        return bool(self.references)

    def __eq__(self, other):
        """Equality operator for PDFXref.

        A PDFXrefStream is:

          - equal to any other PDFXrefStream with the same references
          - different from any other PDFToken subclass

        Comparing a PDFXrefStream with anything else is not implemented.

        :param other: The object to compare to our current object
        :type other: any
        :return: True or False or NotImplemented
        :type: bool
        """
        if isinstance(other, PDFXrefStream):
            return self.references == other.references
        elif isinstance(other, PDFToken):
            return False
        else:
            return NotImplemented

    def calculate_stats(self) -> dict:
        count_entry_types = [0, 0, 0]
        min_obj_num = 2 ** 32
        max_obj_num = 0
        max_offset = 0
        max_position = 0

        for obj_num in self.references:
            entry_type, offset, position = self.references[obj_num]
            count_entry_types[entry_type] += 1
            min_obj_num = min(obj_num, min_obj_num)
            max_obj_num = max(obj_num, max_obj_num)
            max_offset = max(offset, max_offset)
            max_position = max(position, max_position)

        return {
            "min_obj_num": min_obj_num,
            "max_obj_num": max_obj_num,
            "field_sizes": (
                # O, 1 and 2 are the only allowed values, 1 byte is enough.
                1,
                max(1, ceil(log(max_offset + 1, 2) / 8)),
                max(1, ceil(log(count_entry_types[2] + 1, 2) / 8))
            )
        }

    def encode(self) -> bytes:
        # Define field sizes.
        stats = self.calculate_stats()
        field_1_size, field_2_size, field_3_size = stats["field_sizes"]
        columns = field_1_size + field_2_size + field_3_size

        # Update free reference entries.
        next_free = stats["max_obj_num"] + 2
        for index in range(len(self.references) - 1, -1, -1):
            entry_type, offset, position = self.references[index]

            if entry_type != 0:
                continue

            self.references[index] = (entry_type, next_free, 0)
            next_free = index

        # Formats references.
        references_encoded = bytearray(len(self.references) * columns)
        for index in range(len(self.references)):
            entry_type, offset, position = self.references[index]
            references_encoded[index * columns:index * (columns + 1)] = (
                b"%c%s%s" % (
                    entry_type,
                    offset.to_bytes(field_2_size, "big"),
                    position.to_bytes(field_3_size, "big")
                )
            )

        # Use predictor ROW_UP to optimize compression.
        references_predicted = predictor_png_encode(
            bytes(references_encoded), ROW_UP, columns, 1
        )

        # Compresses the references.
        references_deflated = zopfli_deflate(references_predicted)

        return (
            b"%d %d obj<</Type/XRef"
            b"/Index[%d %d]"
            b"/Size %d"
            b"/W[%d %d %d]"
            b"/Filter/FlateDecode"
            b"/DecodeParms<</Predictor %d/Columns %d>>"
            b"/Root %s/Info %s"
            b"/Length %d"
            b">>"
            b"stream\n%s\nendstream\nendobj\n"
        ) % (
            self.obj_num, self.gen_num,
            stats["min_obj_num"],
            stats["max_obj_num"] - stats["min_obj_num"] + 1,
            stats["max_obj_num"] + 1,
            field_1_size, field_2_size, field_3_size,
            PREDICTOR_PNG_UP, columns,
            self.trailer_root.encode(), self.trailer_info.encode(),
            len(references_deflated),
            references_deflated
        )

    def pretty(self) -> str:
        return self._pretty("XRefStream(%d)" % (len(self.references),))
