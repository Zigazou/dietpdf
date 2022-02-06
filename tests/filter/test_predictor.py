from random import seed, randrange

from dietpdf.filter.predictor import (
    predictor_png_decode, predictor_png_encode,
    ROW_NONE, ROW_SUB, ROW_UP, ROW_AVERAGE, ROW_PAETH
)

__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"


def test_predictor_png_encode_length():
    columns_test = [1, 2, 3, 4, 5, 6, 7, 8]
    colors_test = [1, 2, 3, 4]
    row_predictors = [ROW_NONE, ROW_SUB, ROW_UP, ROW_AVERAGE, ROW_PAETH]

    for row_predictor in row_predictors:
        seed(2022)

        for colors in colors_test:
            for columns in columns_test:
                stream = bytes([
                    randrange(256)
                    for _ in range(columns * colors * randrange(100))
                ])

                stream_encoded = predictor_png_encode(
                    stream, row_predictor, columns, colors
                )

                assert (
                    len(stream_encoded) ==
                    len(stream) + len(stream) // (columns * colors)
                ), (
                    "columns=%d, colors=%d, predictor=%d" %
                    (columns, colors, row_predictor)
                )


def test_predictor_png_encode_decode():
    columns_test = [1, 2, 3, 4, 5, 6, 7, 8]
    colors_test = [1, 2, 3, 4]
    row_predictors = [ROW_NONE, ROW_SUB, ROW_UP, ROW_AVERAGE, ROW_PAETH]

    for row_predictor in row_predictors:
        seed(2022)

        for colors in colors_test:
            for columns in columns_test:
                stream = bytes([
                    randrange(256)
                    for _ in range(columns * colors * randrange(100))
                ])

                stream_encoded_decoded = predictor_png_decode(
                    predictor_png_encode(
                        stream, row_predictor, columns, colors
                    ),
                    columns, colors
                )

                assert len(stream_encoded_decoded) == len(stream), (
                    "columns=%d, colors=%d, predictor=%d" %
                    (columns, colors, row_predictor)
                )
                assert stream_encoded_decoded == stream, (
                    "columns=%d, colors=%d, predictor=%d" %
                    (columns, colors, row_predictor)
                )
