from random import seed, randrange
from zlib import compress, decompress

from dietpdf.filter.zopfli import zopfli_deflate

__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"


def test_filter_zopfli_deflate():
    seed(2022)

    for _ in range(10):
        dummy = bytes(
            [randrange(256) for _ in range(100 + randrange(1024))]
        )

        dummy_compressed_zopfli = zopfli_deflate(dummy)
        dummy_compressed_zlib = compress(dummy, 9)
        dummy_uncompressed = decompress(dummy_compressed_zopfli)

        assert len(dummy_compressed_zopfli) > 0
        assert len(dummy_compressed_zopfli) < (len(dummy_uncompressed) + 12)
        assert len(dummy_compressed_zopfli) <= len(dummy_compressed_zlib)
        assert dummy == dummy_uncompressed
