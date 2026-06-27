"""Reads and lexes a single byte-range chunk of the input file into a ChunkMetadata."""
import sys
import os
from concurrent.futures import ThreadPoolExecutor
from lacli.benchmark.timer import timer
from lacli.loader.chunk import ChunkMetadata
from lacli.loader.lexer import Lexer
from lacli.models.matrix import Matrix
from lacli.loader.merge import merge

def read_chunk(fd, offset, size) -> ChunkMetadata:
    """
    Read `size` bytes at `offset` from `fd` using pread (thread-safe, no seek).
    Lex all numeric tokens in the slice and record newline count and boundary conditions.
    """
    NEWLINE = 10
    COMMA = 44
    raw = os.pread(fd, size, offset)
    info = ChunkMetadata()
    lexer = Lexer()

    if raw and (raw[0] == NEWLINE or raw[0] == COMMA):
        info.is_first_stop = True
    for c in raw:
        if c == NEWLINE:
            info.newline_num += 1

        number = lexer.feed(c)
        if number:
            info.data.append(number)

    last = lexer.flush()
    if last:
        info.data.append(last)
        info.is_last_truncated = True  # token was cut at the chunk boundary; must be joined with next chunk

    return info

def read_file(fd: int, thread: int) -> list[ChunkMetadata]:
    """Split `fd` into fixed-size byte chunks, lexing them concurrently across `thread` workers."""
    with timer(label="load_read_file"):
        size = os.stat(fd).st_size

        if thread == 1 or sys._is_gil_enabled():
            return [read_chunk(fd, 0, size)]

        chunk_size = size//thread
        offsets = range(0, size, chunk_size)

        with ThreadPoolExecutor(max_workers=thread) as pool:
            return list(pool.map(
                lambda off: read_chunk(fd, off, min(chunk_size, size - off)),
                offsets,
        ))

def load(fd: int, thread: int) -> Matrix:
    """Load and parse the file at `fd` into a Matrix, splitting it into `thread` byte chunks processed concurrently."""
    #print(f"num thread: {thread}")
    #print(f"size: {size}, chunk size: {chunk_size}, chunk rest: {chunk_rest}\n")
    with timer(label="load"):
        try:
            chunks = read_file(fd, thread)
        except Exception as e:
            raise RuntimeError("error reading chunks threads", e) from e

        matrix = merge(chunks, thread)

    #print(matrix.data)
    #print(f"col count: {matrix.cols}, row count: {matrix.rows}, total nums: {matrix.nums}")

    return matrix
