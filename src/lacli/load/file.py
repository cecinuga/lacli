"""Reads and lexes a single byte-range chunk of the input file into a ChunkMetadata."""
import os
from lacli.models.lexer import Lexer
from lacli.models.matrix import ChunkMetadata, Matrix

def read_chunk(fd, offset, size) -> ChunkMetadata:
    """
    Read `size` bytes at byte offset `index * size` from `fd` using pread (thread-safe, no seek).
    Lex all numeric tokens in the slice and record newline count and boundary conditions.
    """
    raw = os.pread(fd, size, offset)
    info = ChunkMetadata()
    lexer = Lexer()

    if raw and (raw[0] == 10 or raw[0] == 44):
        info.is_first_stop = True
    for c in raw:
        if c == 10: # new line
            info.newline_num += 1

        number = lexer.feed(c)
        if number:
            info.data.append(number)

    last = lexer.flush()
    if last:
        info.data.append(last)
        info.is_last_truncated = True  # token was cut at the chunk boundary; must be joined with next chunk

    return info
