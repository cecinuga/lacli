"""
[4] Least squares.

Solvers for the over-determined system ``A x ≈ b``. The plain and weighted variants
go through NumPy's LAPACK-backed ``lstsq`` (robust to rank-deficient ``A``); the
regularized variants form the (small, well-conditioned) normal equations and solve
them directly. Targets ``b`` may be a single column or several columns at once, in
which case every solver returns one solution per column.
"""
import numpy as np


def least_squares(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """[4.1] Minimum-norm solution of ``min ||A x - b||₂`` via the SVD-based lstsq."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    x, *_ = np.linalg.lstsq(a, b, rcond=None)
    return x


def weighted_least_squares(a: np.ndarray, b: np.ndarray, weights: np.ndarray) -> np.ndarray:
    """[4.2] Weighted least squares ``min Σ wᵢ (Aᵢx - bᵢ)²``; rows are scaled by ``sqrt(w)``."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    sqrt_w = np.sqrt(np.ravel(np.asarray(weights, dtype=float)))
    aw = a * sqrt_w[:, None]
    bw = b * sqrt_w[:, None] if b.ndim > 1 else b * sqrt_w
    x, *_ = np.linalg.lstsq(aw, bw, rcond=None)
    return x


def regularized_least_squares(a: np.ndarray, b: np.ndarray, lam: float) -> np.ndarray:
    """[4.3] Ridge / Tikhonov least squares ``min ||A x - b||² + λ||x||²``."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    lhs = a.T @ a + float(lam) * np.eye(a.shape[1])
    return np.linalg.solve(lhs, a.T @ b)


def regularization(a: np.ndarray, b: np.ndarray, gamma: np.ndarray) -> np.ndarray:
    """[4.4] General Tikhonov regularization ``min ||A x - b||² + ||Γ x||²`` for a matrix ``Γ``."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    g = np.asarray(gamma, dtype=float)
    lhs = a.T @ a + g.T @ g
    return np.linalg.solve(lhs, a.T @ b)


def linear_regression(x: np.ndarray, y: np.ndarray, intercept: bool = True) -> np.ndarray:
    """[4.5] Ordinary linear regression; with ``intercept`` the bias is the first coefficient."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    design = np.hstack([np.ones((x.shape[0], 1)), x]) if intercept else x
    coef, *_ = np.linalg.lstsq(design, y, rcond=None)
    return coef
