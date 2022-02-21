__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from subprocess import Popen, PIPE
from os import remove
from shutil import which

def get_page_count(pdf_file: str) -> int:
    assert type(pdf_file) == str

    if which("pdfinfo") == None:
        return None

    info = Popen(["pdfinfo", pdf_file], stdin=PIPE, stdout=PIPE, stderr=PIPE)

    lines = info.communicate()[0].splitlines()
    if info.returncode:
        return None

    for line in lines:
        if line.startswith(b"Pages:"):
            return int(line[6:].strip())

    return None


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
            "-density", "50",
            "%s[%d]" % (original, page_num),
            "-density", "50",
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


def compare_pdf_cairo(original: str, optimized: str) -> list:
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

    if which("pdftocairo") == None:
        return None

    page_count = get_page_count(original)

    differences = []
    original_image = original + ".png"
    optimized_image = optimized + ".png"
    for page in range(page_count):
        Popen(
            ["pdftocairo", "-png", "-singlefile", "-f", "%d" % page,
            original, original_image],
            stdin=PIPE, stdout=PIPE, stderr=PIPE
        ).communicate()

        Popen(
            ["pdftocairo", "-png", "-singlefile", "-f", "%d" % page,
            optimized, optimized_image],
            stdin=PIPE, stdout=PIPE, stderr=PIPE
        ).communicate()

        comparison = Popen(
            ["convert", original_image + ".png", optimized_image + ".png",
            "-metric", "AE",
            "-compare", "-format", "%[distortion]",
            "info:"
            ],
            stdin=PIPE, stdout=PIPE, stderr=PIPE
        )

        output = comparison.communicate()[0]
        differences.append(float(output))

    remove(original_image + ".png")
    remove(optimized_image + ".png")

    return differences
