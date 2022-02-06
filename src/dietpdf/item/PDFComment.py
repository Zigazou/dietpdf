__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from .PDFItem import PDFItem

class PDFComment(PDFItem):
    """A PDF comment.
    
    It starts with a "%" and ends with a newline (either `\\r\\n` or `\\n`)
    """

    def __init__(self, content: bytes):
        self.content = content

    def __bool__(self):
        return self.content != None and len(self.comment) > 0

    def __eq__(self, other):
        if isinstance(other, PDFComment):
            return self.content == other.content
        elif isinstance(other, bytes):
            return self.content == other
        elif isinstance(other, PDFItem):
            return False
        else:
            return NotImplemented

    def encode(self) -> bytes:
        return self.content + b"\n"

    def pretty(self) -> str:
        return self._pretty("Comment(%s)" % (str(self.content),))
