from concurrent.futures import ThreadPoolExecutor
import os
import sys

print(sys.version)              # must contain "free-threaded build"
print(f"is gil enabled: {sys._is_gil_enabled()}\n")

class ResultInfo:
    def __init__(self):
        self.row = 0
        self.data = []

def read_chunks(fd, index, size) -> ResultInfo:
    offset = index*size
    #print(f"thread number: {index} --- size {size} at offset {offset}")
    raw = os.pread(fd, size, offset)

    info = ResultInfo() # parse numbers and newline, newline is counted to determine row count
    def parse(raw):
        return

    print(raw)
    return info


"""
Every line is intended to be an array of the matrix.
To load the matrix, as many threads as there are CPU cores are spawned, the file is chunked and each thread loads a chunk of the matrix.
"""
if __name__ == '__main__':
    file = sys.argv[1] # file path

    n_thread = os.cpu_count()
    if n_thread == None:
        raise ValueError('os.cpu_count() return None')

    fd = os.open(file, os.O_RDONLY)
    size = os.stat(file).st_size
    chunk_size = size // n_thread
    chunk_rest = size % n_thread

    print(f"num thread: {n_thread}")
    print(f"size: {size}, chunk size: {chunk_size}, chunk rest: {chunk_rest}\n")

    try:
        with ThreadPoolExecutor(max_workers=n_thread) as pool:
            results = list(pool.map(lambda i: read_chunks(fd, i, chunk_size), range(n_thread)))
    finally:
        os.close(fd)

    print(results)
