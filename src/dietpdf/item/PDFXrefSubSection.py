__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from .PDFItem import PDFItem


class PDFXrefSubSection(PDFItem):
    """A PDF cross-reference subsection.

    These objects are meant to be included in PDFXref objects.
    """

    def __init__(self, base: int, count: int):
        """Create a PDFXrefSubsection.

        A PDFXrefSubsection is a cross-reference table starting at a base
        number for a specified number of arguments.

        :param base: Starting number
        :type base: int
        :param count: Number of entries
        :type count: int
        """

        assert type(base) == int
        assert type(count) == int

        self.base = base
        self.count = count
        self.entries = []
        self.first_entry_offset = None

    def __bool__(self):
        """A PDFXrefSubsection is True if it contains entries, False
        otherwise.
        """
        return self.entries != None and len(self.entries) > 0

    def __eq__(self, other):
        """Equality operator for PDFXrefSubsection.

        A PDFXrefSubsection is:

          - equal to any other PDFXrefSubsection with the same base, count and
            entries
          - different from any other PDFItem subclass

        Comparing a PDFXrefSubsection with anything else is not implemented.

        :param other: The object to compare to our current object
        :type other: any
        :return: True or False or NotImplemented
        :type: bool
        """
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
