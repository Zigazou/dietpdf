__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from logging import getLogger

from ..token.TokenStack import TokenStack
from ..token.PDFToken import PDFToken

_logger = getLogger("TokenProcessor")


class TokenProcessor:
    """A PDF Stack
    """

    def __init__(self):
        self.tokens = TokenStack()

    def push(self, item: PDFToken):
        self.tokens.push(item)

    def encode(self) -> bytes:
        """Encode a PDF from the current state of the processor

        :return: A complete PDF file content ready to be written in a file
        :rtype: bytes
        """
        def any_item(_a, _b): return True

        delimiters = b"()<>[]{}/%"
        output = b""
        offset = 0
        previous_is_delimiter = True

        for _, item in self.tokens.find(any_item):
            item_encoded = item.encode()
            current_is_delimiter = item_encoded[0] in delimiters

            if not(previous_is_delimiter or current_is_delimiter):
                offset += 1
                output += b" "

            item.item_offset = offset
            offset += len(item_encoded)
            output += item_encoded

            previous_is_delimiter = item_encoded[-1] in delimiters

        return output

    def pretty_print(self):
        """Pretty print the stack of the processor

        It uses the logging mechanisme at the debug level.
        """
        _logger.debug("Stack state:")

        def any_item(_a, _b): return True
        for _, item in self.tokens.find(any_item):
            _logger.debug("- %s" % (item.pretty(),))
