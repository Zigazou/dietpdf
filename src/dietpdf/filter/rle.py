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

    :param content: The byte string to encode using the RLE algorithm.
    :type content: bytes
    :return: The byte string encoded
    :rtype: bytes
    """

    assert type(content) == bytes

    output = b""
    offset = 0
    while offset < len(content):
        current = content[offset]

        # Read as many following bytes identical to the current byte.
        count = 1
        offset += 1
        while offset < len(content) and content[offset] == current and count < 127:
            count += 1
            offset += 1

        if count == 1:
            # The current byte does not repeat.
            if offset == len(content):
                # The current byte is the last byte.
                output += b"\000%c" % current
            else:
                # Read as many different bytes
                while offset < len(content) and content[offset] != current and count < 128:
                    current = content[offset]
                    count += 1
                    offset += 1

                output += b"%c%s" % (count - 1, content[offset - count:offset])
        else:
            # Encode the repetition of the current byte.
            output += b"%c%c" % (257 - count, current)

    return output


def rle_decode(content: bytes) -> bytes:
    """Decode a byte string using the RLE algorithm specified by the PDF
    specifications.

    :param content: The byte string to decode using the RLE algorithm.
    :type content: bytes
    :return: The byte string decoded
    :rtype: bytes
    """

    assert type(content) == bytes

    offset = 0
    output = b""
    while offset < len(content):
        token = content[offset]

        if token < 128:
            length = token + 1
            output += content[offset + 1:offset + length + 1]
            offset += length
        elif token > 128:
            length = 257 - token
            output += content[offset + 1:offset + 2] * length
            offset += 1

        offset += 1

    return output
