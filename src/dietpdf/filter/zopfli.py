__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from subprocess import Popen, PIPE
from tempfile import NamedTemporaryFile
from os import remove
from shutil import which


def zopfli_deflate(content: bytes) -> bytes:
    """Compress a byte string using Zopfli.

    This function produces a zlib compatible format. The resulting byte string
    is decompressible using standard zlib functions.
    """
    if which("zopfli") == None:
        return None

    with NamedTemporaryFile(delete=False) as input:
        # Write content to a temporary file because the zopfli command does not
        # handle standard input.
        input.write(content)
        input.close()

        # Run zopfli with an aggressive compression level.
        Popen(
            ["zopfli", input.name, "--zlib", "--i31"],
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE
        ).communicate()

        # zopfli automatically writes the compressed data in a file with a
        # `.zlib` extension.
        output_name = input.name + ".zlib"
        file = open(output_name, "rb")
        deflate = file.read()
        file.close()

        # Remove temporary files.
        remove(output_name)
        remove(input.name)

        return deflate
