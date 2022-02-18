from random import seed, randrange

from dietpdf.filter.rle import rle_encode, rle_decode

__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"


def test_rle_encode_decode():
    seed(2022)

    assert rle_encode(b"") == b""
    assert rle_encode(b"a") == b"\000a"
    assert rle_encode(b"aaaaaaaaaaaa") == b"\365a"
    assert rle_encode(b"aaaaaaaaaaaabbbbbbbbbbbb") == b"\365a\365b"
    assert rle_encode(b"aaaaaaaaaaaabbbbbbbbbbbbcd") == b"\365a\365b\001cd"
    assert rle_decode(b"") == b""
    assert rle_decode(b"\365a") == b"aaaaaaaaaaaa"
    assert rle_decode(b"\365a\365b") == b"aaaaaaaaaaaabbbbbbbbbbbb"
    assert rle_decode(b"\365a\365b\000c\000d") == b"aaaaaaaaaaaabbbbbbbbbbbbcd"
    very_long = b"a" * 2048 + b"x" + b"a" * 4096
    assert rle_decode(rle_encode(very_long)) == very_long

    for _ in range(128):
        stream = bytes(
            [randrange(256) for _ in range(randrange(2000))]
        )

        print(stream)
        print(rle_encode(stream))

        stream_encoded_decoded = rle_decode(rle_encode(stream))

        assert stream_encoded_decoded == stream
