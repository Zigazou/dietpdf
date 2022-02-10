__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from dietpdf.token import TokenStack
from dietpdf.item import (
    PDFReference, PDFList, PDFDictionary, PDFObject, PDFItem
)


class PDF(TokenStack):
    """A PDF document

    A PDF document which can be read or written.
    """

    def __init__(self):
        super().__init__()
        self.objects = {}

    def insert(self, index: int, item: PDFItem):
        """Insert a PDFItem at specified index.

        Any number of PDFItem may be pushed.

        :param item: The item to insert
        :type item: PDFItem or any subclass of PDFItem
        :param index: The index where to insert the item
        :type index: int
        :raise TypeError: If `item` is not a PDFItem or any subclass of PDFItem
        """
        super().insert(index, item)

        if type(item) == PDFObject:
            self.objects[item.obj_num] = item

    def push(self, item: PDFItem):
        """Push a PDFItem.

        Any number of PDFItem may be pushed but PDFObject may only be pushed
        once.

        :param item:
        :type item: PDFItem or any subclass of PDFItem
        :raise TypeError: If `item` is not a PDFItem or any subclass of PDFItem
        """
        super().push(item)

        if type(item) == PDFObject:
            self.objects[item.obj_num] = item

    def pop(self, index=-1) -> PDFItem:
        """Pop the last pushed item.

        :param index: The index of the item to pop, the last one if None
        :type index: int
        :return: The last pushed item
        :rtype: PDFItem or any subclass of PDFItem
        :raise IndexError: If there is no more PDFItem to pop
        """
        item = super().pop(index)

        # Remove the item from the objects
        if isinstance(item, PDFObject) and item.obj_num in self.objects:
            del(self.objects[item.obj_num])

        return item

    def get(self, obj_num: int, path=[]) -> PDFItem:
        """Given an object given a starting object number and a path.

        If any part of the path does not point to a valid PDFItem, it returns
        None.

        The part of the path may be either:

          - an `int` which represents an index in a `PDFList`
          - an `str` or `PDFName` which a key in a `PDFDictionary`

        Any value which would be a `PDFReference` will automatically be
        transformed into the object pointed at.

        :param obj_num: The object number.
        :type obj_num: int or PDFReference or PDFObject or anything convertible
            to int
        :param path: A path described by a sequence of subpath.
        :type path: list
        :return: The specified object (subclass of PDFItem) or None if the path
            is not valid.
        :rtype: PDFItem or any subclass of PDFItem or None

        """
        assert type(path) == list

        # Normalize the object number.
        if type(obj_num) in [PDFObject, PDFReference]:
            obj_num = obj_num.obj_num
        else:
            obj_num = int(obj_num)

        # Check if the object is known.
        if obj_num not in self.objects:
            return None

        object = self.objects[obj_num]

        # No more path to follow, this is the final destination.
        if not path:
            return object

        # Consume as many path elements as possible inside the same object.
        value = object.value
        while path and value:
            if type(value) == PDFDictionary:
                value = value[path[0]] if path[0] in value else None
            elif type(value) == PDFList:
                value = value[path[0]] if path[0] in range(len(value)) else None
            elif type(value) == PDFReference:
                break

            path.pop(0)

        if type(value) == PDFReference:
            return self.get(value, path)
        elif path:
            return None
        else:
            return value
