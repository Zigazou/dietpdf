__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from shutil import which

from dietpdf.info import compare_pdf

def test_compare_pdf_identical():
    differences = compare_pdf(
        "pdf-examples/libreoffice-writer-loremipsum.pdf",
        "pdf-examples/libreoffice-writer-loremipsum.pdf"
    )

    assert differences != None
    assert len(differences) == 5
    assert differences == [0.0, 0.0, 0.0, 0.0, 0.0]

def test_compare_pdf_small_difference():
    differences = compare_pdf(
        "pdf-examples/libreoffice-writer-loremipsum.pdf",
        "pdf-examples/libreoffice-writer-loremipsum-missingletter.pdf"
    )

    assert differences != None
    assert len(differences) == 5
    assert differences[1:] == [0.0, 0.0, 0.0, 0.0]
    assert differences[0] != 0.0

def test_compare_pdf_optimized():
    differences = compare_pdf(
        "pdf-examples/libreoffice-writer-hyperlink.pdf",
        "pdf-examples/libreoffice-writer-hyperlink.opt.pdf"
    )

    assert differences != None
    assert len(differences) == 1
    assert differences == [0.0]
