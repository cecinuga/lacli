"""Reads and lexes a single byte-range chunk of the input file into a ChunkMetadata."""
import sys
import os
from concurrent.futures import ThreadPoolExecutor
from lacli.benchmark.bench import bench
from lacli.loader.lex import lex

def read_raw(fd: int, thread: int) -> list[bytes]:
    """Split `fd` into fixed-size byte chunks, lexing them concurrently across `thread` workers."""
    size = os.stat(fd).st_size

    if thread == 1 or sys._is_gil_enabled():
        return [os.pread(fd, size, 0)]

    chunk_size = size//thread
    offsets = range(0, size, chunk_size)
    print(offsets, chunk_size)

    with ThreadPoolExecutor(max_workers=thread) as pool:
        return list(pool.map(
            lambda off: os.pread(fd, min(chunk_size, size - off), off),
            offsets,
    ))

def load(fd: int, thread: int):
    """Load and parse the file at `fd` into a Matrix, splitting it into `thread` byte chunks processed concurrently."""
    #print(f"num thread: {thread}")
    #print(f"size: {size}, chunk size: {chunk_size}, chunk rest: {chunk_rest}\n")

    try:
        chunks = bench("load_read_raw", read_raw, fd, thread)
    except Exception as e:
        raise RuntimeError("error reading chunks threads", e) from e

    print(chunks)
    matrix = bench("load_lex", lex, chunks)

    #print(matrix.data)
    #print(f"col count: {matrix.cols}, row count: {matrix.rows}, total nums: {matrix.nums}")

    return matrix
