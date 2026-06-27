"""Merges per-chunk parse results into a single Matrix."""
from concurrent.futures import ThreadPoolExecutor
from lacli.models.matrix import ChunkMetadata, Matrix

__all__ = ["reconstruct"]

def _reconstruct_numbers(chunks: list[ChunkMetadata]) -> Matrix:
    """
    Stitch chunk-boundary-split tokens and flatten into rows; the result's `data` holds
    one token list per chunk, not yet aligned to real `cols`-sized rows.
    """
    matrix = Matrix()
    # stitch tokens split across chunk boundaries:
    # if chunk i ends mid-number and chunk i+1 does not start on a newline,
    # the tail of chunk i and the head of chunk i+1 form a single token
    i = 0
    while i < len(chunks):
        j = i
        is_truncated = chunks[j].is_last_truncated
        while j+1 < len(chunks) and is_truncated and not chunks[j+1].is_first_stop:
            chunks[i].data[-1] += chunks[j+1].data[0]
            chunks[j+1].data.pop(0)
            if len(chunks[j+1].data) == 0:
                is_truncated = chunks[j+1].is_last_truncated
                matrix.rows += chunks[i+1].newline_num
                chunks.pop(j+1)
            else: break

        matrix.nums += len(chunks[i].data)
        matrix.data.append(chunks[i].data)
        matrix.rows += chunks[i].newline_num
        i += 1
    matrix.cols = matrix.nums // matrix.rows
    matrix.data.extend([] for _ in range(matrix.rows - len(matrix.data)))

    return matrix

def _realignment(matrix: Matrix) -> Matrix:
    """
    Reflow per-chunk token lists into proper rows of `matrix.cols` length each, since byte-based
    chunk boundaries rarely align with newline-based row boundaries; moves overflow tokens
    forward, pulls missing ones from the next row, and drops any row left empty.
    """
    actual_matrix_length = len(matrix.data)
    i = 0
    while i < actual_matrix_length-1:
        curr = i
        next = i+1
        if i+1 < len(matrix.data) and len(matrix.data[curr]) > matrix.cols:
            remainders = matrix.data[curr][matrix.cols:]
            matrix.data[next][:0] = remainders
            matrix.data[curr] = matrix.data[curr][:matrix.cols]

        if i+1 < len(matrix.data) and len(matrix.data[curr]) < matrix.cols:
            resize_index = matrix.cols-len(matrix.data[curr])
            missings = matrix.data[next][:resize_index]
            matrix.data[curr][len(matrix.data[curr]):] = missings
            matrix.data[next] = matrix.data[next][resize_index:]

        if len(matrix.data[curr]) == matrix.cols:
            i+=1

        if not matrix.data[next]:
            matrix.data.pop(next)
            actual_matrix_length -= 1
    if not matrix.data[-1]:
        matrix.data.pop()
    return matrix

def _arr_str_float(arr: list):
    """Convert every element of `arr` from string to float in place; return `arr`."""
    for i in range(len(arr)):
        arr[i] = float(arr[i])
    return arr

def reconstruct(chunks: list[ChunkMetadata], max_threads:int) -> Matrix:
    """
    Build the final numeric `Matrix` from per-chunk parse results: merge boundary-split
    tokens, realign them into proper rows, then convert each row's string tokens to
    floats in batches of `max_threads` rows.
    """
    matrix = _reconstruct_numbers(chunks)
    matrix = _realignment(matrix)
    remaining_rows = matrix.rows
    try:
        chunk_threads = max_threads
        iters = (matrix.rows//chunk_threads)+(matrix.rows%chunk_threads)
        for _ in range(iters):
            with ThreadPoolExecutor(max_workers=max_threads+1) as pool:
                pool.map(lambda i: _arr_str_float(matrix.data[i+(matrix.rows-remaining_rows)]), range(chunk_threads))

            if remaining_rows < chunk_threads:
                chunk_threads = remaining_rows
            remaining_rows -= chunk_threads
    finally:
        pass
    return matrix
