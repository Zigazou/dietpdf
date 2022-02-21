__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

import re
import csv
from os.path import getsize
from subprocess import Popen, PIPE

from testdata import pdf_file_uris


def get_info(pdf_file):
    infos = Popen(
        ["pdfinfo", pdf_file],
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE
    ).communicate()[0].decode("utf-8").splitlines()

    creator = ""
    producer = ""
    pdf_version = ""
    for info in infos:
        if info.startswith("Creator:"):
            creator = info[8:].strip()

        if info.startswith("Producer:"):
            producer = info[9:].strip()

        if info.startswith("PDF version:"):
            pdf_version = info[12:].strip()

    return (creator, producer, pdf_version)


def qpdf_check(pdf_opt_check_file):
    qpdf_output = open(pdf_opt_check_file, "r").read()

    if "ERROR:" in qpdf_output:
        return "error"

    if "WARNING:" in qpdf_output:
        return "warning"

    return "ok"


def gs_check(pdf_opt_check_file):
    gs_output = open(pdf_opt_check_file, "r").read()

    if "Error" in gs_output:
        return "error"

    return "ok"

def get_compare(compare_file):
    pages = open(compare_file, "r").read().splitlines()
    problems = []
    for index in range(len(pages)):
        if float(pages[index]) > 45000.0:
            problems.append(index + 1)

    if problems:
        return "warning({})".format(" ".join([str(page) for page in problems]))
    else:    
        return "ok"

FIELD_FILENAME = "File name"
FIELD_SIZE_BEFORE = "Size before"
FIELD_SIZE_AFTER = "Size after"
FIELD_REDUCTION = "Reduction"
FIELD_QPDF_CHECK = "QPDF check"
FIELD_GS_CHECK = "GS check"
FIELD_COMPARE_GS = "Diff/GS"
FIELD_COMPARE_CAIRO = "Diff/Cairo"
FIELD_CREATOR = "Creator"
FIELD_PRODUCER = "Producer"
FIELD_PDF_VERSION = "PDF"
FIELD_URI = "URI"

fieldnames = [
    FIELD_FILENAME,
    FIELD_SIZE_BEFORE,
    FIELD_SIZE_AFTER,
    FIELD_REDUCTION,
    FIELD_QPDF_CHECK,
    FIELD_GS_CHECK,
    FIELD_COMPARE_GS,
    FIELD_COMPARE_CAIRO,
    FIELD_CREATOR,
    FIELD_PRODUCER,
    FIELD_PDF_VERSION,
    FIELD_URI,
]

total_before = 0
total_after = 0
with open('dietpdf-results.csv', 'w', newline='') as csvfile:
    results = csv.DictWriter(csvfile, fieldnames=fieldnames,
                             quoting=csv.QUOTE_NONNUMERIC)

    results.writeheader()

    for pdf_file, url in pdf_file_uris:
        pdf_opt_file = re.sub("\.pdf$", ".opt.pdf", pdf_file)
        size_before = getsize(pdf_file)
        total_before += size_before
        size_after = getsize(pdf_opt_file)
        total_after += size_after
        creator, producer, pdf_version = get_info(pdf_file)

        results.writerow({
            FIELD_FILENAME: pdf_file,
            FIELD_SIZE_BEFORE: size_before,
            FIELD_SIZE_AFTER: size_after,
            FIELD_REDUCTION: (size_before - size_after) / size_before,
            FIELD_QPDF_CHECK: qpdf_check(pdf_opt_file + ".qpdf-check"),
            FIELD_GS_CHECK: gs_check(pdf_opt_file + ".gs-check"),
            FIELD_COMPARE_GS: get_compare(pdf_file + ".compare-gs"),
            FIELD_COMPARE_CAIRO: get_compare(pdf_file + ".compare-cairo"),
            FIELD_CREATOR: creator,
            FIELD_PRODUCER: producer,
            FIELD_PDF_VERSION: str(pdf_version),
            FIELD_URI: url,
        })

    results.writerow({
        FIELD_FILENAME: "TOTAL",
        FIELD_SIZE_BEFORE: total_before,
        FIELD_SIZE_AFTER: total_after,
        FIELD_REDUCTION: (total_before - total_after) / total_before,
        FIELD_QPDF_CHECK: "",
        FIELD_COMPARE_GS: "",
        FIELD_COMPARE_CAIRO: "",
        FIELD_CREATOR: "",
        FIELD_PRODUCER: "",
        FIELD_PDF_VERSION: "",
        FIELD_URI: "",
    })
