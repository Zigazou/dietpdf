__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

import re

from testdata import pdf_file_uris

# Generate the ALL rule.
print("ALL:", end="")
for pdf_test in pdf_file_uris:
    pdf_file, _ = pdf_test
    pdf_opt_file = re.sub("\.pdf$", ".opt.pdf", pdf_file)
    pdf_opt_qpdf_file = pdf_opt_file + ".qpdf-check"
    pdf_opt_gs_file = pdf_opt_file + ".gs-check"
    compare_file_gs = pdf_file + ".compare-gs"
    compare_file_cairo = pdf_file + ".compare-cairo"

    print(" {} {} {} {} {}".format(
        pdf_opt_file, pdf_opt_qpdf_file, pdf_opt_gs_file, compare_file_gs,
        compare_file_cairo
    ), end="")
print()
print()

# Generate the rules.
for pdf_test in pdf_file_uris:
    pdf_file, url = pdf_test
    pdf_opt_file = re.sub("\.pdf$", ".opt.pdf", pdf_file)
    pdf_opt_qpdf_file = pdf_opt_file + ".qpdf-check"
    pdf_opt_gs_file = pdf_opt_file + ".gs-check"
    compare_file_gs = pdf_file + ".compare-gs"
    compare_file_cairo = pdf_file + ".compare-cairo"

    # Rule for retrieving the PDF file from internet.
    print("{}:".format(pdf_file))
    print("\tcurl --silent \"{}\" -o \"{}\"".format(url, pdf_file))
    print()

    # Rule to use dietpdf against the retrieved PDF file.
    print("{}: {}".format(pdf_opt_file, pdf_file))
    print("\tdietpdf \"{}\"".format(pdf_file))
    print()

    # Rule to run QPDF check against the optimized PDF file.
    print("{}: {}".format(pdf_opt_qpdf_file, pdf_opt_file))
    print("\t-qpdf --suppress-recovery -check \"{}\" > \"{}\"".format(
        pdf_opt_file, pdf_opt_qpdf_file
    ))
    print()

    # Rule to run GhostScript check against the optimized PDF file.
    print("{}: {}".format(pdf_opt_gs_file, pdf_opt_file))
    print("\t-gs -dNOPAUSE -dBATCH -sDEVICE=nullpage {} > {}".format(
        pdf_opt_file, pdf_opt_gs_file
    ))
    print()

    # Rule to compare with Ghostscript the original and the optimized version
    # of the PDF.
    print("{}: {} {}".format(compare_file_gs, pdf_file, pdf_opt_file,))
    print("\tpython3 generate-comparison-gs.py {} {} > {}".format(
        pdf_file, pdf_opt_file, compare_file_gs
    ))
    print()

    # Rule to compare with Cairo the original and the optimized version of the
    # PDF.
    print("{}: {} {}".format(compare_file_cairo, pdf_file, pdf_opt_file,))
    print("\tpython3 generate-comparison-cairo.py {} {} > {}".format(
        pdf_file, pdf_opt_file, compare_file_cairo
    ))
    print()

# Clean rule (clean only the optimized PDF files).
print("clean:")
for pdf_test in pdf_file_uris:
    pdf_file, _ = pdf_test
    pdf_opt_file = re.sub("\.pdf$", ".opt.pdf", pdf_file)
    pdf_opt_qpdf_file = pdf_opt_file + ".qpdf-check"
    pdf_opt_gs_file = pdf_opt_file + ".gs-check"
    compare_file_gs = pdf_file + ".compare-gs"
    compare_file_cairo = pdf_file + ".compare-cairo"

    print("\trm -f -- {} {} {} {} {}".format(
        pdf_opt_file, pdf_opt_qpdf_file, pdf_opt_gs_file, compare_file_gs,
        compare_file_cairo
    ))

print()

# Clean all rule (clean even the downloaded files).
print("clean-all:")
for pdf_test in pdf_file_uris:
    pdf_file, _ = pdf_test
    pdf_opt_file = re.sub("\.pdf$", ".opt.pdf", pdf_file)
    pdf_opt_qpdf_file = pdf_opt_file + ".qpdf-check"
    pdf_opt_gs_file = pdf_opt_file + ".gs-check"
    compare_file_gs = pdf_file + ".compare-gs"
    compare_file_cairo = pdf_file + ".compare-cairo"

    print("\trm -f -- {} {} {} {} {}".format(
        pdf_file, pdf_opt_file, pdf_opt_qpdf_file, pdf_opt_gs_file,
        compare_file_gs, compare_file_cairo
    ))

print()
