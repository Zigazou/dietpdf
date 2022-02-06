__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from logging import getLogger

from ..item import (
    PDFReference, PDFObjectID, PDFList, PDFDictionary, PDFXrefSubSection,
    PDFName, PDFNumber, PDFObject, PDFTrailer, PDFStartXref, PDFXref,
    PDFListOpen, PDFDictOpen, PDFCommand, PDFStream, PDFListClose, PDFDictClose,
    PDFComment,
)

_logger = getLogger("PDFProcessor")

class PDFProcessor:
    """A PDF processor

    A PDF processor is a stack machine. It recognizes some command and executes
    them, changing the stack state.
    """

    def __init__(self):
        self.stack = []
        self.objects = {}

    def _generate_reference(self):
        gen_num = int(self.stack.pop().value)
        obj_num = int(self.stack.pop().value)
        self.stack.append(PDFReference(obj_num, gen_num))

    def _generate_object_id(self):
        gen_num = int(self.stack.pop().value)
        obj_num = int(self.stack.pop().value)
        self.stack.append(PDFObjectID(obj_num, gen_num))

    def _generate_list(self):
        items = []
        while len(self.stack) > 0:
            current = self.stack.pop()

            if isinstance(current, PDFListOpen):
                items.reverse()
                self.stack.append(PDFList(items))
                return

            items.append(current)

    def _generate_dict(self):
        key_values = {}

        while len(self.stack) > 0:
            value = self.stack.pop()

            if isinstance(value, PDFDictOpen):
                self.stack.append(PDFDictionary(key_values))
                return

            key = self.stack.pop()
            key_values[key] = value

    def _generate_object(self):
        stream = self.stack.pop()

        if isinstance(stream, PDFStream):
            value = self.stack.pop()
        else:
            value = stream
            stream = None

        object_id = self.stack.pop()
        object = PDFObject(object_id.obj_num, object_id.gen_num, value, stream)
        self.objects[object.obj_num] = object
        self.stack.append(object)

    def _find_command(self, command: bytes, start: int) -> int:
        offset = start
        while offset < len(self.stack):
            item = self.stack[offset]
            if isinstance(item, PDFCommand) and item.command == command:
                return offset

            offset += 1

        return -1

    def _find_by_type(self, item_type: str, start: int) -> int:
        offset = start
        while offset < len(self.stack):
            if self.stack[offset].__class__.__name__ == item_type:
                return offset

            offset += 1

        return -1

    def _convert_startxref(self):
        offset = self._find_command(b"startxref", 0)
        while offset != -1:
            self.stack.pop(offset)
            self.stack.insert(
                offset,
                PDFStartXref(self.stack.pop(offset).value)
            )

            # Next startxref
            offset = self._find_command(b"startxref", offset + 1)

    def _convert_xref(self):
        offset = self._find_command(b"xref", 0)
        while offset != -1:
            self.stack.pop(offset)

            xref = PDFXref()

            while isinstance(self.stack[offset], PDFNumber):
                base = self.stack.pop(offset).value
                count = self.stack.pop(offset).value
                subsection = PDFXrefSubSection(base, count)

                for _ in range(count):
                    ref_offset = self.stack.pop(offset).value
                    ref_new = self.stack.pop(offset).value
                    ref_type = self.stack.pop(offset).command.decode('ascii')

                    subsection.entries.append((ref_offset, ref_new, ref_type))

                xref.subsections.append(subsection)

            self.stack.insert(offset, xref)

            # Next xref table
            offset = self._find_command(b"xref", offset + 1)

    def _convert_trailer(self):
        offset = self._find_command(b"trailer", 0)
        while offset != -1:
            self.stack.pop(offset)
            self.stack.insert(offset, PDFTrailer(self.stack.pop(offset)))

            # Next trailer
            offset = self._find_command(b"trailer", offset + 1)

    def end_parsing(self):
        self._convert_startxref()
        self._convert_xref()
        self._convert_trailer()

    def push(self, item):
        """Push an object onto the stack"""
        if isinstance(item, PDFCommand) and item.command == b"R":
            self._generate_reference()
        elif isinstance(item, PDFCommand) and item.command == b"obj":
            self._generate_object_id()
        elif isinstance(item, PDFCommand) and item.command == b"endobj":
            self._generate_object()
        elif isinstance(item, PDFListClose):
            self._generate_list()
        elif isinstance(item, PDFDictClose):
            self._generate_dict()
        elif isinstance(item, PDFComment):
            # Discard unneeded comments
            if item.content[:5] == b"%PDF-" or item.content[:5] == b"%%EOF":
                self.stack.append(item)
        else:
            self.stack.append(item)

    def update_xref(self, original: bytes):
        # Force calculation of actual offset for every item in the stack
        pdf = self.encode()

        # Changing offsets in an XREF table won't change its size
        offset = self._find_by_type("PDFXref", 0)
        xref = None
        while offset != -1:
            xref = self.stack[offset]

            for subsection in xref.subsections:
                base = subsection.base
                count = subsection.count
                for index in range(count):
                    (ref_offset, ref_new, ref_type) = subsection.entries[index]
                    try:
                        object = self.objects[base + index]
                    except:
                        object = None

                    subsection.entries[index] = (
                        object.item_offset if ref_type == "n" else ref_offset,
                        ref_new,
                        ref_type
                    )

            # Next XREF table
            offset = self._find_by_type("PDFXref", offset + 1)

        # Update last startxref item
        offset = self._find_by_type("PDFXref", 0)
        if offset != -1:
            self.stack[-2].offset = self.stack[offset].item_offset

        # Update the first object if it contains linearization information
        if isinstance(self.stack[1].value, PDFDictionary):
            items = self.stack[1].value.items
            if b"Linearized" in items:
                # Update file length
                items[PDFName(b"L")] = PDFNumber(str(len(pdf)).encode('ascii'))

                # Update offset of end of first page
                old_end = items[PDFName(b"E")].value
                object_id = int(original[old_end:old_end + 10].split()[0])
                items[PDFName(b"E")] = PDFNumber(
                    str(self.objects[object_id].item_offset).encode('ascii')
                )

                # Update offset of first entry in main xref table
                if xref != None:
                    items[PDFName(b"T")] = PDFNumber(
                        str(xref.item_offset +
                            xref.first_entry_offset).encode('ascii')
                    )

        # Update first trailer
        offset = self._find_by_type("PDFTrailer", 0)
        if offset != -1:
            if xref != None:
                self.stack[offset].dictionary.items[PDFName(b"Prev")] = (
                    PDFNumber(str(xref.item_offset).encode('ascii'))
                )

    def encode(self) -> bytes:
        """Encode a PDF from the current state of the processor"""

        output = b""
        offset = 0

        for item in self.stack:
            item.item_offset = offset
            item_encoded = item.encode()
            offset += len(item_encoded)
            output += item_encoded

        return output

    def pretty_print(self):
        """Pretty print the stack of the processor"""
        _logger.debug("Stack state:")
        for item in self.stack:
            _logger.debug("- %s" % (item.pretty(),))
