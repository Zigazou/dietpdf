__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from zlib import decompress
from dietpdf.token import PDFName, PDFString, PDFNumber

from dietpdf.item import (
    PDFObject, PDFObjectStream, PDFDictionary, PDFReference, PDFList
)

from dietpdf.processor.PDFProcessor import PDFProcessor
from dietpdf.parser.PDFParser import PDFParser
from dietpdf.info import convert_objstm


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


def hexdump(stream: bytes):
    for base in range(0, len(stream), 16):
        hexadecimal_part = " ".join([
            ("%02X" % stream[offset])
            if offset < len(stream) else "  "
            for offset in range(base, base + 16)
        ])

        ascii_part = "".join([
            "%c" % (
                stream[offset] if stream[offset] in range(32, 128) else "."
            )
            if offset < len(stream) else " "
            for offset in range(base, base + 16)
        ])

        print("%08X:  %s  %s" % (base, hexadecimal_part, ascii_part))


def test_PDFObjectStream():
    object_stream = PDFObjectStream(12, 0, create_objects())

    # Encode the object stream.
    encoded = object_stream.encode()
    hexdump(encoded)

    # Parse the encoded data.
    processor = PDFProcessor()
    parser = PDFParser(processor)
    parser.parse(encoded)
    processor.end_parsing()

    hexdump(decompress(processor.tokens.stack[0].stream.stream))

    # Convert back the object stream to its original objects.
    convert_objstm(processor.tokens)

    assert len(processor.tokens.stack) == 11
