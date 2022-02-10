__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

import re

from dietpdf.token import PDFCommand
from dietpdf.item import PDFStream, PDFNull

from .TokenParser import TokenParser

class PDFParser(TokenParser):
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
