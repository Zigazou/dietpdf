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

    output = bytearray(len(content) * 2)
    output_offset = 0
    input_offset = 0
    while input_offset < len(content):
        current = content[input_offset]

        # Read as many following bytes identical to the current byte.
        count = 1
        input_offset += 1
        while input_offset < len(content) and content[input_offset] == current and count < 127:
            count += 1
            input_offset += 1

        if count == 1:
            # The current byte does not repeat.
            if input_offset == len(content):
                # The current byte is the last byte.
                output[output_offset:output_offset + 2] = b"\000%c" % current
                output_offset += 2
            else:
                # Read as many different bytes
                while input_offset < len(content) and content[input_offset] != current and count < 128:
                    current = content[input_offset]
                    count += 1
                    input_offset += 1

                output[output_offset:output_offset + count] = (
                    b"%c%s" % (count - 1, content[input_offset - count:input_offset])
                )
                output_offset += count + 1

        else:
            # Encode the repetition of the current byte.
            output[output_offset:output_offset + 2] = b"%c%c" % (257 - count, current)
            output_offset += 2

    return bytes(output[:output_offset])


def rle_decode(content: bytes) -> bytes:
    """Decode a byte string using the RLE algorithm specified by the PDF
    specifications.

    :param content: The byte string to decode using the RLE algorithm.
    :type content: bytes
    :return: The byte string decoded
    :rtype: bytes
    """

    assert type(content) == bytes

    input_offset = 0
    output = b""
    while input_offset < len(content):
        token = content[input_offset]

        if token < 128:
            length = token + 1
            output += content[input_offset + 1:input_offset + length + 1]
            input_offset += length
        elif token > 128:
            length = 257 - token
            output += content[input_offset + 1:input_offset + 2] * length
            input_offset += 1

        input_offset += 1

    return output
