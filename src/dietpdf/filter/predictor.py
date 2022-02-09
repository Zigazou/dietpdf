__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

PREDICTOR_NONE = 1
PREDICTOR_TIFF = 2
PREDICTOR_PNG_NONE = 10
PREDICTOR_PNG_SUB = 11
PREDICTOR_PNG_UP = 12
PREDICTOR_PNG_AVERAGE = 13
PREDICTOR_PNG_PAETH = 14
PREDICTOR_PNG_OPTIMUM = 15


def paeth_predictor(left: int, above: int, upper_left: int) -> int:
    """Selected a value according to the Paeth predictor algorithm.

    See https://www.w3.org/TR/PNG-Filters.html for more information.

    :param left: The value of the pixel on the left of the current pixel.
    :type left: int
    :param above: The value of the pixel above the current pixel.
    :type above: int
    :param upper_left: The value of the pixel on the left and above of the
        current pixel.
    :type upper_left: int
    :return: The selected value
    :rtype: int
    """
    assert type(left) == int
    assert type(above) == int
    assert type(upper_left) == int

    total = left + above + upper_left
    dist_to_left = abs(total - left)
    dist_to_above = abs(total - above)
    dist_to_upper_left = abs(total - upper_left)

    if dist_to_left <= dist_to_above and dist_to_left <= dist_to_upper_left:
        return left
    elif dist_to_above <= dist_to_upper_left:
        return above
    else:
        return upper_left


ROW_NONE = 0
ROW_SUB = 1
ROW_UP = 2
ROW_AVERAGE = 3
ROW_PAETH = 4


def predictor_png_encode(stream: bytes, row_predictor: int, columns: int, colors: int) -> bytes:
    """Decode a stream encoded with PNG predictor(s).

    See https://www.w3.org/TR/PNG-Filters.html for more information.

    :param stream: The byte sequence to encode
    :type stream: bytes
    :param row_predictor: The row predictor used for encoding (ROW_NONE,
        ROW_SUB, ROW_UP, ROW_AVERAGE, ROW_PAETH)
    :type row_predictor: int
    :param columns: Number of columns
    :type columns: int
    :param colors: Number of bytes for one pixel (ie. 3 for 24 bit RGB)
    :type colors: int
    :return: the byte sequence decoded
    :rtype: bytes
    :raise ValueError: If the byte sequence length is not a multiple of columns
        number (with colors taken into account)
    """

    assert type(stream) == bytes
    assert type(row_predictor) == int
    assert type(columns) == int
    assert type(colors) == int

    if len(stream) % (columns * colors) != 0:
        raise ValueError(
            "length of stream to encode is not a multiple of columns"
        )

    output = b""
    previous_row = bytes([0] * columns * colors)
    for offset in range(0, len(stream), columns * colors):
        current_row = stream[offset:offset+columns*colors]

        if row_predictor == ROW_NONE:
            row_encoded = current_row
        elif row_predictor == ROW_SUB:
            current_row = b"\0" * colors + current_row
            row_encoded = bytes([
                (current_row[column + colors] - current_row[column]) % 256
                for column in range(columns * colors)
            ])
            current_row = current_row[colors:]
        elif row_predictor == ROW_UP:
            row_encoded = bytes([
                (current_row[column] - previous_row[column]) % 256
                for column in range(columns * colors)
            ])
        elif row_predictor == ROW_AVERAGE:
            current_row = b"\0" * colors + current_row
            row_encoded = bytes([
                (
                    current_row[column + colors] -
                    (current_row[column] + previous_row[column]) // 2
                ) % 256
                for column in range(columns * colors)
            ])
            current_row = current_row[colors:]
        elif row_predictor == ROW_PAETH:
            current_row = b"\0" * colors + current_row
            previous_row = b"\0" * colors + previous_row
            row_encoded = bytes([
                (
                    current_row[column + colors] -
                    paeth_predictor(
                        current_row[column],
                        previous_row[column + colors],
                        previous_row[column]
                    )
                ) % 256
                for column in range(columns * colors)
            ])
            current_row = current_row[colors:]
        else:
            pass

        output += b"%c%s" % (row_predictor, row_encoded)
        previous_row = current_row

    return output


def predictor_png_decode(stream: bytes, columns: int, colors: int) -> bytes:
    """Decode a stream encoded with PNG predictor(s).

    See https://www.w3.org/TR/PNG-Filters.html for more information.

    :param stream: The byte sequence to decode
    :type stream: bytes
    :param columns: Number of columns
    :type columns: int
    :param colors: Number of bytes for one pixel (ie. 3 for 24 bit RGB)
    :type colors: int
    :return: the byte sequence decoded
    :rtype: bytes
    :raise ValueError: If the byte sequence length is not a multiple of columns
        number (with colors taken into account)
    """

    assert type(stream) == bytes
    assert type(columns) == int
    assert type(colors) == int

    # The stream length must be a multiple columns * colors + 1 (the +1 takes
    # into account the starting byte)
    if len(stream) % (columns * colors + 1) != 0:
        raise ValueError(
            "length of stream to decode is not a multiple of %d" %
            (columns * colors + 1)
        )

    output = b""
    previous_row = bytes([0] * columns * colors)
    for offset in range(0, len(stream), columns * colors + 1):
        predictor = stream[offset]
        current_row = stream[offset+1:offset+1+columns * colors]

        if predictor == ROW_NONE:
            row_decoded = current_row
        elif predictor == ROW_SUB:
            row_decoded = [0] * colors
            for column in range(columns * colors):
                row_decoded.append(
                    (current_row[column]+row_decoded[column]) % 256
                )
            row_decoded = bytes(row_decoded[colors:])
        elif predictor == ROW_UP:
            row_decoded = bytes([
                (current_row[column] + previous_row[column]) % 256
                for column in range(columns * colors)
            ])
        elif predictor == ROW_AVERAGE:
            row_decoded = [0] * colors
            for column in range(columns * colors):
                row_decoded.append(
                    (
                        current_row[column] +
                        (row_decoded[column] + previous_row[column]) // 2
                    ) % 256
                )
            row_decoded = bytes(row_decoded[colors:])
        elif predictor == ROW_PAETH:
            row_decoded = [0] * colors
            previous_row = b"\0" * colors + previous_row
            for column in range(columns * colors):
                row_decoded.append(
                    (
                        current_row[column] +
                        paeth_predictor(
                            row_decoded[column],
                            previous_row[column + colors],
                            previous_row[column]
                        )
                    ) % 256
                )
            row_decoded = bytes(row_decoded[colors:])
        else:
            pass

        output += row_decoded
        previous_row = row_decoded

    return output
