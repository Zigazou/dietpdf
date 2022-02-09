__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

import re
from ..processor import PDFProcessor
from ..item import (
    PDFComment, PDFNumber, PDFStream, PDFCommand, PDFName, PDFNull,
    PDFListOpen, PDFListClose, PDFDictOpen, PDFDictClose, PDFHexString,
    PDFString
)


class PDFParser:
    def __init__(self, processor: PDFProcessor):
        self.processor = processor
        self.offset = 0
        self.binary_data = b""

        # Characters authorized by the PDF specifications
        self.pdf_white_space = b"\0\t\n\f\r "
        self.pdf_delimiter = b"()<>[]{}/%"
        self.pdf_name_chars = b"!\"#$&'*+,.0-9:;=?@A-Z\\^_`a-z{|}~-"

        self.start_comment = b"%"
        self.start_number = b"0123456789-+."
        self.start_command = b"%s%s" % (
            b"abcdefghijklmnopqrstuvwxyz",
            b"ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        )
        self.start_name = b"/"

        # Regular expression
        self.end_value = b"(?=[%s%s]|$)" % (
            re.escape(self.pdf_white_space),
            re.escape(self.pdf_delimiter)
        )

        self.end_of_line = re.compile(b"(.*?)([\r\n]+|$)", re.DOTALL)

        self.end_of_number = re.compile(
            b"([+-]?[0-9]+\.?[0-9]*|[+-]?[0-9]*\.[0-9]+)" + self.end_value
        )

        self.end_of_word = re.compile(
            b"([%s]*)%s" % (self.pdf_name_chars, self.end_value)
        )

        self.hex_string = re.compile(
            b"([A-Fa-f0-9%s]*)>" % (self.pdf_white_space,)
        )

        self.end_of_stream = re.compile(
            b"(\r\n|\n)(.+?)\n?endstream(?=[%s]+endobj)"
            % re.escape(self.pdf_white_space),
            re.DOTALL
        )

    def _parse_white_space(self):
        self.offset += 1

    def _parse_comment(self):
        sub = self.end_of_line.search(self.binary_data, self.offset)
        self.processor.push(PDFComment(sub.group(1)))

        self.offset = sub.span(0)[1]

    def _parse_number(self):
        sub = self.end_of_number.search(self.binary_data, self.offset)
        self.processor.push(PDFNumber(sub.group(1)))

        self.offset = sub.span(0)[1]

    def _parse_command(self):
        sub = self.end_of_word.search(self.binary_data, self.offset)
        word = sub.group(1)

        if word == b"stream":
            stream = self.end_of_stream.search(
                self.binary_data, self.offset + len(b"stream")
            )
            self.processor.push(PDFStream(stream.group(2)))
            self.offset = stream.span(0)[1]
        elif word == b"null":
            self.processor.push(PDFNull())
            self.offset = sub.span(0)[1]
        else:
            self.processor.push(PDFCommand(word))
            self.offset = sub.span(0)[1]

    def _parse_name(self):
        sub = self.end_of_word.search(self.binary_data, self.offset + 1)
        self.processor.push(PDFName(sub.group(1)))
        self.offset = sub.span(0)[1]

    def _parse_list_open(self):
        self.processor.push(PDFListOpen())
        self.offset += 1

    def _parse_list_close(self):
        self.processor.push(PDFListClose())
        self.offset += 1

    def _parse_dict_open(self):
        self.processor.push(PDFDictOpen())
        self.offset += 2

    def _parse_dict_close(self):
        self.processor.push(PDFDictClose())
        self.offset += 2

    def _parse_hex_string(self):
        sub = self.hex_string.search(self.binary_data, self.offset + 1)
        self.processor.push(PDFHexString(sub.group(1)))
        self.offset = sub.span(0)[1]

    def _parse_string(self):
        char_offset = self.offset + 1
        nested = 1
        while nested != 0:
            char = self.binary_data[char_offset:char_offset + 1]
            if char == b")":
                nested -= 1
            elif char == b"(":
                nested += 1
            elif char == b"\\":
                char_offset += 1

            char_offset += 1

        self.processor.push(
            PDFString(self.binary_data[self.offset+1:char_offset-1])
        )

        self.offset = char_offset

    def parse(self, binary_data: bytes):
        """Parses a PDF

        Given a freshly created PDFself.Processor, this function parses a block
        of bytes and extract the PDF structure and objects.

        Once finished, the PDFself.Processor object will hold the structure and
        objects.
        """
        self.offset = 0
        self.binary_data = binary_data

        while self.offset < len(self.binary_data):
            current = self.binary_data[self.offset:self.offset+1]

            if current in self.pdf_white_space:
                self._parse_white_space()
            elif current in self.start_comment:
                self._parse_comment()
            elif current in self.start_number:
                self._parse_number()
            elif current in self.start_command:
                self._parse_command()
            elif current in self.start_name:
                self._parse_name()
            elif current == b"[":
                self._parse_list_open()
            elif current == b"]":
                self._parse_list_close()
            elif self.binary_data[self.offset:self.offset + 2] == b"<<":
                self._parse_dict_open()
            elif self.binary_data[self.offset:self.offset + 2] == b">>":
                self._parse_dict_close()
            elif current == b"<":
                self._parse_hex_string()
            elif current == b"(":
                self._parse_string()
            else:
                print("Unable to read at offset %d" % (self.offset,))
