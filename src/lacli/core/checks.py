"""
[1] Property checks.

All predicates return a plain Python ``bool``. Matrices are coerced to float and,
where a property only makes sense for square inputs, a non-square matrix simply
yields ``False`` instead of raising. Tolerances default to a tight ``1e-10`` so
floating-point noise from the loader does not produce false negatives.
"""
import numpy as np


def is_invertible(a: np.ndarray, tol: float | None = None) -> bool:
    """[1.1] True when the matrix is square and has full rank (hence invertible)."""
    a = np.asarray(a, dtype=float)
    if a.ndim != 2 or a.shape[0] != a.shape[1]:
        return False
    return int(np.linalg.matrix_rank(a, tol=tol)) == a.shape[0]


def are_independent(a: np.ndarray) -> bool:
    """[1.2] True when the column vectors are linearly independent (rank == #columns)."""
    a = np.asarray(a, dtype=float)
    return int(np.linalg.matrix_rank(a)) == a.shape[1]


def are_orthogonal(a: np.ndarray, tol: float = 1e-10) -> bool:
    """[1.3] True when the column vectors are pairwise orthogonal (Gram matrix is diagonal)."""
    a = np.asarray(a, dtype=float)
    gram = a.T @ a
    off_diagonal = gram - np.diag(np.diag(gram))
    return bool(np.all(np.abs(off_diagonal) <= tol))


def is_symmetric(a: np.ndarray, tol: float = 1e-10) -> bool:
    """[1.4] True when the matrix is square and equal to its transpose."""
    a = np.asarray(a, dtype=float)
    return a.ndim == 2 and a.shape[0] == a.shape[1] and bool(np.allclose(a, a.T, atol=tol))


def is_triangular(a: np.ndarray, tol: float = 1e-10) -> bool:
    """[1.5] True when the matrix is upper- or lower-triangular within ``tol``."""
    a = np.asarray(a, dtype=float)
    upper = np.allclose(a, np.triu(a), atol=tol)
    lower = np.allclose(a, np.tril(a), atol=tol)
    return bool(upper or lower)


def is_positive_definite(a: np.ndarray, tol: float = 1e-10) -> bool:
    """[1.6] True when the matrix is symmetric and its Cholesky factorization exists."""
    a = np.asarray(a, dtype=float)
    if not is_symmetric(a, tol):
        return False
    try:
        np.linalg.cholesky(a)
        return True
    except np.linalg.LinAlgError:
        return False
