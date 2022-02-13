__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from subprocess import Popen, PIPE
from shutil import which


class UnableToLZWEncode(Exception):
    pass


class UnableToLZWDecode(Exception):
    pass


def lzw_encode(content: bytes) -> bytes:
    """Compress a byte string using LZW."""

    assert type(content) == bytes

    if which("compress") == None:
        return None

    child = Popen(
        ["compress", "-b", "12"],
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE
    )

    output = child.communicate(content)[0]

    # Only return code 1 is really an error, return code 2 means the compressed
    # content is larger than the uncompressed content.
    if child.returncode == 1:
        raise UnableToLZWEncode(
            "Compress returned with rc=%d" % child.returncode
        )
    else:
        # Get rid of the first 3 bytes of the .Z format.
        return output[3:]


def lzw_decode(content: bytes) -> bytes:
    """Uncompress a byte string using LZW."""

    assert type(content) == bytes

    if which("uncompress.real") == None:
        return None

    child = Popen(
        ["uncompress.real", "-c"],
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE
    )

    output = child.communicate(b"\x1f\x9d\x8c%s" % content)[0]
    if child.returncode:
        raise UnableToLZWDecode(
            "Uncompress returned with rc=%d" % child.returncode
        )
    else:
        return output
