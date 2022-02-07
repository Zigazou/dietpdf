from dietpdf.item import PDFObject, PDFNumber, PDFDictionary

__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"


def test_PDFObject_bool():
    object_number_true = PDFObject(1, 0, PDFNumber(2022), None)
    object_number_false = PDFObject(1, 0, PDFNumber(0), None)
    object_dictionary_true = PDFObject(1, 0, PDFDictionary({"a": 1}), None)
    object_dictionary_false = PDFObject(1, 0, PDFDictionary({}), None)

    assert object_number_true and True
    assert not object_number_false
    assert object_dictionary_true and True
    assert not object_dictionary_false
