"""

Run:
- `python3 setup.py install` to install `dietpdf` globally
- or `python3 setup.py install --home=~` to install `dietpdf` locally

You may need to run `pip3 install .` to install the package.

"""

__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

import argparse
import logging
import sys

from .parser.PDFParser import PDFParser
from .processor.PDFProcessor import PDFProcessor
from .item.PDFObject import PDFObject
from .item.PDFList import PDFList
from .item.PDFDictionary import PDFDictionary
from .info.decode_objstm import convert_objstm
from . import __version__

_logger = logging.getLogger(__name__)


def infopdf(input_pdf_name: str):
    """Reduce PDF file size

    Args:
      input_pdf_name (str): the PDF to reduce
    """

    # Read PDF
    pdf_file_content = open(input_pdf_name, "rb").read()
    processor = PDFProcessor()
    parser = PDFParser(processor)
    parser.parse(pdf_file_content)
    processor.end_parsing()
    convert_objstm(processor.tokens)

    pdf = processor.tokens

    # Print all hyperlinks.
    def any_link(_, item): return (
        type(item) == PDFObject and type(item.value) == PDFDictionary and
        b"Type" in item.value and item.value[b"Type"] == b"Annot" and
        b"Subtype" in item.value and item.value[b"Subtype"] == b"Link"
    )

    urls = set()
    for _, object in pdf.find(any_link):
        link = pdf.get(object, ["A", "URI"])
        if link:
            urls.add(link.to_string())

    print("[HYPERLINK]")
    for url in urls:
        print(url)

    print()

    # Print all filters used.
    def any_filter(_, item): return (
        type(item) == PDFObject and
        type(item.value) == PDFDictionary and b"Filter" in item.value
    )

    filters = set()
    for _, object in pdf.find(any_filter):
        filter = object.value[b"Filter"]

        if type(filter) == PDFList:
            for item in filter:
                filters.add(str(item))
        else:
            filters.add(str(object.value[b"Filter"]))

    print("[FILTER]")
    for filter in filters:
        print(filter)

    print()

def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Aims at reducing PDF size")

    parser.add_argument(
        "--version",
        action="version",
        version="dietpdf {ver}".format(ver=__version__),
    )

    parser.add_argument(
        dest="input_pdf",
        help="the PDF to get info from",
        type=str,
        metavar="<input PDF>"
    )

    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )

    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )

    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel,
        stream=sys.stdout,
        format=logformat,
        datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Getting info about a PDF")

    infopdf(args.input_pdf)

    _logger.info("PDF info done")


def run():
    """Entry point for console_scripts"""
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
