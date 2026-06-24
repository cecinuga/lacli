import csv
from concurrent.futures import ThreadPoolExecutor
import os
import sys
from lacli.core.reconstruction import reconstruct
from lacli.core.file import read_chunk

print(sys.version)                      # must contain "free-threaded build"

def run(fd: int, n_thread: int):
    size = os.stat(fd).st_size
    chunk_size = size // n_thread

    #print(f"num thread: {n_thread}")
    #print(f"size: {size}, chunk size: {chunk_size}\n")

    try:
        with ThreadPoolExecutor(max_workers=n_thread+1) as pool:
            chunks_metas = list(pool.map(lambda i: read_chunk(fd, i, chunk_size), range(n_thread+1)))
    except:
        raise Exception("error reading chunks threads")

    matrix = reconstruct(chunks_metas, n_thread)
    #print(matrix.data)
    print(f"col count: {matrix.cols}, row count: {matrix.rows}, total nums: {matrix.nums}")

    return matrix

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
        raise ValueError('n_thread setted to None')

    fd = os.open(file, os.O_RDONLY)
    run(fd, n_thread)
    os.close(fd)
