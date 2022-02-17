__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"


from dietpdf.parser.PDFParser import PDFParser
from dietpdf.processor.PDFProcessor import PDFProcessor
from dietpdf.info.all_uri import all_uri


def test_all_uri():
    pdf_file_content = open(
        "pdf-examples/libreoffice-writer-hyperlink.pdf", "rb"
    ).read()

    processor = PDFProcessor()
    parser = PDFParser(processor)
    parser.parse(pdf_file_content)
    processor.end_parsing()

    expected_result = [
        "https://www.example.com/1",
        "https://www.example.com/2"
    ]

    uris = sorted(all_uri(processor.tokens))

    assert uris == expected_result
