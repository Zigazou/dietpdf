__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from zlib import compress, decompress
from logging import getLogger

from .PDFItem import PDFItem
from .PDFName import PDFName
from .PDFStream import PDFStream
from .PDFList import PDFList
from .PDFNull import PDFNull
from .PDFNumber import PDFNumber
from .PDFDictionary import PDFDictionary
from ..filter.zopfli import zopfli_deflate
from ..filter.rle import rle_encode
from ..filter.predictor import predictor_png_decode, predictor_png_encode
from ..filter.jpegoptim import jpegtran_optimize

_logger = getLogger("PDFObject")

NO_SPACE = ["PDFDictionary", "PDFList", "PDFString", "PDFHexString"]

class PDFObject(PDFItem):
    """A PDF object"""

    def __init__(self, obj_num: int, gen_num: int, value, stream: PDFStream):
        self.obj_num = obj_num
        self.gen_num = gen_num
        self.value = value
        self.stream = stream
        self.source_code = False

    def __bool__(self):
        return self.value != None and self.value

    def __eq__(self, other):
        if isinstance(other, PDFObject):
            return (
                self.obj_num == other.obj_num and
                self.gen_num == self.gen_num and
                self.value == other.value and
                self.stream == other.stream
            )
        elif isinstance(other, PDFItem):
            return False
        else:
            return NotImplemented

    def __contains__(self, key):
        if not isinstance(key, PDFName):
            key = PDFName(key)

        return self.value.__contains__(key)

    def __getitem__(self, key):
        if isinstance(self.value, PDFDictionary):
            return self.value.__getitem__(key)
        elif isinstance(self.value, PDFList):
            return self.value.__getitem__(key)
        else:
            raise TypeError()

    def has_stream(self) -> bool:
        return self.stream != None

    def pretty(self) -> str:
        if self.value != None:
            return self._pretty(
                "Object(%d, %d)+stream" % (self.obj_num, self.gen_num)
            )
        else:
            return self._pretty("Object(%d, %d)" % (self.obj_num, self.gen_num))

    def encode(self) -> bytes:
        if self.value.__class__.__name__ in NO_SPACE:
            output = b"%d %d obj%s" % (
                self.obj_num, self.gen_num, self.value.encode()
            )
        else:
            output = b"%d %d obj %s" % (
                self.obj_num, self.gen_num, self.value.encode()
            )

        if self.stream != None:
            output += b"stream\n%sendstream\nendobj\n" % self.stream.encode()
        elif self.value.__class__.__name__ in NO_SPACE:
            output += b"endobj\n"
        else:
            output += b"\nendobj\n"

        return output

    def has_type(self, name: str) -> bool:
        if isinstance(self.value, PDFDictionary):
            return False

        item_type = PDFName(b"Type")
        if item_type in self.value.items:
            return self.value.items[item_type] == PDFName(name.encode('ascii'))

    def has_key_value(self, key: bytes, value: bytes) -> bool:
        if isinstance(self.value, PDFDictionary):
            return False

        pdf_key = PDFName(key)
        pdf_value = PDFName(value)
        if pdf_key in self.value.items:
            pdf_item_value = self.value.items[pdf_key]
            if isinstance(pdf_item_value, PDFList):
                return pdf_value in pdf_item_value
            else:
                return pdf_item_value == pdf_value

    def get_value(self, key: bytes):
        if not isinstance(self.value, PDFDictionary):
            return None

        pdf_key = PDFName(key)
        if pdf_key in self.value.items:
            return self.value.items[pdf_key]
        else:
            return None

    def decode_stream(self) -> bytes:
        if not self.has_stream():
            return b""

        # Retrieve filter(s)
        filters = self.get_value(b"Filter")
        if filters == None:
            # The stream needs not to be filtered
            return self.stream.stream

        # Convert the filter to a PDFList of filters
        if not isinstance(filters, PDFList):
            filters = PDFList(filters)

        # Retrieve decode parameters
        try:
            decode_parms = self[b"DecodeParms"]
            if not isinstance(decode_parms, PDFList):
                decode_parms = PDFList(decode_parms)
        except KeyError:
            decode_parms = PDFList(PDFNull())

        # Apply filters
        output = bytes(self.stream)
        for (filter, parms) in zip(filters, decode_parms):
            if filter == b"FlateDecode":
                try:
                    output = decompress(output)
                except:
                    raise Exception(
                        "Unable to decompress object %d stream" % self.obj_num
                    )

                if parms:
                    columns = parms[b"Columns"].value

                    if b"Colors" in parms:
                        colors = parms[b"Colors"].value
                    else:
                        colors = 1
                    output = predictor_png_decode(output, columns, colors)

        return output

    def optimize_stream(self):
        if not self.has_stream():
            return b""

        stream = self.decode_stream()

        # Replacing line returns by space helps compression.
        if self.source_code:
            _logger.debug(
                "Optimize source code on object %d" % self.obj_num
            )
            stream = stream.replace(b"\n", b" ")

        key_dct_decode = PDFName(b"DCTDecode")
        key_flate_decode = PDFName(b"FlateDecode")
        key_rle_decode = PDFName(b"RunLengthDecode")

        # Retrieve filter(s)
        filters = self.get_value(b"Filter")
        if filters == None:
            filters = []

        # Convert the filter to a PDFList of filters
        if not isinstance(filters, PDFList):
            filters = PDFList(filters)

        # Retrieve decode parameters
        decode_parms = self.get_value(b"DecodeParms")
        if len(filters) == 0:
            decode_parms = PDFList([])
        elif decode_parms == None:
            decode_parms = PDFList(PDFNull())
        elif not isinstance(decode_parms, PDFList):
            decode_parms = PDFList(decode_parms)

        # Remove the FlateDecode from the filters list if any
        index = 0
        colors = None
        columns = None
        while index < len(filters.items):
            if filters.items[index] == key_flate_decode:
                filters.items.pop(index)
                parms = decode_parms.items.pop(index)
                if isinstance(parms, PDFDictionary):
                    key_colors = PDFName(b"Colors")
                    if key_colors in parms:
                        colors = parms[key_colors]

                    key_columns = PDFName(b"Columns")
                    if key_columns in parms:
                        columns = parms[key_columns]
            elif filters.items[index] == key_dct_decode:
                stream = jpegtran_optimize(stream)
                index += 1
            else:
                index += 1

        _logger.debug(
            "Before RLE on object %d, size = %d" %
            (self.obj_num, len(stream))
        )
        rle_stream = rle_encode(stream)
        _logger.debug(
            "After  RLE on object %d, size = %d" %
            (self.obj_num, len(rle_stream))
        )

        _logger.debug(
            "Before RLE+Zopfli on object %d, size = %d" %
            (self.obj_num, len(stream))
        )
        zopfli_rle_stream = zopfli_deflate(rle_stream)
        _logger.debug(
            "After  RLE+Zopfli on object %d, size = %d" %
            (self.obj_num, len(zopfli_rle_stream))
        )

        _logger.debug(
            "Before RLE+Zlib on object %d, size = %d" %
            (self.obj_num, len(stream))
        )
        zlib_rle_stream = compress(rle_stream, 9)
        _logger.debug(
            "After  RLE+Zlib on object %d, size = %d" %
            (self.obj_num, len(zlib_rle_stream))
        )

        _logger.debug(
            "Before Zlib on object %d, size = %d" %
            (self.obj_num, len(stream))
        )
        zlib_stream = compress(stream, 9)
        _logger.debug(
            "After  Zlib on object %d, size = %d" %
            (self.obj_num, len(zlib_stream))
        )

        _logger.debug(
            "Before Zopfli on object %d, size = %d" %
            (self.obj_num, len(stream))
        )
        zopfli_stream = zopfli_deflate(stream)
        _logger.debug(
            "After  Zopfli on object %d, size = %d" %
            (self.obj_num, len(zopfli_stream))
        )

        # Replace only if size reduced
        if len(zopfli_stream) < len(self.stream.stream) or \
            len(zopfli_rle_stream) < len(self.stream):

            _logger.debug(
                "Compression reduces the object %d stream size" % self.obj_num
            )

            if len(zopfli_stream) < len(zopfli_rle_stream):
                _logger.debug(
                    ("Zopfli alone is better than RLE + Zopfli for object %d "
                     "(%d -> %d)"
                    ) % (self.obj_num, len(self.stream), len(zopfli_rle_stream))
                )
                filters.items.insert(0, key_flate_decode)
                decode_parms.items.insert(0, PDFNull())
                self.stream = PDFStream(zopfli_stream)
                self.value[b"Filter"] = filters
                self.value[b"DecodeParms"] = decode_parms
                self.value[b"Length"] = PDFNumber(len(zopfli_stream))
            else:
                _logger.debug(
                    ("RLE + Zopfli is better than Zopfli alone for object %d "
                     "(%d -> %d)"
                    ) % (self.obj_num, len(self.stream), len(zopfli_rle_stream))
                )
                filters.items.insert(0, key_rle_decode)
                decode_parms.items.insert(0, PDFNull())
                filters.items.insert(0, key_flate_decode)
                if colors != None or columns != None:
                    parms = {}
                    parms[PDFName(b"Predictor")] = PDFNumber(0)
                    if colors != None:
                        parms[PDFName(b"Colors")] = colors

                    if columns != None:
                        parms[PDFName(b"Columns")] = columns

                    decode_parms.items.insert(0, PDFDictionary(parms))
                else:
                    decode_parms.items.insert(0, PDFNull())

                self.stream = PDFStream(zopfli_rle_stream)
                self.value[b"Filter"] = filters
                self.value[b"DecodeParms"] = decode_parms
                self.value[b"Length"] = PDFNumber(len(zopfli_rle_stream))
