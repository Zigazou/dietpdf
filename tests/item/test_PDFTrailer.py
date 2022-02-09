from dietpdf.item import PDFTrailer, PDFDictionary

__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"


def test_PDFTrailer_bool():
    trailer_true = PDFTrailer(PDFDictionary({"a": 1}))
    trailer_false = PDFTrailer(PDFDictionary({}))

    assert trailer_true and True
    assert not trailer_false
