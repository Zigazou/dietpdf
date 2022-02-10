from dietpdf.token.PDFString import unescape, PDFString

__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"


def test_PDFString_unescape():
    assertions = [
        (b"", b""),
        (b"ABCD", b"ABCD"),
        (b"\\101\\102\\103\\104", b"ABCD"),
        (b"\\60\\61\\62\\63", b"0123"),
        (b"\\618", b"18"),
        (b"\\0053", b"\0053"),
        (b"\\053", b"+"),
        (b"\\53", b"+"),
        (b"hello\\\r\nworld", b"helloworld"),
        (b"hello\\\rworld", b"helloworld"),
        (b"hello\\\nworld", b"helloworld"),
        (b"hello\world", b"helloworld"),
        (b"hello\\nworld", b"hello\nworld"),
    ]

    for encoded, decoded in assertions:
        assert decoded == unescape(encoded)

def test_PDFString_to_string():
    assertions = [
        (b"", ""),
    ]

    for encoded, decoded in assertions:
        pdf_string = PDFString(encoded)
        assert decoded == pdf_string.to_string()
