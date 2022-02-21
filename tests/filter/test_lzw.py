__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from random import seed, randrange
from dietpdf.filter.lzw import lzw_decode, lzw_encode


def test_lzw_decode():
    seed(2022)

    assert lzw_decode(b"\x80\x0B\x60\x50\x22\x0C\x0C\x85\x01") == b"-----A---B"
    assert lzw_encode(b"-----A---B") == b"\x80\x0B\x60\x50\x22\x0C\x0C\x85\x01"

    assert lzw_decode(lzw_encode(b"Hello, World!")) == b"Hello, World!"

    for _ in range(10):
        dummy = bytes(
            [randrange(256) for _ in range(100 + randrange(8192))]
        )

        dummy_compressed = lzw_encode(dummy)
        dummy_uncompressed = lzw_decode(dummy_compressed)

        assert dummy_uncompressed == dummy
