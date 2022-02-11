__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from logging import getLogger

from dietpdf.token import (
    PDFNumber, PDFListOpen, PDFDictOpen, PDFCommand, PDFListClose,
    PDFDictClose, PDFComment, PDFName
)

from dietpdf.item import (
    PDFReference, PDFObjectID, PDFList, PDFDictionary, PDFXrefSubSection,
    PDFObject, PDFTrailer, PDFStartXref, PDFXref, PDFStream
)

from dietpdf.pdf import PDF
from .TokenProcessor import TokenProcessor


_logger = getLogger("PDFProcessor")

class PDFProcessor(TokenProcessor):
    """A PDF processor

    A PDF processor is a stack machine. It recognizes some command and executes
    them, changing the stack state.
    """
    def __init__(self):
        self.tokens = PDF()

    def _generate_reference(self):
        gen_num = int(self.tokens.pop().value)
        obj_num = int(self.tokens.pop().value)
        self.tokens.push(PDFReference(obj_num, gen_num))

    def _generate_object_id(self):
        gen_num = int(self.tokens.pop().value)
        obj_num = int(self.tokens.pop().value)
        self.tokens.push(PDFObjectID(obj_num, gen_num))

    def _generate_list(self):
        items = []
        while self.tokens.stack_size() > 0:
            current = self.tokens.pop()

            if isinstance(current, PDFListOpen):
                items.reverse()
                self.tokens.push(PDFList(items))
                return

            items.append(current)

    def _generate_dict(self):
        key_values = {}

        while self.tokens.stack_size() > 0:
            value = self.tokens.pop()

            if isinstance(value, PDFDictOpen):
                self.tokens.push(PDFDictionary(key_values))
                return

            key = self.tokens.pop()
            key_values[key] = value

    def _generate_object(self):
        stream = self.tokens.pop()

        if isinstance(stream, PDFStream):
            value = self.tokens.pop()
        else:
            value = stream
            stream = None

        object_id = self.tokens.pop()
        object = PDFObject(object_id.obj_num, object_id.gen_num, value, stream)
        self.tokens.push(object)

    def _convert_startxref(self):
        any_startxref_command = lambda _, item: (
            type(item) == PDFCommand and
            item.command == b"startxref"
        )

        for offset, _ in self.tokens.find(any_startxref_command):
            self.tokens.pop(offset)
            self.tokens.insert(
                offset,
                PDFStartXref(self.tokens.pop(offset).value)
            )

    def _convert_xref(self):
        any_xref_command = lambda _, item: (
            type(item) == PDFCommand and
            item.command == b"xref"
        )

        for offset, _ in self.tokens.find(any_xref_command):
            self.tokens.pop(offset)

            xref = PDFXref()

            while isinstance(self.tokens.stack_at(offset), PDFNumber):
                base = self.tokens.pop(offset).value
                count = self.tokens.pop(offset).value
                subsection = PDFXrefSubSection(base, count)

                for _ in range(count):
                    ref_offset = self.tokens.pop(offset).value
                    ref_new = self.tokens.pop(offset).value
                    ref_type = self.tokens.pop(offset).command.decode('ascii')

                    subsection.entries.append((ref_offset, ref_new, ref_type))

                xref.subsections.append(subsection)

            self.tokens.insert(offset, xref)

    def _convert_trailer(self):
        any_trailer_command = lambda _, item: (
            type(item) == PDFCommand and
            item.command == b"trailer"
        )

        for offset, _ in self.tokens.find(any_trailer_command):
            self.tokens.pop(offset)
            self.tokens.insert(offset, PDFTrailer(self.tokens.pop(offset)))

    def end_parsing(self):
        """Converts remaining items on the stack.
        
        The `startxref`, `xref` and `trailer` elements of a PDF file do not
        follow a stack principle. They must therefore be recognized when all the
        parsing has been done.

        Without calling this method, the processor state is inconsistent.
        """
        self._convert_startxref()
        self._convert_xref()
        self._convert_trailer()

    def push(self, item):
        """Push an item onto the processor's stack.
        
        Pushing item on stack may result in their interpretation. For example,
        pushing `1` then `0` then `R` on the stack will make the processor
        replace them by a `PDFReference` object.

        Comments other than `%PDF-*` or `%%EOF` will be completely ignored.
        """
        if type(item) == PDFCommand and item.command == b"R":
            self._generate_reference()
        elif type(item) == PDFCommand and item.command == b"obj":
            self._generate_object_id()
        elif type(item) == PDFCommand and item.command == b"endobj":
            self._generate_object()
        elif type(item) == PDFListClose:
            self._generate_list()
        elif type(item) == PDFDictClose:
            self._generate_dict()
        elif type(item) == PDFComment:
            # Discard unneeded comments
            if item.content[:5] == b"%PDF-" or item.content[:5] == b"%%EOF":
                self.tokens.push(item)
        else:
            self.tokens.push(item)

    def encode(self) -> bytes:
        """Encode a PDF from the current state of the processor

        :return: A complete PDF file content ready to be written in a file
        :rtype: bytes
        """

        # Detect linearization
        def any_linearized(_, item):
            return (
                type(item) == PDFObject and
                type(item.value) == PDFDictionary and
                b"Linearized" in item
            )

        linearized = self.tokens.find_first(any_linearized)

        # Encode each object.
        def any_object(_, item):
            if type(item) != PDFObject:
                return False

            if type(item.value) == PDFDictionary:
                if b"Type" in item and item[b"Type"] == b"XRef":
                    return False

                if b"Type" in item and item[b"Type"] == b"ObjStm":
                    return False

                if b"Linearized" in item:
                    return False

            return True

        output = PDFComment(b"%PDF-1.7").encode()
        offset = len(output)

        # Write every object
        xref_entries = {}
        max_obj_num = 0
        for _, item in self.tokens.find(any_object):
            item.item_offset = offset
            xref_entries[item.obj_num] = (offset, 0, "n")
            max_obj_num = max(max_obj_num, item.obj_num)

            item_encoded = item.encode()
            offset += len(item_encoded)
            output += item_encoded

        # Write the XRef table
        xref_subsection = PDFXrefSubSection(0, max_obj_num + 1)
        for index in range(max_obj_num + 1):
            if index in xref_entries:
                xref_subsection.entries.append(xref_entries[index])
            else:
                xref_subsection.entries.append((0, 65535, "f"))

        xref = PDFXref()
        xref.subsections.append(xref_subsection)

        output += xref.encode()

        # Write the Trailer dictionary
        def any_trailer(_, item):
            return (
                type(item) == PDFTrailer or
                (
                    type(item) == PDFObject and
                    type(item.value) == PDFDictionary and
                    b"Type" in item and item[b"Type"] == b"XRef"
                )
            )

        trailers = list(self.tokens.find(any_trailer))

        if linearized:
            old_trailer = trailers[0][1]
        else:
            old_trailer = trailers[-1][1]

        if type(old_trailer) == PDFObject:
            trailer_dictionary = PDFDictionary({
                PDFName(b"Info"): old_trailer[b"Info"],
                PDFName(b"Root"): old_trailer[b"Root"],
                PDFName(b"Size"): PDFNumber(max_obj_num + 1),
            })
        else:
            trailer_dictionary = PDFDictionary({
                PDFName(b"Info"): old_trailer.dictionary[b"Info"],
                PDFName(b"Root"): old_trailer.dictionary[b"Root"],
                PDFName(b"Size"): PDFNumber(max_obj_num + 1),
            })

        trailer = PDFTrailer(trailer_dictionary)
        output += trailer.encode()

        # Write the startxref offset
        output += b"startxref\n%d\n" % offset

        # Write the end of file
        output += PDFComment(b"%%EOF").encode()

        return output
