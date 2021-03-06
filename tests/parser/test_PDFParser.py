__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from random import seed, randrange, choice
from zlib import decompress

from dietpdf.parser.PDFParser import PDFParser
from dietpdf.processor.PDFProcessor import PDFProcessor

from dietpdf.token.PDFString import PDFString
from dietpdf.token.PDFHexString import PDFHexString
from dietpdf.token.PDFNumber import PDFNumber

from dietpdf.item.PDFObject import PDFObject


def test_PDFParser_stream():
    seed(2022)

    after_stream = [b"\r\n", b"\n"]

    for _ in range(64):
        processor = PDFProcessor()
        parser = PDFParser(processor)

        raw_data = bytes([randrange(256) for _ in range(randrange(5000))])
        pdf_stream = b"0 0 obj\n8\nstream%s%sendstream\nendobj\n" % (
            choice(after_stream), raw_data
        )

        parser.parse(pdf_stream)

        assert processor.tokens.stack_size() == 1
        assert isinstance(processor.tokens.stack_at(0), PDFObject)
        assert processor.tokens.stack_at(0).has_stream()
        assert len(processor.tokens.stack_at(0).stream) == len(raw_data)
        assert processor.tokens.stack_at(0).stream == raw_data


def test_PDFParser_hexstring():
    hexstring_tests = [
        b"<>",
        b"<0102030405060708090A0B0C0D0E0F10>",
        b"< 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F 10 >",
        b"<0102030405060708090A0B0C0D0E0F1>",
        b"<0102030405060708090a0b0c0d0e0f10>",
        b"< 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f 10 >",
        b"<0102030405060708090a0b0c0d0e0f1>",
    ]

    for hexstring_test in hexstring_tests:
        processor = PDFProcessor()
        parser = PDFParser(processor)

        parser.parse(hexstring_test)

        assert processor.tokens.stack_size() == 1
        assert isinstance(processor.tokens.stack_at(0), PDFHexString)
        assert len(processor.tokens.stack_at(0).hexstring) == len(hexstring_test) - 2


def test_PDFParser_string():
    string_tests = [
        b"()",
        b"(Hello world!)",
        b"(\\123Hello world!)",
        b"((()))",
        b"(\\(\\(\\)\\))",
    ]

    for string_test in string_tests:
        processor = PDFProcessor()
        parser = PDFParser(processor)

        parser.parse(string_test)

        assert processor.tokens.stack_size() == 1
        assert isinstance(processor.tokens.stack_at(0), PDFString)
        assert len(processor.tokens.stack_at(0).string) == len(string_test) - 2


def test_PDFParser_integer():
    integer_tests = [
        b"0",
        b"12",
        b"+0",
        b"+12",
        b"-0",
        b"-12",
    ]

    for integer_test in integer_tests:
        processor = PDFProcessor()
        parser = PDFParser(processor)

        parser.parse(integer_test)

        assert processor.tokens.stack_size() == 1
        assert isinstance(processor.tokens.stack_at(0), PDFNumber)
        assert type(processor.tokens.stack_at(0).value) == int


def test_PDFParser_float():
    float_tests = [
        b"0.0",
        b"12.3",
        b"+0.0",
        b"+12.3",
        b"-0.0",
        b"-12.3",
        b".3",
        b"+.3",
        b"-.3",
    ]

    for float_test in float_tests:
        processor = PDFProcessor()
        parser = PDFParser(processor)

        parser.parse(float_test)

        assert processor.tokens.stack_size() == 1
        assert isinstance(processor.tokens.stack_at(0), PDFNumber)
        assert type(processor.tokens.stack_at(0).value) == float


def test_PDFParser_comment():
    seed(2022)

    end_of_line = [b"\r\n", b"\r", b"\n", b""]

    for _ in range(128):
        processor = PDFProcessor()
        parser = PDFParser(processor)

        dummy_text = bytes([randrange(32, 127) for _ in range(randrange(5000))])
        pdf_stream = b"%%%s%s" % (dummy_text, choice(end_of_line))

        parser.parse(pdf_stream)

        # Comments other than %PDF* and %%EOF are discarded
        assert processor.tokens.stack_size() == 0
