__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from zlib import compress, decompress
from base64 import a85decode, encode
from logging import getLogger

from ..filter.zopfli import zopfli_deflate
from ..filter.rle import rle_encode
from ..filter.lzw import lzw_decode
from ..filter.jpegoptim import jpegtran_optimize
from ..filter.predictor import (
    PREDICTOR_NONE, predictor_png_decode,
    predictor_tiff_decode, predictor_png_best_encode,
    PREDICTOR_PNG_OPTIMUM
)

from ..token.PDFToken import PDFToken
from ..token.PDFName import PDFName
from ..token.PDFNumber import PDFNumber

from .content_stream import optimize_content_stream
from .PDFItem import PDFItem
from .PDFStream import PDFStream
from .PDFList import PDFList
from .PDFNull import PDFNull
from .PDFDictionary import PDFDictionary

_logger = getLogger("PDFObject")

NO_SPACE = ["PDFDictionary", "PDFList", "PDFString", "PDFHexString"]


class PDFObject(PDFItem):
    """A PDF object"""

    def __init__(self, obj_num: int, gen_num: int, value, stream: PDFStream):
        assert type(obj_num) == int
        assert type(gen_num) == int
        assert isinstance(value, PDFToken)
        assert stream == None or type(stream) == PDFStream

        self.obj_num = obj_num
        self.gen_num = gen_num
        self.value = value
        self.stream = stream
        self.source_code = False

    def __bool__(self):
        """A PDFObject is True if it has a value and this value is itself
        True, False otherwise.
        """
        return self.value != None and bool(self.value)

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
        if isinstance(other, PDFObject):
            return (
                self.obj_num == other.obj_num and
                self.gen_num == other.gen_num and
                self.value == other.value and
                self.stream == other.stream
            )
        elif isinstance(other, PDFToken):
            return False
        else:
            return NotImplemented

    def __contains__(self, key):
        """A PDFObject implements the __contains__ method when its value is a
        PDFDictionary.

        PDFDictionary keys are PDFName. If anything else than a PDFName is used,
        this method will try to convert it to a PDFNmae.

        It allows to directly use byte strings as key for example.

        If the PDFObject value is anything other than PDFDictionary, it returns
        False.
        """
        if type(key) != PDFName:
            key = PDFName(key)

        if type(self.value) != PDFDictionary:
            return False

        return self.value.__contains__(key)

    def __getitem__(self, key):
        """A PDFObject implements the __getitem__ method when its value is a
        PDFDictionary.

        PDFDictionary keys are PDFName. If anything else than a PDFName is used,
        this method will try to convert it to a PDFNmae.

        It allows to directly use byte strings as key for example.

        Using this method on PDFObject having other values than PDFDictionary
        will lead to incorrect results or exceptions.
        """
        if isinstance(self.value, PDFDictionary):
            return self.value.__getitem__(key)
        elif isinstance(self.value, PDFList):
            return self.value.__getitem__(key)
        else:
            raise TypeError()

    def has_stream(self) -> bool:
        """Does this object has a stream?

        :return: True if the object has a non-empty stream, False otherwise
        :rtype: bool
        """
        return bool(self.stream)

    def pretty(self) -> str:
        if type(self.value) == PDFDictionary and b"Type" in self.value:
            obj_type = self.value[b"Type"].encode().decode('ascii')
        else:
            obj_type = ""

        if self.stream:
            return self._pretty(
                "Object(%d, %d%s) + stream(%d)" %
                (self.obj_num, self.gen_num, obj_type, len(self.stream))
            )
        else:
            return self._pretty("Object(%d, %d%s)" %
                (self.obj_num, self.gen_num, obj_type)
            )

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

    def decode_stream(self) -> bytes:
        """Decode the stream associated to the PDFObject.

        The stream is decoded according to the specified filters.

        :return: The decoded stream
        :rtype: bytes
        """
        if not self.has_stream():
            return b""

        # Retrieve filter(s)
        filters = self[b"Filter"] if b"Filter" in self else None
        if not filters:
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
            decode_parms = PDFList([PDFNull() for _ in filters])

        # Apply filters
        output = bytes(self.stream)
        for (filter, parms) in zip(filters, decode_parms):
            if filter == b"FlateDecode":
                try:
                    _logger.debug("Inflating")
                    output = decompress(output)
                except:
                    raise Exception(
                        "Unable to decompress (ZLIB) object %d stream" %
                        self.obj_num
                    )
            elif filter == b"ASCII85Decode":
                try:
                    _logger.debug("ASCII85 decoding")
                    output = a85decode(output.strip(), adobe=True)
                except:
                    raise Exception(
                        "Unable to decode ASCII85 object %d stream" %
                        self.obj_num
                    )
            elif filter == b"LZWDecode":
                try:
                    _logger.debug("LZW decoding")
                    output = lzw_decode(output)
                except:
                    raise Exception(
                        "Unable to decompress (LZW) object %d stream" %
                        self.obj_num
                    )

            if type(parms) == PDFDictionary and b"Predictor" in parms:
                columns = parms[b"Columns"].value

                if b"Colors" in parms:
                    colors = parms[b"Colors"].value
                else:
                    colors = 1

                predictor = int(parms[b"Predictor"])
                if predictor == 2:
                    output = predictor_tiff_decode(output, columns, colors)
                elif predictor >= 10 and predictor <= 15:
                    output = predictor_png_decode(output, columns, colors)

        return output

    def optimize_stream(self):
        """Optimize the stream of a PDFObject, if any.

        This method will try different strategies (filters, combination of
        filters) to reduce the stream size.

        The optimization process will replace the stream by its optimized
        version.
        """
        # No stream, nothing to optimize.
        if not self.has_stream():
            return

        stream = self.decode_stream()

        # Replacing line returns by space helps compression.
        if self.source_code:
            _logger.debug("Optimize source code")
            stream = optimize_content_stream(stream)

        key_dct_decode = PDFName(b"DCTDecode")
        key_flate_decode = PDFName(b"FlateDecode")
        key_lzw_decode = PDFName(b"LZWDecode")
        key_rle_decode = PDFName(b"RunLengthDecode")
        key_jbig2_decode = PDFName(b"JBIG2Decode")
        key_ascii85_decode = PDFName(b"ASCII85Decode")
        key_ccittfax_decode = PDFName(b"CCITTFaxDecode")

        # Retrieve filter(s)
        filters = self[b"Filter"] if b"Filter" in self else []

        # Convert the filter to a PDFList of filters
        if type(filters) != PDFList:
            filters = PDFList(filters)

        # Retrieve decode parameters
        decode_parms = self[b"DecodeParms"] if b"DecodeParms" in self else []
        if not filters:
            decode_parms = PDFList([])
        elif not decode_parms:
            decode_parms = PDFList([PDFNull() for _ in range(len(filters))])
        elif type(decode_parms) != PDFList:
            decode_parms = PDFList(decode_parms)

        # Remove the FlateDecode from the filters list if any
        index = 0
        colors = None
        columns = None
        dctencoded = False
        jbig2encoded = False
        deflateencoded = False
        ccittfaxencoded = False
        while index < len(filters.items):
            if filters.items[index] == key_flate_decode:
                deflateencoded = True
                filters.items.pop(index)
                parms = decode_parms.items.pop(index)
                if isinstance(parms, PDFDictionary):
                    key_colors = PDFName(b"Colors")
                    if key_colors in parms:
                        colors = parms[key_colors]

                    key_columns = PDFName(b"Columns")
                    if key_columns in parms:
                        columns = parms[key_columns]
            elif filters.items[index] == key_lzw_decode:
                filters.items.pop(index)
                parms = decode_parms.items.pop(index)
                if isinstance(parms, PDFDictionary):
                    key_colors = PDFName(b"Colors")
                    if key_colors in parms:
                        colors = parms[key_colors]

                    key_columns = PDFName(b"Columns")
                    if key_columns in parms:
                        columns = parms[key_columns]
            elif filters.items[index] == key_jbig2_decode:
                jbig2encoded = True
                index += 1
            elif filters.items[index] == key_ccittfax_decode:
                ccittfaxencoded = True
                index += 1
            elif filters.items[index] == key_dct_decode:
                dctencoded = True
                _logger.debug("Optimize JPEG")
                stream = jpegtran_optimize(stream)
                index += 1
            elif filters.items[index] == key_ascii85_decode:
                filters.items.pop(index)
                decode_parms.items.pop(index)
            else:
                index += 1

        if not dctencoded and not jbig2encoded and not ccittfaxencoded:
            if not columns and b"Width" in self.value:
                columns = self.value[b"Width"]

            if not colors and b"ColorSpace" in self.value:
                if self.value[b"ColorSpace"] == PDFName(b"DeviceRGB"):
                    colors = PDFNumber(3)
                elif self.value[b"ColorSpace"] == PDFName(b"DeviceGray"):
                    colors = PDFNumber(1)
                elif self.value[b"ColorSpace"] == PDFName(b"DeviceCMYK"):
                    colors = PDFNumber(4)

        streams = {}

        streams["NONE"] = stream
        streams["RLE"] = rle_encode(stream)
        _logger.debug("Try RLE")

        if columns:
            if not colors:
                colors = PDFNumber(1)

            try:
                streams["AUTO"] = predictor_png_best_encode(
                    stream, int(columns), int(colors)
                )
                _logger.debug("Try PNG_AUTO predictor")
            except ValueError:
                _logger.debug("Ignore PNG_AUTO predictor")

        # Calculates compressed sizes for all predictors.
        (best_opt, best_size) = ("NONE", 2**32)
        for opt in streams:
            size = len(compress(streams[opt], 5))
            if size < best_size:
                (best_opt, best_size) = (opt, size)

        # Find best optimization.
        zopfli_stream = zopfli_deflate(streams[best_opt])
        _logger.debug("Try Zopfli")

        # Compression has no gain.
        if ccittfaxencoded or jbig2encoded or len(zopfli_stream) >= len(self.stream):
            if dctencoded:
                _logger.info(
                    "Best strategy for object %d stream = DCTENCODE" %
                    self.obj_num
                )
            elif jbig2encoded:
                _logger.info(
                    "Best strategy for object %d stream = JBIG2ENCODE" %
                    self.obj_num
                )
            elif deflateencoded:
                self.value[b"Filter"] = key_flate_decode
                _logger.info(
                    "Best strategy for object %d stream = DEFLATE" %
                    self.obj_num
                )
            elif ccittfaxencoded:
                _logger.info(
                    "Best strategy for object %d stream = CCITTFAX" %
                    self.obj_num
                )
            else:
                _logger.info(
                    "Best strategy for object %d stream = NONE" %
                    self.obj_num
                )

            return

        if dctencoded:
            best_strategy = "DCTENCODE+"
        elif jbig2encoded:
            best_strategy = "JBIG2ENCODE+"
        else:
            best_strategy = ""

        _logger.info(
            "Best strategy for object %d stream = %sZOPFLI+%s" %
                (self.obj_num, best_strategy, best_opt)
        )

        if best_opt == "RLE":
            filters.items.insert(0, key_rle_decode)
            decode_parms.items.insert(0, PDFNull())
            columns = None
            colors = None

        filters.items.insert(0, key_flate_decode)

        if (colors or columns) and best_opt not in ["NONE", "RLE"]:
            parms = {}
            if best_opt == "AUTO":
                parms[PDFName(b"Predictor")] = PDFNumber(PREDICTOR_PNG_OPTIMUM)

            if colors != None:
                parms[PDFName(b"Colors")] = colors

            if columns != None:
                parms[PDFName(b"Columns")] = columns

            decode_parms.items.insert(0, PDFDictionary(parms))
        else:
            decode_parms.items.insert(0, PDFNull())

        self.stream = PDFStream(zopfli_stream)

        if len(filters) == 0:
            if b"Filter" in self.value:
                self.value.delete(b"Filter")
        elif len(filters) == 1:
            self.value[b"Filter"] = filters[0]
        else:
            self.value[b"Filter"] = filters

        if decode_parms.is_null():
            if b"DecodeParms" in self.value:
                self.value.delete(b"DecodeParms")
        elif len(decode_parms) == 1:
            self.value[b"DecodeParms"] = decode_parms[0]
        else:
            self.value[b"DecodeParms"] = decode_parms

        self.value[b"Length"] = PDFNumber(len(zopfli_stream))
