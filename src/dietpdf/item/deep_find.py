__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from . import PDFItem, PDFDictionary, PDFList, PDFObject


def deep_find(item: PDFItem, select: callable) -> list:
    """Find an item in an item matching a predicate.

    The predicate should have the following signature:

        predicate(path: list, item: PDFItem) -> bool

    Where:

        - path is the path leading to the item to filter
        - item is the PDFItem to filter
        - the predicate must return True if the item meets the criteria

    :param item: The starting point
    :type item: PDFItem or any subclass
    :param select: The predicate
    :type select: function
    :return: a list of tuples (path, item) of items satisfying the predicate
    :rtype: list
    :raise TypeError: If the predicate is not a function
    """

    def _deep_find(path: list, start: PDFItem) -> list:
        found = []
        if select(path, start):
            found += [(path, start)]

        if type(start) == PDFObject:
            found += _deep_find(path, start.value)
        elif type(start) == PDFDictionary:
            for key in start:
                items = _deep_find(path + [str(key)], start[key])
                if items:
                    found += items
        elif type(start) == PDFList:
            for index in range(len(start)):
                items = _deep_find(path + [index], start[index])
                if items:
                    found += items

        return found

    assert isinstance(item, PDFItem)

    if not callable(select):
        raise TypeError("select must be a function which returns a boolean")

    return _deep_find([], item)
