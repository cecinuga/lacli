import os
from models.matrix import ChunkMetadata, Matrix

def read_chunk(fd, index, size) -> ChunkMetadata:
    """
    Read `size` bytes at byte offset `index * size` from `fd` using pread (thread-safe, no seek).
    Lex all numeric tokens in the slice and record newline count and boundary conditions.
    """
    offset = index*size
    #print(f"thread number: {index} --- size {size} at offset {offset}")
    raw = os.pread(fd, size, offset)

    info = ChunkMetadata()
    lexer = NumberLexer()

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
    #print(raw)
    return info
