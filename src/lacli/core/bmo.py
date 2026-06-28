"""
[0] Basic Matrix Operations.

Every function is a thin, vectorized NumPy wrapper so the heavy lifting stays in
optimized native code. Inputs are coerced to float `np.ndarray` to keep behaviour
predictable regardless of how the loader typed the data.
"""
import numpy as np


def matmul(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """[0.1] Matrix multiplication for arbitrary (conformable) dimensions: ``A @ B``."""
    return np.asarray(a, dtype=float) @ np.asarray(b, dtype=float)


def add(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """[0.2] Element-wise matrix sum: ``A + B``."""
    return np.asarray(a, dtype=float) + np.asarray(b, dtype=float)


def scalar_mul(a: np.ndarray, k: float) -> np.ndarray:
    """[0.3] Multiply every entry of the matrix by the scalar ``k``."""
    return np.asarray(a, dtype=float) * float(k)


def dot(a: np.ndarray, b: np.ndarray) -> float:
    """[0.4] Scalar dot product of two vectors; inputs are flattened first."""
    return float(np.dot(np.ravel(np.asarray(a, dtype=float)),
                        np.ravel(np.asarray(b, dtype=float))))


def scalar_sum(a: np.ndarray, k: float) -> np.ndarray:
    """[0.5] Add the scalar ``k`` to every entry of the matrix."""
    return np.asarray(a, dtype=float) + float(k)


def inverse(a: np.ndarray) -> np.ndarray:
    """[0.6] Inverse of a square, non-singular matrix."""
    return np.linalg.inv(np.asarray(a, dtype=float))


def transpose(a: np.ndarray) -> np.ndarray:
    """[0.7] Transpose of the matrix."""
    return np.asarray(a, dtype=float).T


def rank(a: np.ndarray) -> int:
    """[0.8] Numerical rank via the singular value decomposition."""
    return int(np.linalg.matrix_rank(np.asarray(a, dtype=float)))
