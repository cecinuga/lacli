from concurrent.futures import ThreadPoolExecutor
import os
import sys

print(sys.version)              # must contain "free-threaded build"
print(f"is gil enabled: {sys._is_gil_enabled()}\n")

class ResultInfo:
    def __init__(self):
        self.col_count = 0
        self.row_count = 0
        self.new_lines_pos = []
        self.data = []

class NumberLexer:
    DIGITS = set("0123456789")
    SIGNS  = set("+-")
    DOT    = "."

    def __init__(self):
        self._buf = []
        self._has_dot = False

    def feed(self, x: int) -> str | None:
        c = chr(x)
        if c in self.DIGITS:
            self._buf.append(c)
            return None
        if c in self.SIGNS and not self._buf:
            self._buf.append(c)
            return None
        if c == self.DOT and self._buf and not self._has_dot:
            self._buf.append(c)
            self._has_dot = True
            return None
        return self._flush()

    def flush(self) -> str | None:
        return self._flush()

    def _flush(self) -> str | None:
        if not self._buf:
            return None
        s = "".join(self._buf)
        self._buf.clear()
        self._has_dot = False
        if not any(ch.isdigit() for ch in s):
            return None
        return s

def read_chunks(fd, index, size) -> ResultInfo:
    offset = index*size
    #print(f"thread number: {index} --- size {size} at offset {offset}")
    raw = os.pread(fd, size, offset)

    info = ResultInfo()
    lexer = NumberLexer()
    for c in raw:
        if c == 10: # new line
            info.row_count += 1
            info.new_lines_pos.append(len(info.data))
        if c == 44: # comma
            info.col_count += 1

        number = lexer.feed(c)
        if number:
            info.data.append(number)

    last = lexer.flush()
    if last:
        info.data.append(last)
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

    merged_results = ResultInfo()
    try:
        with ThreadPoolExecutor(max_workers=n_thread+1) as pool:
            results = list(pool.map(lambda i: read_chunks(fd, i, chunk_size), range(n_thread)))

        results.append(read_chunks(fd, n_thread, chunk_size))
    finally:
        os.close(fd)

    for res in results:
        merged_results.data.append(res.data)
        merged_results.row_count += res.row_count
        print(res.new_lines_pos)


    print(f"col count: {merged_results.col_count}, row count: {merged_results.row_count}")
    print(merged_results.data)
