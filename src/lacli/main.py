from concurrent.futures import ThreadPoolExecutor
import os
import sys
from core.reconstruction import reconstruct
from core.file import read_chunk

print(sys.version)                      # must contain "free-threaded build"

"""
Every line is intended to be an array of the matrix.
To load the matrix, as many threads as there are CPU cores are spawned, the file is chunked and each thread loads a chunk of the matrix.
"""
if __name__ == '__main__':
    file = sys.argv[1] # file path
    n_thread = os.cpu_count()
    if len(sys.argv) == 3:
        n_thread = int(sys.argv[2])

    if n_thread == None:
        raise ValueError('os.cpu_count() return None')

    fd = os.open(file, os.O_RDONLY)
    size = os.stat(file).st_size
    chunk_size = size // n_thread
    chunk_rest = size % n_thread

    print(f"num thread: {n_thread}")
    print(f"size: {size}, chunk size: {chunk_size}, chunk rest: {chunk_rest}\n")

    try:
        with ThreadPoolExecutor(max_workers=n_thread+1) as pool:
            chunks_metas = list(pool.map(lambda i: read_chunk(fd, i, chunk_size), range(n_thread+1)))
    finally:
        os.close(fd)

    matrix = reconstruct(chunks_metas, n_thread)

    print(matrix.data)
    print(f"col count: {matrix.cols}, row count: {matrix.rows}, total nums: {matrix.nums}")
