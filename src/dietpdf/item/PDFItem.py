__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

"""Base class for any PDF item that might be encountered in a PDF file.
"""

from ..token.PDFToken import PDFToken


class PDFItem(PDFToken):
    """Base class for any PDF item that might be encountered in a PDF file.
    
    This class should not be used directly, it should be derived first.
    """
    pass