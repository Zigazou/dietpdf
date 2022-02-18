__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from .PDFToken import PDFToken


class PDFNumber(PDFToken):
    """A PDF number (either an integer or a float)"""

    def __init__(self, value):
        if type(value) == float or type(value) == int:
            self.value = value
        elif ord('.') in value:
            self.value = float(value)
        else:
            self.value = int(value)

    def __eq__(self, other):
        """Equality operator for PDFNumber.

        A PDFNumber is:

          - equal to any other PDFNumber with the same number
          - equal to any number (int or float) with the same value
          - different from any other PDFToken subclass

        Comparing a PDFNumber with anything else is not implemented.

        :param other: The object to compare to our current object
        :type other: any
        :return: True or False or NotImplemented
        :type: bool
        """
        if isinstance(other, PDFNumber):
            return self.value == other.value
        elif isinstance(other, int) or isinstance(other, float):
            return self.value == other
        elif isinstance(other, PDFToken):
            return False
        else:
            return NotImplemented

    def __int__(self) -> int:
        return int(self.value)

    def __float__(self) -> float:
        return float(self.value)

    def __bool__(self):
        """A PDFNumber is True if its value is not zero, False otherwise."""
        return self.value != None and float(self.value) != 0.0

    def pretty(self) -> str:
        return self._pretty("Number(%s)" % (self.value,))

    def encode(self) -> bytes:
        if type(self.value) == int:
            human = str(self.value)
        else:
            # Smart float rounding.
            if self.value != 0.0:
                for precision in range(2, 6):
                    float_rounded = round(self.value, precision)
                    if float_rounded != 0.0:
                        break

                human = str(float_rounded)
            else:
                human = "0"

        # Remove trailing .0
        if len(human) > 2 and human[-2:] == ".0":
            human = human[:-2]

        # Remove leading zero.
        if len(human) > 1 and human[0] == "0":
            human = human[1:]
        elif len(human) > 3 and human[0:3] == "-0.":
            human = "-" + human[2:]

        return human.encode('ascii')
