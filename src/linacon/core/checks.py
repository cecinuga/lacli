"""
Property checks.

All predicates return a plain Python ``bool``. Matrices are coerced to float and,
where a property only makes sense for square inputs, a non-square matrix simply
yields ``False`` instead of raising. Tolerances default to a tight ``1e-10`` so
floating-point noise from the loader does not produce false negatives.
"""
import numpy as np


def is_invertible(a: np.ndarray, tol: float | None = None) -> bool:
    """True when the matrix is square and has full rank (hence invertible)."""
    if a.ndim != 2 or a.shape[0] != a.shape[1]:
        return False
    return int(np.linalg.matrix_rank(a, tol=tol)) == a.shape[0]


def are_independent(a: np.ndarray) -> bool:
    """True when the column vectors and the row vector are linearly independent (rank == #columns == #row)."""
    if a.shape[0] != a.shape[1]:
        return False
    rank = int(np.linalg.matrix_rank(a))
    return rank == a.shape[1] and rank == a.shape[0]


def are_orthogonal(a: np.ndarray, tol: float = 1e-10) -> bool:
    """True when the column vectors are pairwise orthogonal (Gram matrix is diagonal)."""
    gram = a.T @ a
    off_diagonal = gram - np.diag(np.diag(gram))
    return bool(np.all(np.abs(off_diagonal) <= tol))


def is_symmetric(a: np.ndarray, tol: float = 1e-10) -> bool:
    """True when the matrix is square and equal to its transpose."""
    return a.ndim == 2 and a.shape[0] == a.shape[1] and bool(np.allclose(a, a.T, atol=tol))


def is_triangular(a: np.ndarray, tol: float = 1e-10) -> bool:
    """True when the matrix is upper- or lower-triangular within ``tol``."""
    upper = np.allclose(a, np.triu(a), atol=tol)
    lower = np.allclose(a, np.tril(a), atol=tol)
    return bool(upper or lower)


def is_positive_definite(a: np.ndarray, tol: float = 1e-10) -> bool:
    """True when the matrix is symmetric and its Cholesky factorization exists."""
    if not is_symmetric(a, tol):
        return False
    try:
        np.linalg.cholesky(a)
        return True
    except np.linalg.LinAlgError:
        return False
