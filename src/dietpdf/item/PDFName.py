__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from .PDFItem import PDFItem

class PDFName(PDFItem):
    """A PDF name (starting with /)"""

    def __init__(self, name):
        """Create a new PDFName.

        It sets the name of the PDFName to the name parameter.

        The string must not be empty.

        It can get its name from:
        
          - another PDFName
          - a byte string
          - a unicode string which must use only ASCII characters

        :param name: name to set.
        :type name: PDFName or str or bytes
        """
        assert type(name) in [PDFName, str, bytes]

        if type(name) == PDFName:
            self.name = name.name
        elif type(name) == str:
            assert len(name) > 0
            self.name = name.encode('ascii')
        else:
            assert len(name) > 0
            self.name = name

    def __hash__(self) -> int:
        """Hash of a PDFName
        
        The hash of a PDFName is simply the hash of its byte string name.

        :return: The hash
        :rtype: int
        """
        return hash(self.name)

    def __eq__(self, other):
        """Equality operator for PDFName.

        A PDFName is:
        
          - equal to any other PDFName with the same byte string
          - equal to any byte string with the same byte string
          - different from any other PDFItem subclass

        Comparing a PDFName with anything else is not implemented.

        :param other: The object to compare to our current object
        :type other: any
        :return: True or False or NotImplemented
        :type: bool
        """
        if type(other) == PDFName:
            return self.name == other.name
        elif type(other) == bytes:
            return self.name == other
        elif isinstance(other, PDFItem):
            return False
        else:
            return NotImplemented

    def __str__(self) -> str:
        return self.name.decode('ascii')

    def __bool__(self):
        """A PDFName is True if its name contains bytes (this should always
        happen)."""
        return self.name != None and len(self.name) > 0

    def pretty(self) -> str:
        return self._pretty("Name(%s)" % (self.name.decode('ascii'),))

    def encode(self) -> bytes:
        return b"/" + self.name
