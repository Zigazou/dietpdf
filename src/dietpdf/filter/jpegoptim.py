__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from logging import getLogger
from subprocess import Popen, PIPE
from shutil import which

_logger = getLogger("jpegoptim")


def jpegtran_optimize(content: bytes) -> bytes:
    """Optimize a JPEG using Jpegtran.
    """

    assert type(content) == bytes

    if which("jpegtran") == None or which("jpegoptim") == None:
        return None

    streams = {}

    # Run jpegoptim in progressive mode.
    streams["OPT-PRG"] = Popen(
        ["jpegoptim",
         "--all-progressive",
         "--max=90",
         "--strip-all",
         "--stdin", "--stdout"
        ],
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE
    ).communicate(content)[0]

    # Run jpegoptim in baseline mode.
    streams["OPT-BSL"] = Popen(
        ["jpegoptim",
         "--all-normal",
         "--max=90",
         "--strip-all",
         "--stdin", "--stdout"
        ],
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE
    ).communicate(content)[0]

    # Run jpegtran in progressive mode.
    streams["TRA-PRG"] = Popen(
        ["jpegtran", "-trim", "-optimize", "-copy", "none", "-progressive"],
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE
    ).communicate(content)[0]

    # Run jpegtran in baseline mode.
    streams["TRA-BSL"] = Popen(
        ["jpegtran", "-trim", "-optimize", "-copy", "none"],
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE
    ).communicate(content)[0]

    # Find best size.
    (best_opt, best_size) = ("NONE", len(content))
    for opt in streams:
        size = len(streams[opt])
        if size < best_size:
            (best_opt, best_size) = (opt, size)

    _logger.debug("Best JPEG optimization = %s" % best_opt)
    return streams[best_opt]


def jpeg_cmyk_to_rgb(jpeg_cmyk: bytes) -> bytes:
    profile_srgb = "/usr/share/color/icc/sRGB.icm"
    profile_cmyk = "/usr/share/color/icc/ISOcoated.icc"

    jpeg_rgb = Popen(
        ["convert",
         "-profile", profile_cmyk, "jpeg:-",
         "-negate",
         "-profile", profile_srgb, "jpeg:-"
        ],
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE
    ).communicate(jpeg_cmyk)[0]

    return jpeg_rgb

def jpeg_to_jpeg2000(image: bytes) -> bytes:
    convert = Popen(
        ["convert",
         "jpeg:-",
         "-quality", "60",
         "jp2:-"
        ],
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE
    )

    jpeg2000 = convert.communicate(image)[0]
    if convert.returncode:
        return None
    else:
        return jpeg2000
