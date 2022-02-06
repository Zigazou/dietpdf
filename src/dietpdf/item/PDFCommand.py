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
        """
        self.command = command

    def __bool__(self):
        return self.command != None and len(self.command) > 0

    def __eq__(self, other):
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

    def need_space_before(self, item):
        raise Exception("The need_space_before method has not been implemented")
