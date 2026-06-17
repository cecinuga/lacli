from concurrent.futures import ThreadPoolExecutor
import os
import sys

print(sys.version)              # must contain "free-threaded build"
print(f"is gil enabled: {sys._is_gil_enabled()}\n")

class ResultInfo:
    def __init__(self):
        self.row_count = 0
        self.data = []

def parse_number_fct():
    state = ''
    empty = True
    decimal = False
    def parser(c: int) -> str | None:
        nonlocal state
        nonlocal empty
        nonlocal decimal

        match c:
            case 45 | 43: # minus or plus
                if empty:
                    state += chr(c)
                    empty = False
                    return None
                else: # state not permitted, so i return the accumulated number
                    empty = True
                    decimal = False
                    completed = state
                    state = ''
                    return completed

            case 48 | 49 | 50 | 51 | 52 | 53 | 54 | 55 | 56 | 57: # digits
                state += chr(c)
                empty = False
                return None

            case 46: # full_stop
                # state not permitted, so i return the accumulated number
                if empty or decimal:
                    empty = True
                    decimal = False
                    completed = state
                    state = ''
                    return completed

                decimal = True
                state += chr(c)
                return None

            case _:
                empty = True
                decimal = False
                completed = state
                state = ''
                return completed
    return parser

def read_chunks(fd, index, size) -> ResultInfo:
    offset = index*size
    #print(f"thread number: {index} --- size {size} at offset {offset}")
    raw = os.pread(fd, size, offset)

    info = ResultInfo() # parse numbers and newline, newline is counted to determine row count

    parse_number = parse_number_fct()

    raw = raw + b'W' # for parsing the last number
    for c in raw:
        if c == 10:
            info.row_count += 1

        number = parse_number(c)
        if number:
            info.data.append(number)


    print(info.row_count)
    print(info.data)
    print(raw)
    print('---------------------------')
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
