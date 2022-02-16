__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from ..token.PDFToken import PDFToken

from .PDFItem import PDFItem


class PDFObjectID(PDFItem):
    """A PDF object ID"""

    def __init__(self, obj_num: int, gen_num: int):
        """Create a PDFObjectID.

        :param obj_num: The object number
        :type obj_num: int
        :param gen_num: The generation number (usually 0)
        :type gen_num: int
        """
        assert type(obj_num) == int
        assert type(gen_num) == int

        self.obj_num = obj_num
        self.gen_num = gen_num

    def __eq__(self, other):
        """Equality operator for PDFObjectID.

        A PDFObjectID is:

          - equal to any other PDFObjectID with the same object number and
            generation number
          - equal to a tuple (int, int) with the same object number and
            generation number
          - different from any other PDFToken subclass

        Comparing a PDFObjectID with anything else (including tuple with more
        than 2 elements) is not implemented.

        :param other: The object to compare to our current object
        :type other: any
        :return: True or False or NotImplemented
        :type: bool
        """
        if isinstance(other, PDFObjectID):
            return (
                self.obj_num == other.obj_num and
                self.gen_num == other.gen_num
            )
        elif isinstance(other, tuple):
            if len(other) == 2:
                return self.obj_num == other[0] and self.gen_num == other[1]
            else:
                return NotImplemented
        elif isinstance(other, PDFToken):
            return False
        else:
            return NotImplemented

    def __bool__(self):
        """A PDFObjectID is always True."""
        return True

    def pretty(self) -> str:
        return self._pretty("ObjectID(%d,%d)" % (self.obj_num, self.gen_num))

    def encode(self) -> bytes:
        return b"%d %d obj" % (self.obj_num, self.gen_num)
