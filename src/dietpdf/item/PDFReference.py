__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from .PDFItem import PDFItem
from .PDFObject import PDFObject

class PDFReference(PDFItem):
    """A PDF reference to a PDF object"""

    def __init__(self, obj_num: int, gen_num: int):
        if isinstance(obj_num, PDFObject):
            self.obj_num = obj_num.obj_num
            self.gen_num = obj_num.gen_num
        else:
            self.obj_num = obj_num
            self.gen_num = gen_num

    def __bool__(self):
        return True

    def __eq__(self, other):
        if isinstance(other, PDFReference):
            return (
                self.obj_num == other.obj_num and
                self.gen_num == other.gen_num
            )
        elif isinstance(other, tuple):
            if len(other) == 2:
                return self.obj_num == other[0] and self.gen_num == other[1]
            else:
                return NotImplemented
        elif isinstance(other, PDFItem):
            return False
        else:
            return NotImplemented

    def pretty(self) -> str:
        return self._pretty("Reference(%d, %d)" % (self.obj_num, self.gen_num))

    def encode(self) -> bytes:
        return b"%d %d R" % (self.obj_num, self.gen_num)
