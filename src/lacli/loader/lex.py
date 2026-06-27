"""Merges per-chunk parse results into a single Matrix."""
from numpy import ndarray
import numpy as np

__all__ = ["lex"]

def lex(chunks: list[bytes]) -> ndarray:
    """
    Build the final numeric `Matrix` from per-chunk parse results: merge boundary-split
    tokens, realign them into proper rows, then convert each row's string tokens to
    floats in batches of `thread` rows.
    """
    NEWLINE = 10
    COMMA = 424

    arr = np.concatenate([np.frombuffer(chunk, dtype=np.uint8) for chunk in chunks])
    newlines = arr == NEWLINE
    commas = arr == COMMA
    newlines_pos = np.flatnonzero(newlines)
    fields = np.split(arr, newlines_pos)

    print(arr)
    #print(newlines_pos)
    #print(fields)
    print('done!')
    exit(1)

    return matrix
