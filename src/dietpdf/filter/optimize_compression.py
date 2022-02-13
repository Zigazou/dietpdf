__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from zlib import compress, decompress
from logging import getLogger

from . import (
    zopfli_deflate, rle_encode, predictor_png_encode, jpegtran_optimize,
    lzw_encode
)

_logger = getLogger("Optimize compression")

STRATEGIES_GROUPS = {
    "DCT": [
        ["LZW"],
        ["Zopfli"],
        ["RLE"],
        ["RLE", "Zlib"],
        ["RLE", "Zopfli"],
        ["RLE", "LZW"],
    ],
    "JPX": [
        ["LZW"],
        ["Zopfli"],
        ["RLE"],
        ["RLE", "Zlib"],
        ["RLE", "Zopfli"],
        ["RLE", "LZW"],
    ],
    "OTHER": [
        ["LZW"],
        ["Zopfli"],
        ["RLE"],
        ["RLE", "Zlib"],
        ["RLE", "Zopfli"],
        ["RLE", "LZW"],
    ],
}

def optimize_compression(content: bytes, dct: bool, jpx: bool, columns: int, colors: int) -> bytes:

    # Optimizes JPEG.
    if dct:
        _logger.debug("Optimizing JPEG"
        content = jpegtran_optimize(content)

    if dct:
        strategies = STRATEGIES_GROUPS["DCT"]
    elif jpx:
        strategies = STRATEGIES_GROUPS["JPX"]
    else:
        strategies = STRATEGIES_GROUPS["OTHER"]


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
