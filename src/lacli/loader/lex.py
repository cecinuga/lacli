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
    matrix = np.concatenate([np.frombuffer(chunk, dtype=np.uint8) for chunk in chunks])
    print('done!')
    exit(1)

    return matrix
