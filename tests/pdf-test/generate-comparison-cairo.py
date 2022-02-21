__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from sys import argv

from dietpdf.info.compare_pdf import compare_pdf_cairo

for difference in compare_pdf_cairo(argv[1], argv[2]):
    print(difference)
