__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from subprocess import Popen, PIPE
from shutil import which


def compare_pdf(original: str, optimized: str) -> list:
    """Compares two PDF files visually using ImageMagick.

    This function assumes the PDFs have the same number of pages.

    :param original: The path to the original PDF
    :type original: str
    :param original: The path to the optimized PDF
    :type original: str
    :return: a list of difference rate for each page of None if ImageMagick's
        convert has not been found.
    :rtype: list or None
    """

    assert type(original) == str
    assert type(optimized) == str

    if which("convert") == None:
        return None

    page_num = 0
    differences = []

    while True:
        comparison = Popen(
            ["convert",
            "-density", "300",
            "%s[%d]" % (original, page_num),
            "-density", "300",
            "%s[%d]" % (optimized, page_num),
            "-metric", "AE",
            "-compare",
            "-format", "%[distortion]",
            "info:"
            ],
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE
        )

        output = comparison.communicate()[0]
        if comparison.returncode:
            break

        differences.append(float(output))
        page_num += 1

    return differences
