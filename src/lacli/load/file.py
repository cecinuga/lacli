"""Reads and lexes a single byte-range chunk of the input file into a ChunkMetadata."""
import os
from concurrent.futures import ThreadPoolExecutor
from lacli.models.lexer import Lexer
from lacli.models.matrix import ChunkMetadata, Matrix
from lacli.load.recon import reconstruct
from lacli.benchmark.timer import timer

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

def read_file(fd: int, n_thread: int) -> list[ChunkMetadata]:
    size = os.stat(fd).st_size
    chunk_size = size // n_thread
    chunk_rest = size%n_thread
    chunks_meta = []
    with ThreadPoolExecutor(max_workers=n_thread) as pool:
        chunks_meta.extend(list(pool.map(lambda i: read_chunk(fd, i*chunk_size, chunk_size), range(n_thread))))
    if chunk_rest > 0:
        chunks_meta.append(read_chunk(fd, chunk_size*n_thread, chunk_rest))

    return chunks_meta

def load(fd: int, n_thread: int) -> Matrix:
    """
    Load and parse the file at `fd` into a Matrix using `n_thread` worker threads.

    Splits the file into `n_thread+1` byte-sized chunks, parses each chunk
    concurrently with `read_chunk`, and merges the results via `reconstruct`.

    Input: `fd` open file descriptor (read-only), `n_thread` number of worker threads.
    Output: the reconstructed `Matrix`.
    """
    #print(f"num thread: {n_thread}")
    #print(f"size: {size}, chunk size: {chunk_size}, chunk rest: {chunk_rest}\n")

    try:
        chunks = read_file(fd, n_thread)
    except:
        raise Exception("error reading chunks threads")

    matrix = reconstruct(chunks, n_thread)

    #print(matrix.data)
    #print(f"col count: {matrix.cols}, row count: {matrix.rows}, total nums: {matrix.nums}")

    return matrix
