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

from dietpdf.parser.PDFParser import PDFParser
from dietpdf.processor.PDFProcessor import PDFProcessor
from dietpdf.item import PDFObject
from dietpdf.info import all_source_codes
from dietpdf import __version__

_logger = logging.getLogger(__name__)


def extractpdf(input_pdf_name: str, base: str):
    """Extract streams to files

    Args:
      input_pdf_name (str): the PDF to work on
      base (str): base for generated files
    """

    # Read PDF
    pdf_file_content = open(input_pdf_name, "rb").read()
    processor = PDFProcessor()
    parser = PDFParser(processor)
    parser.parse(pdf_file_content)
    processor.end_parsing()

    # Find all content objects
    content_objects_set = all_source_codes(processor.tokens)

    # Extract all available streams
    any_object_with_stream = lambda _, item: (
        type(item) == PDFObject and
        item.stream != None        
    )
    for _, object in processor.tokens.find(any_object_with_stream):
        object_id = object.obj_num
        extension = "raw"
        width = None
        height = None
        if b"Type" in object and object[b"Type"] == b"XObject":
            if b"Subtype" in object and object[b"Subtype"] == b"Form":
                extension = "form-xobject"
        elif object.obj_num in content_objects_set:
            extension = "content"
        elif b"Subtype" in object and object[b"Subtype"] == b"Image":
            width = int(object[b"Width"])
            height = int(object[b"Height"])

            if b"Filter" in object and object[b"Filter"] == b"DCTDecode":
                extension = "%dx%d.jpg" % (width, height)
            else:
                extension = "%dx%d.picture" % (width, height)

        filtered = object.decode_stream()
        output_file_name = "%s-%d.%s" % (base, object_id, extension)
        with open(output_file_name, "wb") as output_file:
            output_file.write(filtered)

        print(output_file_name)

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
        help="the PDF to get info from",
        type=str,
        metavar="<input PDF>"
    )

    parser.add_argument(
        dest="base",
        help="base name/path that will be used to extract to",
        type=str,
        metavar="<base>"
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

    extractpdf(args.input_pdf, args.base)

    _logger.info("PDF info done")


def run():
    """Entry point for console_scripts"""
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
