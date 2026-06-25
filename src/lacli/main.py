"""
CLI entry point: loads a numeric CSV-like file into a Matrix using parallel threads.

Every line is intended to be an array of the matrix. To load the matrix, the file is
split into byte chunks (one per thread plus a remainder), each chunk is lexed
concurrently, and the resulting per-chunk token lists are stitched back into a Matrix.
"""
from concurrent.futures import ThreadPoolExecutor
import os
import sys
from lacli.load.recon import reconstruct
from lacli.load.file import read_chunk

print(sys.version)                      # must contain "free-threaded build"

def run(fd: int, n_thread: int):
    """
    Load and parse the file at `fd` into a Matrix using `n_thread` worker threads.

    Splits the file into `n_thread+1` byte-sized chunks, parses each chunk
    concurrently with `read_chunk`, and merges the results via `reconstruct`.

    Input: `fd` open file descriptor (read-only), `n_thread` number of worker threads.
    Output: the reconstructed `Matrix`.
    """
    size = os.stat(fd).st_size
    chunk_size = size // n_thread
    chunk_rest = size%n_thread

    #print(f"num thread: {n_thread}")
    #print(f"size: {size}, chunk size: {chunk_size}, chunk rest: {chunk_rest}\n")

    chunks_meta = []
    try:
        with ThreadPoolExecutor(max_workers=n_thread) as pool:
            chunks_meta.extend(list(pool.map(lambda i: read_chunk(fd, i*chunk_size, chunk_size), range(n_thread))))
        if chunk_rest > 0:
            chunks_meta.append(read_chunk(fd, chunk_size*n_thread, chunk_rest))
    except:
        raise Exception("error reading chunks threads")

    matrix = reconstruct(chunks_meta, n_thread)

    print(matrix.data)
    print(f"col count: {matrix.cols}, row count: {matrix.rows}, total nums: {matrix.nums}")

    return matrix

if __name__ == '__main__':
    file = sys.argv[1] # file path
    n_thread = os.cpu_count()
    if len(sys.argv) == 3:
        n_thread = int(sys.argv[2])

    if n_thread == None:
        raise ValueError('n_thread setted to None')

    fd = os.open(file, os.O_RDONLY)
    run(fd, n_thread)
    os.close(fd)
