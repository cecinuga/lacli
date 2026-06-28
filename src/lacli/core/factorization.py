"""
Factorizations.

Where NumPy already ships a battle-tested LAPACK routine (QR, Cholesky, SVD,
eigendecomposition) we delegate to it. The elementary eliminations that NumPy
does not expose directly (Gauss-Jordan / RREF, LU and LDU) are implemented with
rank-1 vectorized updates (``np.outer``) so each elimination step touches whole
sub-matrices at once instead of looping element by element.
"""
import numpy as np


def gauss_jordan(a: np.ndarray, tol: float = 1e-12) -> np.ndarray:
    """Reduced row echelon form via Gauss-Jordan elimination with partial pivoting."""
    m = np.array(a, dtype=float)
    rows, cols = m.shape
    pivot_row = 0
    for col in range(cols):
        if pivot_row >= rows:
            break
        candidates = np.abs(m[pivot_row:, col])
        best = int(np.argmax(candidates))
        if candidates[best] <= tol:
            continue
        best += pivot_row
        m[[pivot_row, best]] = m[[best, pivot_row]]
        m[pivot_row] /= m[pivot_row, col]
        factors = m[:, col].copy()
        factors[pivot_row] = 0.0
        m -= np.outer(factors, m[pivot_row])  # zero out the whole column at once
        pivot_row += 1
    return m


def lu(a: np.ndarray):
    """LU decomposition with partial pivoting: returns ``(P, L, U)`` with ``P @ A == L @ U``."""
    A = np.array(a, dtype=float)
    n, cols = A.shape
    if n != cols:
        raise ValueError("LU decomposition requires a square matrix")
    U = A.copy()
    L = np.eye(n)
    P = np.eye(n)
    for k in range(n):
        pivot = int(np.argmax(np.abs(U[k:, k]))) + k
        if pivot != k:
            U[[k, pivot]] = U[[pivot, k]]
            P[[k, pivot]] = P[[pivot, k]]
            if k > 0:
                L[[k, pivot], :k] = L[[pivot, k], :k]
        if U[k, k] == 0:
            continue
        factors = U[k + 1:, k] / U[k, k]
        L[k + 1:, k] = factors
        U[k + 1:] -= np.outer(factors, U[k])  # eliminate the sub-column in one shot
    return P, L, U


def ldu(a: np.ndarray):
    """LDU decomposition: returns ``(P, L, D, U)`` with ``P @ A == L @ D @ U``, ``U`` unit-diagonal."""
    P, L, raw_u = lu(a)
    d = np.diag(raw_u).copy()
    safe = np.where(d == 0, 1.0, d)  # avoid division by zero on singular pivots
    U = raw_u / safe[:, None]
    return P, L, np.diag(d), U


def qr(a: np.ndarray):
    """QR decomposition: returns ``(Q, R)`` with orthonormal ``Q`` and upper-triangular ``R``."""
    return np.linalg.qr(np.asarray(a, dtype=float))


def cholesky(a: np.ndarray) -> np.ndarray:
    """Cholesky factor ``L`` (lower-triangular) of a symmetric positive-definite matrix."""
    return np.linalg.cholesky(np.asarray(a, dtype=float))


def orthogonal(a: np.ndarray):
    """
    Orthogonal (polar) decomposition: returns ``(Q, P)`` with orthogonal ``Q`` and
    symmetric positive-semidefinite ``P`` such that ``A == Q @ P``. Built from the SVD.
    """
    u, s, vt = np.linalg.svd(np.asarray(a, dtype=float))
    q = u @ vt
    p = (vt.T * s) @ vt
    return q, p


def svd(a: np.ndarray):
    """Singular value decomposition: returns ``(U, s, Vt)`` with ``A == U @ diag(s) @ Vt``."""
    return np.linalg.svd(np.asarray(a, dtype=float))


def eigen(a: np.ndarray):
    """Eigenvalue decomposition: returns ``(eigenvalues, eigenvectors)`` (columns are vectors)."""
    return np.linalg.eig(np.asarray(a, dtype=float))
