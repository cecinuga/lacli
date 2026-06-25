"""Byte-level numeric tokenizer used by load.file.read_chunk."""

class Lexer:
    """
    Streaming byte-level tokenizer that emits strings from raw bytes.

    Accumulates characters into a buffer and flushes the accumulated token when a
    non-numeric delimiter is encountered. Accepts an optional leading sign and at
    most one decimal point; the digit-only validation that would reject a bare
    sign (e.g. '+') is currently disabled (see `_flush`).
    """
    DIGITS = set("0123456789")
    SIGNS  = set("+-")
    DOT    = "."

    def __init__(self):
        self._buf = []
        self._has_dot = False

    def feed(self, x: int) -> str | None:
        """Feed one byte value; return a complete token string when a delimiter is hit, else None."""
        c = chr(x)
        if c in self.DIGITS:
            self._buf.append(c)
            return None
        if c in self.SIGNS and not self._buf:
            # accept sign only at the start of a number
            self._buf.append(c)
            return None
        if c == self.DOT and not self._has_dot:
            # accept the first decimal point inside a number
            self._buf.append(c)
            self._has_dot = True
            return None
        return self._flush()

    def flush(self) -> str | None:
        """Emit any token still in the buffer; call at end-of-stream to capture the last number."""
        return self._flush()

    def _flush(self) -> str | None:
        """
        Drain the buffer and return the accumulated string, or None if the buffer is empty.

        NOTE: the digit-only check below is disabled, so a buffer with no digits
        (e.g. a bare '+' or '-') is currently returned as-is rather than rejected.
        """
        if not self._buf:
            return None
        s = "".join(self._buf)
        self._buf.clear()
        self._has_dot = False
        #if not any((ch.isdigit() or ch in self.SIGNS) for ch in s):
        #    return None
        return s
