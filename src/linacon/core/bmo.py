"""
Basic Matrix Operations.

Every function is a thin, vectorized NumPy wrapper so the heavy lifting stays in
optimized native code. Inputs are coerced to float `np.ndarray` to keep behaviour
predictable regardless of how the loader typed the data.
"""
import numpy as np
from linacon.models import ShapeException

def matmul(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Matrix multiplication for arbitrary (conformable) dimensions: ``A @ B``."""
    if a.shape[1] != b.shape[0]:
        raise ShapeException(f"Shape must be compatible: {a.shape[1]} != {b.shape[0]}")

    return np.matmul(a, b, dtype=np.float32)

def _matadd(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Element-wise matrix sum: ``A + B``."""
    if a.shape != b.shape:
        raise ShapeException(f"Shape must be compatible: {a.shape} != {b.shape}")
    return np.add(a, b, dtype=np.float32)

def _matvectadd(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Element-wise matrix vector sum ``A + v``."""
    if a.shape[0] != b.shape[0] or b.shape[1] == 1:
        raise ShapeException(f"Shape must be compatible: {a.shape[0]} != {b.shape[0]} and {b.shape[1]} != 1")
    return np.add(a, b, dtype=np.float32)

def add(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    if b.shape[1] != 1:
        return _matadd(a, b)
    return _matvectadd(a, b)

def scalar_mul(a: np.ndarray, k: float) -> np.ndarray:
    """Multiply every entry of the matrix by the scalar ``k``."""
    return a * k

def dot(a: np.ndarray, b: np.ndarray) -> float:
    """Scalar dot product of two vectors; inputs are flattened first."""
    if a.shape != b.shape:
        raise ShapeException(f"Shape must be compatible: {a.shape} != {b.shape}")
    return np.dot(a, b)

def scalar_sum(a: np.ndarray, k: float) -> np.ndarray:
    """Add the scalar ``k`` to every entry of the matrix."""
    return a + k

def inverse(a: np.ndarray) -> np.ndarray:
    """Inverse of a square, non-singular matrix."""
    return np.linalg.inv(a)

def transpose(a: np.ndarray) -> np.ndarray:
    """Transpose of the matrix."""
    return a.T

def rank(a: np.ndarray) -> int:
    """Numerical rank via the singular value decomposition."""
    return int(np.linalg.matrix_rank(a))
