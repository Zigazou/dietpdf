__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from .PDFToken import PDFToken


class TokenStack:
    """A token stack

    A token stack which can be read or written.
    """

    def __init__(self):
        self.stack = []

    def insert(self, index: int, item: PDFToken):
        """Insert a PDFToken at specified index.

        :param item: The item to insert
        :type item: PDFToken or any subclass of PDFToken
        :param index: The index where to insert the item
        :type index: int
        :raise TypeError: If `item` is not a PDFToken or any subclass of PDFToken
        """
        if not isinstance(item, PDFToken):
            raise TypeError("expected PDFToken or any subclass")

        self.stack.insert(index, item)

    def push(self, item: PDFToken):
        """Push a PDFToken.

        Any number of PDFToken may be pushed but PDFObject may only be pushed
        once.

        :param item:
        :type item: PDFToken or any subclass of PDFToken
        :raise TypeError: If `item` is not a PDFToken or any subclass of PDFToken
        """
        if not isinstance(item, PDFToken):
            raise TypeError("expected PDFToken or any subclass")

        self.stack.append(item)

    def pop(self, index=-1) -> PDFToken:
        """Pop the last pushed item.

        :param index: The index of the item to pop, the last one if None
        :type index: int
        :return: The last pushed item
        :rtype: PDFToken or any subclass of PDFToken
        :raise IndexError: If there is no more PDFToken to pop
        """
        try:
            item = self.stack.pop(index)
        except IndexError:
            raise IndexError("pop from empty PDF")

        return item

    def stack_size(self) -> int:
        """Returns the stack size of the PDF

        :return: Stack size of the PDF
        :rtype: int
        """
        return len(self.stack)

    def stack_at(self, index: int) -> PDFToken:
        """Get the element on the stack at the specified index.

        :param index: The index
        :type index: int
        """
        return self.stack[index]

    def find(self, select: callable, start: int = 0):
        """Find an item in the stack according to a predicate.

        The predicate should have the following signature:

            predicate(index: int, item: PDFToken) -> bool

        Where:

          - index is the index of the item in the stack, not its object number
          - item is a PDFToken or any subclass
          - the predicate must return True if the item meets the criteria

        :param select: The predicate
        :type select: function
        :param start: the starting index
        :type start: int
        :raise TypeError: If the predicate is not a function
        """
        if not callable(select):
            raise TypeError("select must be a function which returns a boolean")

        index = start
        while index < len(self.stack):
            item = self.stack[index]

            if select(index, item):
                yield (index, item)

            index += 1

    def find_all(self, select: callable, start: int = 0) -> list:
        """Find an item in the stack according to a predicate.

        See the `find` method for information about the predicate.

        :param select: The predicate
        :type select: function
        :param start: the starting index
        :type start: int
        :raise TypeError: If the predicate is not a function
        :return: A list of PDFToken satisfying the predicate
        :rtype: list
        """

        return [item for _, item in self.find(select, start)]

    def find_first(self, select: callable, start: int = 0) -> PDFToken:
        """Find an item in the stack according to a predicate.

        See the `find` method for information about the predicate.

        :param select: The predicate
        :type select: function
        :param start: the starting index
        :type start: int
        :raise TypeError: If the predicate is not a function
        :return: The first item satisfying the predicate
        :rtype: PDFToken or None
        """
        for index, item in self.find(select, start):
            return item

        return None
