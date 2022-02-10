__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"


from dietpdf.parser.PDFParser import PDFParser
from dietpdf.processor.PDFProcessor import PDFProcessor
from dietpdf.info import all_source_codes


def test_all_source_codes():
    pdf_file_content = open(
        "pdf-examples/libreoffice-writer-hyperlink.pdf", "rb"
    ).read()

    processor = PDFProcessor()
    parser = PDFParser(processor)
    parser.parse(pdf_file_content)
    processor.end_parsing()

    expected_result = [2, 16]

    source_codes = sorted(all_source_codes(processor.tokens))

    assert source_codes == expected_result
