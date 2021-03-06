__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from ..parser.TokenParser import TokenParser
from ..token.PDFHexString import PDFHexString
from ..token.hexstring_to_string import hexstring_to_string
from ..processor.TokenProcessor import TokenProcessor

def optimize_content_stream(stream: bytes) -> bytes:
    """Optimize a content stream.

    The optimization process consists in:

      - removing unnecessary white spaces
      - converting line feed to space for a better compression ratio

    :param content: The content stream to optimize
    :type content: bytes
    :return: The content stream optimized
    :rtype: bytes
    """
    assert type(stream) == bytes

    stack = TokenProcessor()
    parser = TokenParser(stack)

    parser.parse(stream)

    # Convert hexadecimal strings to strings but not in character mappings
    # because some readers do not like it.
    if b"/CIDInit" not in stream:
        def any_hexstring(_, item): return type(item) == PDFHexString
        for index, _ in stack.tokens.find(any_hexstring):
            stack.tokens.stack[index] = hexstring_to_string(
                stack.tokens.stack[index]
            )

    # The encode method will remove unnecessary spaces and convert any white
    # spaces including line returns into standard space.
    return stack.encode() + b"\n"
