__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

"""Base class for any PDF item that might be encountered in a PDF file.
"""

class PDFItem:
    """Base class for any PDF item that might be encountered in a PDF file.
    
    This class should not be used directly, it should be derived first.
    """
    item_offset = None

    def __eq__(self, other):
        return NotImplemented

    def __str__(self):
        return self.__class__.__name__

    def __bool__(self):
        """A PDFItem is always False."""
        return False

    def encode(self) -> bytes:
        """Generate a byte string conforming to PDF specifications based on the
        content of the object.
        """
        raise Exception("The encode method has not been implemented")

    def _pretty(self, string: str) -> str:
        """Add the item_offset attribute, if set to the pretty string.

        This method should not be overwritten.

        Returns:
            A string (str)
        """
        if self.item_offset != None:
            return "%s @ %d" % (string, self.item_offset)
        else:
            return "%s" % (string,)

    def pretty(self) -> str:
        """Pretty print the object for debugging purposes.
        
        When this method is implemented, it should call the `_pretty` protected
        method to generate the resulting string.

        Returns:
            A string (str)
        """
        return self._pretty(self.__class__.__name__[3:])
