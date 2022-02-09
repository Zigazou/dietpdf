__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from ..pdf import PDF
from ..item import PDFObject, PDFDictionary


def all_uri(pdf: PDF) -> list:
    """Retrieve all URIs in a PDF.

    :param pdf: The PDF object from which to extract URIs
    :type pdf: PDF
    :return: A list of URIs (str)
    :rtype: list
    """

    assert type(pdf) == PDF

    # URIs are conteained in annotation objects in a PDF file.
    def any_link(_, item): return (
        type(item) == PDFObject and type(item.value) == PDFDictionary and
        "Type" in item.value and item.value["Type"] == b"Annot" and
        "Subtype" in item.value and item.value["Subtype"] == b"Link"
    )

    urls = set()
    for _, object in pdf.find(any_link):
        urls.add(pdf.get(object, ["A", "URI"]).to_string())

    return list(urls)
