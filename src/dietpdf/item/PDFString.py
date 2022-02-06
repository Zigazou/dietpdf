__author__ = "Frédéric BISSON"
__copyright__ = "Copyright 2022, Frédéric BISSON"
__credits__ = ["Frédéric BISSON"]
__license__ = "mit"
__maintainer__ = "Frédéric BISSON"
__email__ = "zigazou@protonmail.com"

from .PDFItem import PDFItem

OCTAL_DIGITS = b"01234567"
ESCAPE_CHARS = {
    0x6e: 0x0a, # \n
    0x72: 0x0d, # \r
    0x74: 0x09, # \t
    0x62: 0x08, # \b
    0x66: 0x0c, # \f
    0x28: 0x28, # \(
    0x29: 0x29, # \)
    0x5c: 0x5c, # \\
}
LF = 0x0a
CR = 0x0d
ESCAPE = ord(b"\\")

STATE_INIT = 0
STATE_ESCAPE = 1
STATE_OCTAL_1 = 2
STATE_OCTAL_2 = 3
STATE_ESCAPE_CR = 4
def unescape(string: bytes) -> bytes:
    unescaped = b""
    state = STATE_INIT
    ordinal = 0

    for char in string:
        if state == STATE_INIT:
            if char == ESCAPE:
                state = STATE_ESCAPE
            else:
                unescaped += b"%c" % char
        elif state == STATE_ESCAPE:
            if char in OCTAL_DIGITS:
                ordinal = char - 0x30
                state = STATE_OCTAL_1
            elif char in ESCAPE_CHARS:
                unescaped += b"%c" % ESCAPE_CHARS[char]
                state = STATE_INIT
            elif char == LF:
                state = STATE_INIT
            elif char == CR:
                state = STATE_ESCAPE_CR
            else:
                unescaped += b"%c" % char
                state = STATE_INIT
        elif state == STATE_OCTAL_1:
            if char in OCTAL_DIGITS:
                ordinal = ordinal * 8 + char - 0x30
                state = STATE_OCTAL_2
            else:
                unescaped += b"%c" % ordinal
                if char == ESCAPE:
                    state = STATE_ESCAPE
                else:
                    unescaped += b"%c" % char
                    state = STATE_INIT
        elif state == STATE_OCTAL_2:
            if char in OCTAL_DIGITS:
                ordinal = ordinal * 8 + char - 0x30
                unescaped += b"%c" % ordinal
                state = STATE_INIT
            else:
                unescaped += b"%c" % ordinal
                if char == ESCAPE:
                    state = STATE_ESCAPE
                else:
                    unescaped += b"%c" % char
                    state = STATE_INIT
        elif state == STATE_ESCAPE_CR:
            if char != 0x0a:
                unescaped += b"%c" % char

            state = STATE_INIT

    if state == STATE_OCTAL_1 or state == STATE_OCTAL_2:
        unescaped += b"%c" % ordinal

    return unescaped


class PDFString(PDFItem):
    """A PDF string (between ( and ) )"""

    def __init__(self, string: bytes):
        self.string = string

    def __bool__(self):
        return self.string != None and len(self.string) > 0

    def __eq__(self, other):
        if isinstance(other, PDFString):
            return self.string == other.string
        elif isinstance(other, bytes):
            return self.string == other
        elif isinstance(other, PDFItem):
            return False
        else:
            return NotImplemented

    def pretty(self) -> str:
        return self._pretty("String(%s)" % (self.string,))

    def encode(self) -> bytes:
        return b"(%s)" % (self.string,)

    def to_string(self) -> str:
        unescaped = unescape(self.string)

        if len(unescaped) >= 3 and unescaped[0:3] == b"\xEF\xBB\xBF":
            return unescaped[3:].decode("utf-8")
        elif len(unescaped) >= 2 and unescaped[0:2] == b"\xFE\xFF":
            return unescaped[2:].decode("utf-16-be")
        elif len(unescaped) >= 2 and unescaped[0:2] == b"\xFF\xFE":
            return unescaped[2:].decode("utf-16-le")
        else:
            return unescaped.decode("iso-8859-1")