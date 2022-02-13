__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from subprocess import Popen, PIPE
from shutil import which


def jpegtran_optimize(content: bytes) -> bytes:
    """Optimize a JPEG using Jpegtran.
    """

    assert type(content) == bytes

    if which("jpegtran") == None:
        return None

    # Run jpegtran discarding anything unneeded in the JPEG file.
    optimized = Popen(
        ["jpegtran", "-trim", "-optimize", "-copy", "none", "-progressive"],
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE
    ).communicate(content)[0]

    return optimized
