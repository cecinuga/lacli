"""Merges per-chunk parse results (ChunkMetadata) produced by load.file.read_chunk into a single Matrix."""
import os
from concurrent.futures import ThreadPoolExecutor
from lacli.models.matrix import ChunkMetadata, Matrix

__all__ = ["reconstruct"]

def _reconstruct_numbers(chunks: list[ChunkMetadata]) -> Matrix:
    """
    Stitch chunk-boundary-split tokens and flatten chunk data into matrix rows.

    Input: ordered list of `ChunkMetadata` (one per file chunk).
    Output: a `Matrix` whose `data` holds one list-of-tokens per chunk (not yet
    aligned to real rows) and whose `rows`/`nums`/`cols` are derived counts.
    """
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

    return matrix

def _realignment(matrix: Matrix) -> Matrix:
    """
    Reflow per-chunk token lists into proper rows of `matrix.cols` length each.

    Chunk boundaries (byte-based) rarely align with row boundaries (newline-based),
    so this moves overflow tokens forward and pulls missing tokens from the next
    row, dropping any row left empty in the process.

    Input/Output: `Matrix` with `data` realigned in place; same object is returned.
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
    Build the final numeric `Matrix` from per-chunk parse results.

    Pipeline: merge boundary-split tokens and flatten chunks (`_reconstruct_numbers`),
    realign tokens into proper rows (`_realignment`), then convert each row's string
    tokens to floats, processing `max_threads` rows at a time via a thread pool.

    Input: `chunks` per-file-chunk parse results, `max_threads` rows to convert per batch.
    Output: the completed `Matrix` with float data.
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
