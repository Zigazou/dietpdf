__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from ..item.PDFObject import PDFObject
from ..item.PDFDictionary import PDFDictionary
from ..item.PDFList import PDFList
from ..item.PDFStream import PDFStream
from ..item.PDFReference import PDFReference
from ..pdf.PDF import PDF


def group_contents(pdf: PDF):
    """Groups contents objects contained in the same page object.

    :param pdf: The PDF file for which to group contents objects.
    :type pdf: PDF
    """

    # Find pages with contents list.
    def any_page_with_contents_list(_, item):
        return (
            type(item) == PDFObject and type(item.value) == PDFDictionary and
            b"Type" in item and item[b"Type"] == b"Page" and
            b"Contents" in item and type(item[b"Contents"]) == PDFList and
            len(item[b"Contents"]) > 1
        )

    objects_to_remove = []
    for _, item in pdf.find(any_page_with_contents_list):
        grouped_contents = b" ".join([
            pdf.get(reference).decode_stream()
            for reference in item[b"Contents"]
        ])

        # The first content object will receive the groupd contents stream.
        first_content = pdf.get(item[b"Contents"][0])
        first_content.stream = PDFStream(grouped_contents)

        if b"Filter" in first_content:
            first_content.value.delete(b"Filter")

        if b"DecodeParms" in first_content:
            first_content.value.delete(b"DecodeParms")

        for index in range(1, len(item[b"Contents"])):
            objects_to_remove.append(item[b"Contents"][index].obj_num)

        item.value[b"Contents"] = PDFReference(first_content)

    # Remove contents that have been grouped.
    def any_grouped_contents(_, item):
        return type(item) == PDFObject and item.obj_num in objects_to_remove

    to_remove = [index for index, _ in pdf.find(any_grouped_contents)]
    to_remove.sort(reverse=True)
    for index in to_remove:
        pdf.pop(index)
