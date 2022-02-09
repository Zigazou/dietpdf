__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from .PDFItem import PDFItem


class PDFCommand(PDFItem):
    """A PDF command.

    Contrary to a PDF name (starting with a "/"), a PDF command may imply an
    interpretation upon its pushing on the processor stack.
    """

    def __init__(self, command: bytes):
        """Create a `PDFCommand` object.

        :param command: The command without any leading or trailing white space.
        ;type command: bytes
        """

        assert type(command) == bytes
        assert len(command) > 0

        self.command = command

    def __bool__(self):
        return self.command != None and len(self.command) > 0

    def __eq__(self, other):
        """Equality operator for PDFCommand.

        A PDFCommand is:

          - equal to any other PDFCommand with the same byte string
          - equal to any byte string with the same byte string
          - different from any other PDFItem subclass

        Comparing a PDFCommand with anything else is not implemented.

        :param other: The object to compare to our current object
        :type other: any
        :return: True or False or NotImplemented
        :type: bool
        """
        if isinstance(other, PDFCommand):
            return self.command == other.command
        elif isinstance(other, bytes):
            return self.command == other
        elif isinstance(other, PDFItem):
            return False
        else:
            return NotImplemented

    def pretty(self) -> str:
        return self._pretty("Command(%s)" % (self.command.decode('ascii'),))

    def encode(self) -> bytes:
        return self.command
