__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

import logging

from dietpdf.item import PDFReference, PDFDictionary

_logger = logging.getLogger("content_objects")


def content_objects(objects: dict) -> set:
    """Get the set of objects which are content objects

    A content object is an object which is referenced by a `/Contents` key in
    another object.

    :param dict objects: A dictionary of PDFObject, keyed by the object ID
    :return: A set of object numbers (int)
    :rtpe: set
    """

    assert type(objects) == dict

    # Find all content objects.
    content_objects = set()
    for object_id in objects:
        object = objects[object_id]

        # Ignore objects with no dictionary.
        if type(object.value) != PDFDictionary:
            continue

        # Ignore objects which have no /Contents key in their dictionary.
        if b"Contents" not in object:
            continue

        contents = object[b"Contents"]

        # The /Contents key must contain a reference to another object.
        if not isinstance(contents, PDFReference):
            continue

        # Add the number of the referenced object to the set.
        content_objects.add(contents.obj_num)

    return content_objects
