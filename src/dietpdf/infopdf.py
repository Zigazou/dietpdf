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
from .item.PDFReference import PDFReference
from .item.PDFTrailer import PDFTrailer
from .item.deep_find import deep_find
from .info.decode_objstm import convert_objstm
from . import __version__

_logger = logging.getLogger(__name__)


def info_hyperlinks(pdf):
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

    return urls

def info_filters(pdf):
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

    return filters

def info_types(pdf):
    def any_object_with_type(_, item): return type(item) == PDFObject

    labels = {}
    for _, object in pdf.find(any_object_with_type):
        if type(object.value) == PDFDictionary:
            if b"Type" in object:
                if b"Subtype" in object:
                    label = "%s/%s" % (
                        str(object.value[b"Type"]),
                        str(object.value[b"Subtype"])
                    )
                else:
                    label = "%s" % str(object.value[b"Type"])
            elif b"Linearized" in object:
                label = "(Linearized)"
            else:
                label = ""
        else:
            label = ""

        stream = object.has_stream()

        labels[object.obj_num] = (label, stream)

    return labels

def info_graph(pdf):
    def any_object(_, item): return type(item) == PDFObject
    def any_reference(_, item): return type(item) == PDFReference
    def any_trailer(_, item): return type(item) == PDFTrailer

    directed_links = set()
    for _, object in pdf.find(any_object):
        for path, item in deep_find(object, any_reference):
            if type(path[-1]) == int and len(path) > 1:
                relation = "%s[%d]" % (path[-2], path[-1])
            else:
                relation = path[-1]
            directed_links.add((object.obj_num, relation, item.obj_num))

    for index, object in pdf.find(any_trailer):
        for path, item in deep_find(object, any_reference):
            if type(path[-1]) == int and len(path) > 1:
                relation = "%s[%d]" % (path[-2], path[-1])
            else:
                relation = path[-1]
            directed_links.add(("trailer-%s" % index, relation, item.obj_num))

    return directed_links

ALL_INFO = "all"

def infopdf(infotype: str, input_pdf_name: str):
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
    if infotype in [ALL_INFO, "hyperlink"]:
        print("/* hyperlink */")
        for url in info_hyperlinks(pdf):
            print(url)

        print()

    # Print all filters used.
    if infotype in [ALL_INFO, "filter"]:
        print("/* filter */")
        for filter in info_filters(pdf):
            print(filter)

        print()

    # Print all relations.
    if infotype in [ALL_INFO, "graph"]:
        print("/* graph */")
        print("digraph {")

        print("  rankdir = LR;")
        print("  splines = polyline;")
        print(
            "  node ["
            "shape=rectangle, "
            "fontname=\"IBM Plex Sans Condensed:style=Regular\""
            "]"
        )

        print(
            "  edge ["
            "fontname=\"IBM Plex Sans Condensed:style=Regular\""
            "]"
        )

        labels = info_types(pdf)

        pages = [
            "%d;" % obj_num
            for obj_num in labels
            if labels[obj_num][0] == "Page"
        ]

        catalogs = [
            "%d;" % obj_num
            for obj_num in labels
            if labels[obj_num][0] == "Catalog" or labels[obj_num][0] == "Pages"
        ]

        pagess = [
            "%d;" % obj_num
            for obj_num in labels
            if labels[obj_num][0] == "Pages"
        ]

        print("  subgraph cluster_page { rank = same; %s }" % " ".join(pages))
        print("  subgraph cluster_catalog { rank = same; %s }" % " ".join(catalogs))
        """
        print("  subgraph cluster_pages { rank = same; %s }" % " ".join(pagess))
        """

        for obj_num in labels:
            label, stream = labels[obj_num]

            if stream:
                if label:
                    print(
                        "  \"%s\" [shape=record, label=\"{{%s|(✉)}|%s}\"]" %
                        (obj_num, obj_num, label)
                    )
                else:
                    print(
                        "  \"%s\" [shape=record, label=\"%s|(✉)\"]" %
                        (obj_num, obj_num)
                    )
            else:
                if label:
                    print(
                        "  \"%s\" [shape=record, label=\"{%s|%s}\"]" %
                        (obj_num, obj_num, label)
                    )
                else:
                    print("  \"%s\" [label=\"%s\"]" % (obj_num, obj_num))

        for origin, relation, destination in info_graph(pdf):
            print(
                "  \"%s\" -> \"%s\" [label=\"%s\"]" %
                (origin, destination, relation)
            )

        print("}")
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
        dest="infotype",
        help="type of information to extract",
        type=str,
        metavar="[all|hyperlink|filter|graph]"
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

    infopdf(args.infotype, args.input_pdf)

    _logger.info("PDF info done")


def run():
    """Entry point for console_scripts"""
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
