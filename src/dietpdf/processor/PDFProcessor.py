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

from ..pdf import PDF

_logger = getLogger("PDFProcessor")

class PDFProcessor:
    """A PDF processor

    A PDF processor is a stack machine. It recognizes some command and executes
    them, changing the stack state.
    """

    def __init__(self):
        self.pdf = PDF()

    def _generate_reference(self):
        gen_num = int(self.pdf.pop().value)
        obj_num = int(self.pdf.pop().value)
        self.pdf.push(PDFReference(obj_num, gen_num))

    def _generate_object_id(self):
        gen_num = int(self.pdf.pop().value)
        obj_num = int(self.pdf.pop().value)
        self.pdf.push(PDFObjectID(obj_num, gen_num))

    def _generate_list(self):
        items = []
        while self.pdf.stack_size() > 0:
            current = self.pdf.pop()

            if isinstance(current, PDFListOpen):
                items.reverse()
                self.pdf.push(PDFList(items))
                return

            items.append(current)

    def _generate_dict(self):
        key_values = {}

        while self.pdf.stack_size() > 0:
            value = self.pdf.pop()

            if isinstance(value, PDFDictOpen):
                self.pdf.push(PDFDictionary(key_values))
                return

            key = self.pdf.pop()
            key_values[key] = value

    def _generate_object(self):
        stream = self.pdf.pop()

        if isinstance(stream, PDFStream):
            value = self.pdf.pop()
        else:
            value = stream
            stream = None

        object_id = self.pdf.pop()
        object = PDFObject(object_id.obj_num, object_id.gen_num, value, stream)
        self.pdf.push(object)

    def _find_command(self, command: bytes, start: int) -> int:
        offset = start
        while offset < self.pdf.stack_size():
            item = self.pdf.stack[offset]
            if isinstance(item, PDFCommand) and item.command == command:
                return offset

            offset += 1

        return -1

    def _convert_startxref(self):
        any_startxref_command = lambda _, item: (
            type(item) == PDFCommand and
            item.command == b"startxref"
        )

        for offset, startxref in self.pdf.find(any_startxref_command):
            self.pdf.pop(offset)
            self.pdf.insert(
                offset,
                PDFStartXref(self.stack.pop(offset).value)
            )

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
        any_xref_table = lambda _, item: type(item) == PDFXref
        xrefs = self.pdf.find_all(any_xref_table)

        any_startxref = lambda _, item: type(item) == PDFStartXref
        startxrefs = self.pdf.find_all(any_startxref)

        for xref in xrefs:
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

        # Update last startxref item
        if xrefs and startxrefs:
            startxrefs[-1].offset = xrefs[0].item_offset

        # Update the first object if it contains linearization information
        any_linearized = lambda _, item: (
            type(item) == PDFObject and
            type(item.value) == PDFDictionary and
            b"Linearized" in item.value
        )

        linearized = self.pdf.find_first(any_linearized)
        if linearized:
            items = linearized.value

            # Update file length
            linearized.value[b"L"] = PDFNumber(str(len(pdf)).encode('ascii'))

            # Update offset of end of first page
            old_end = int(linearized.value[b"E"])
            object_id = int(original[old_end:old_end + 10].split()[0])

            linearized.value[b"E"] = PDFNumber(
                str(self.pdf.get(object_id).item_offset).encode('ascii')
            )

            # Update offset of first entry in main xref table
            if xrefs:
                linearized.value[b"T"] = PDFNumber(
                    str(xrefs[0].item_offset +
                        xrefs[0].first_entry_offset).encode('ascii')
                )

        # Update first trailer
        any_trailer = lambda _, item: type(item) == PDFTrailer
        trailer = self.pdf.find_first(any_trailer)
        if trailer and xrefs:
            trailer.dictionary[b"Prev"] = (
                PDFNumber(str(xrefs[0].item_offset).encode('ascii'))
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
