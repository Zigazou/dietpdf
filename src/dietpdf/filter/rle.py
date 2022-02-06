__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

"""
Implementation of the Run-Length-Encoding encoding/decoding functions.

From Adobe PDF 32000-1:2008:

    The RunLengthDecode filter decodes data that has been encoded in a simple
    byte-oriented format based on run length. The encoded data shall be a
    sequence of runs, where each run shall consist of a length byte followed by
    1 to 128 bytes of data. If the length byte is in the range 0 to 127, the
    following length + 1 (1 to 128) bytes shall be copied literally during
    decompression. If length is in the range 129 to 255, the following single
    byte shall be copied 257 - length (2 to 128) times during decompression.
    A length value of 128 shall denote EOD.

    The compression achieved by run-length encoding depends on the input data.
    In the best case (all zeros), a compression of approximately 64 : 1 is
    achieved for long files. The worst case (the hexadecimal sequence 00
    alternating with FF) results in an expansion of 127 : 128.
"""


def rle_encode(content: bytes) -> bytes:
    """Encode a byte string using the RLE algorithm specified by the PDF
    specifications.

    """
    output = []
    offset = 0
    while offset < len(content):
        current = content[offset]

        count = 1
        offset += 1
        while offset < len(content) and content[offset] == current and count < 127:
            count += 1
            offset += 1

        if count == 1:
            if offset == len(content):
                output.append(0)
                output.append(current)
            else:
                while offset < len(content) and content[offset] != current and count < 128:
                    current = content[offset]
                    count += 1
                    offset += 1

                output.append(count - 1)
                output += content[offset - count:offset]
        else:
            output.append(257 - count)
            output.append(current)

    return bytes(output)


def rle_decode(content: bytes) -> bytes:
    """Decode a byte string using the RLE algorithm specified by the PDF
    specifications.

    """
    offset = 0
    output = b""
    while offset < len(content):
        token = content[offset]

        if token < 128:
            length = token + 1
            offset += 1
            output += content[offset:offset + length]
            offset += length
        elif token > 128:
            length = 257 - token
            offset += 1
            output += content[offset:offset + 1] * length
            offset += 1
        else:
            offset += 1

    return bytes(output)
