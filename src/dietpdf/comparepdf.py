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
import re

from dietpdf.item import PDFDictionary

from .parser import PDFParser
from .processor import PDFProcessor
from .item import PDFObject, PDFReference
from dietpdf import __version__

_logger = logging.getLogger("dietpdf")


def pdfcompare(first_pdf: str, second_pdf: str):
    """Compare visual rendering of two PDF files

    Args:
      first_pdf (str): first PDF path
      second_pdf (str): second PDF path
    """

    output_pdf_name = re.sub("\.pdf$", ".opt.pdf", input_pdf_name)

    # Read PDF.
    _logger.info("Reading %s" % input_pdf_name)
    pdf_file_content = open(input_pdf_name, "rb").read()
    processor = PDFProcessor()
    parser = PDFParser(processor)
    parser.parse(pdf_file_content)
    processor.end_parsing()

    # Find all source code streams
    source_codes = set()
    for object_id in processor.objects:
        object = processor.objects[object_id]

        if not isinstance(object.value, PDFDictionary):
            continue

        if b"Type" in object and object[b"Type"] == b"XRef":
            print(
                "Sorry, dietpdf doesn't know how to handle cross-reference "
                "objects for the moment!"
            )
            return

        if b"Type" in object and object[b"Type"] == b"XObject":
            if b"Subtype" in object and object[b"Subtype"] == b"Form":
                source_codes.add(object.obj_num)
        elif b"Contents" in object and isinstance(object[b"Contents"], PDFReference):
            source_codes.add(object[b"Contents"].obj_num)

    for object_id in processor.objects:
        object = processor.objects[object_id]
        object.source_code = object.obj_num in source_codes

    # Optimize streams.
    _logger.info("Start optimizing objects and streams")
    for object_id in processor.objects:
        object = processor.objects[object_id]
        if isinstance(object, PDFObject) and object.has_stream():
            _logger.info("Optimizing object %d stream" % object.obj_num)
            object.optimize_stream()

    # Write PDF.
    _logger.info("Updating cross-reference table")
    processor.update_xref(pdf_file_content)
    _logger.info("Writing optimized PDF in %s" % output_pdf_name)
    open(output_pdf_name, "wb").write(processor.encode())

    processor.pretty_print()


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
        help="the PDF for which to reduce size",
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
    _logger.info("Start optimizing PDF %s" % args.input_pdf)

    diet(args.input_pdf)


def run():
    """Entry point for console_scripts"""
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
