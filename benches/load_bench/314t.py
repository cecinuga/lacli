import os
import sys

print(sys.version)              # deve contenere "free-threaded build"
print(sys._is_gil_enabled())

"""
Every line is intended to be an array of the matrix.
To load the matrix, as many threads as there are CPU cores are spawned, the file is chunked and each thread loads a chunk of the matrix.
"""
if __name__ == '__main__':
    file = sys.argv[1]
    n_thread = os.cpu_count()
    if n_thread == None:
        raise ValueError('os.cpu_count() return None')

    fd = os.open(file, os.O_RDONLY)
    size = os.stat(file).st_size
    chunk_size = size // n_thread
    chunk_rest = size % n_thread
