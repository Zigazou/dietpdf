__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from .PDFItem import PDFItem

class PDFXrefSubSection(PDFItem):
    """A PDF cross-reference subsection"""

    def __init__(self, base: int, count: int):
        self.base = base
        self.count = count
        self.entries = []
        self.first_entry_offset = None

    def __bool__(self):
        return self.entries != None and len(self.entries) > 0

    def __eq__(self, other):
        if isinstance(other, PDFXrefSubSection):
            return (
                self.base == other.base and
                self.count == other.count and
                self.entries == other.entries
            )
        elif isinstance(other, PDFItem):
            return False
        else:
            return NotImplemented

    def encode(self) -> bytes:
        output = b"%d %d\n" % (self.base, self.count)
        self.first_entry_offset = len(output)
        for (ref_offset, ref_new, ref_type) in self.entries:
            output += b"%010d %05d %s \n" % (
                ref_offset,
                ref_new,
                ref_type.encode('ascii')
            )

        return output

    def pretty(self) -> str:
        return self._pretty("XREFSubsection(%d, %d)" % (self.base, self.count))
