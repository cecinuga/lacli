from concurrent.futures import ThreadPoolExecutor
import os
import sys

print(sys.version)                      # must contain "free-threaded build"

class ChunkMetadata:
    """Parsed output of a single file chunk: extracted numbers and boundary flags used during merge."""
    def __init__(self):
        self.newline_num = 0
        self.is_first_stop = False   # True if the chunk starts with '\n' (no leading truncated token)
        self.is_last_truncated = False  # True if the last token was cut at the chunk boundary
        self.data: list[str] = []

class Matrix:
    def __init__(self):
        self.cols = 0
        self.rows = 0
        self.nums = 0
        self.data = []

class NumberLexer:
    """
    Streaming byte-level tokenizer that emits numeric strings (integer or float) from raw bytes.

    Accumulates characters into a buffer and flushes a complete token when a non-numeric
    delimiter is encountered. Accepts an optional leading sign, at most one decimal point,
    and rejects buffers that contain no digit (e.g. a bare '+').
    """
    DIGITS = set("0123456789")
    SIGNS  = set("+-")
    DOT    = "."

    def __init__(self):
        self._buf = []
        self._has_dot = False

    def feed(self, x: int) -> str | None:
        """Feed one byte value; return a complete token string when a delimiter is hit, else None."""
        c = chr(x)
        if c in self.DIGITS:
            self._buf.append(c)
            return None
        if c in self.SIGNS and not self._buf:
            # accept sign only at the start of a number
            self._buf.append(c)
            return None
        if c == self.DOT and self._buf and not self._has_dot:
            # accept the first decimal point inside a number
            self._buf.append(c)
            self._has_dot = True
            return None
        return self._flush()

    def flush(self) -> str | None:
        """Emit any token still in the buffer; call at end-of-stream to capture the last number."""
        return self._flush()

    def _flush(self) -> str | None:
        """Drain the buffer; return the accumulated string only if it contains at least one digit."""
        if not self._buf:
            return None
        s = "".join(self._buf)
        self._buf.clear()
        self._has_dot = False
        if not any(ch.isdigit() for ch in s):
            return None
        return s

def read_chunks(fd, index, size) -> ChunkMetadata:
    """
    Read `size` bytes at byte offset `index * size` from `fd` using pread (thread-safe, no seek).
    Lex all numeric tokens in the slice and record newline count and boundary conditions.
    """
    offset = index*size
    #print(f"thread number: {index} --- size {size} at offset {offset}")
    raw = os.pread(fd, size, offset)

    info = ChunkMetadata()
    lexer = NumberLexer()

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
    #print(raw)
    return info

def recostruct_matrix(chunks: list[ChunkMetadata]) -> Matrix:
    matrix = Matrix()

    # stitch tokens split across chunk boundaries:
    # if chunk i ends mid-number and chunk i+1 does not start on a newline,
    # the tail of chunk i and the head of chunk i+1 form a single token
    for i, chunk in enumerate(chunks):
        if i+1 < len(chunks) and chunk.is_last_truncated and not chunks[i+1].is_first_stop:
            chunk.data[-1] += chunks[i+1].data[0]
            chunks[i+1].data.pop(0)

        matrix.nums += len(chunk.data)
        matrix.data.append(chunk.data)
        matrix.rows += chunk.newline_num
    matrix.cols = matrix.nums // matrix.rows
    matrix.data.extend([] for _ in range(matrix.rows - len(matrix.data)))

    #print(len(matrix.data))
    #print(matrix.data)
    #print('--------------------------------------------------------------------')
    actual_matrix_length = len(matrix.data)
    i = 0
    while i < actual_matrix_length-1:
        curr = i
        next = i+1
        print("before:")
        print(f"curr={matrix.data[curr]}")
        print(f"next={matrix.data[next]}")
        print('-----------------------------------------------')
        if i+1 < len(matrix.data) and len(matrix.data[curr]) > matrix.cols:
            remainders = matrix.data[curr][matrix.cols:]
            matrix.data[next][:0] = remainders
            matrix.data[curr] = matrix.data[curr][:matrix.cols]

        if i+1 < len(matrix.data) and len(matrix.data[curr]) < matrix.cols:
            resize_index = matrix.cols-len(matrix.data[curr])
            missings = matrix.data[next][:resize_index]
            matrix.data[curr][len(matrix.data[curr]):] = missings
            matrix.data[next] = matrix.data[next][resize_index:]
        print("after:")
        print(f"curr={matrix.data[curr]}")
        print(f"next={matrix.data[next]}")
        print('-----------------------------------------------')
        if not matrix.data[next]:
            matrix.data.pop(next)
            actual_matrix_length -= 1
        i+=1
    return matrix

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

    merged_results = ChunkMetadata()
    try:
        with ThreadPoolExecutor(max_workers=n_thread+1) as pool:
            chunks_metas = list(pool.map(lambda i: read_chunks(fd, i, chunk_size), range(n_thread)))

        # read the remainder bytes (size % n_thread) that were not covered by the equal-sized chunks
        chunks_metas.append(read_chunks(fd, n_thread, chunk_size))
    finally:
        os.close(fd)

    matrix = recostruct_matrix(chunks_metas)

    print(matrix.data)
    print(f"col count: {matrix.cols}, row count: {matrix.rows}, total nums: {matrix.nums}")
