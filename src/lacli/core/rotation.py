"""
[2] Rotations.

[2.1] builds a homogeneous affine transformation from a rotation plus the optional
modifiers (scale, shear, center, perspective) and applies it to a set of points.

The input ``matrix`` is interpreted as ``N`` row-points in ``D``-dimensional space
(``D`` is 2 or 3). The transform is composed in homogeneous coordinates as::

    M = T(center) @ R @ S @ H @ T(-center)        (+ perspective bottom row)

and every point ``p`` is mapped to ``(M @ [p, 1]) / w``.
"""
import numpy as np


def _rotation_linear(angle: float, axis: str, dim: int) -> np.ndarray:
    """Linear (non-homogeneous) rotation block for a 2D plane or a 3D axis."""
    c, s = np.cos(angle), np.sin(angle)
    if dim == 2:
        return np.array([[c, -s], [s, c]])
    if dim == 3:
        if axis == "x":
            return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
        if axis == "y":
            return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
        if axis == "z":
            return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
        raise ValueError(f"axis must be one of x/y/z, got {axis!r}")
    raise ValueError(f"rotation supports 2D or 3D points, got dimension {dim}")


def _scale_linear(scale, dim: int) -> np.ndarray:
    """Diagonal scaling block; a single value is broadcast to every axis."""
    if scale is None:
        return np.eye(dim)
    scale = np.atleast_1d(np.asarray(scale, dtype=float))
    if scale.size == 1:
        scale = np.full(dim, scale.item())
    return np.diag(scale)


def _shear_linear(shear, dim: int) -> np.ndarray:
    """Off-diagonal shear block; values fill the off-diagonal entries row by row."""
    h = np.eye(dim)
    if shear is None:
        return h
    values = np.atleast_1d(np.asarray(shear, dtype=float))
    off = [(i, j) for i in range(dim) for j in range(dim) if i != j]
    for (i, j), v in zip(off, values):
        h[i, j] = v
    return h


def transform_matrix(dim, angle, axis="z", center=None, scale=None,
                     shear=None, perspective=None, degrees=True) -> np.ndarray:
    """Compose the ``(dim+1) x (dim+1)`` homogeneous transform from its parts."""
    if degrees:
        angle = np.deg2rad(angle)

    linear = _rotation_linear(angle, axis, dim) @ _scale_linear(scale, dim) @ _shear_linear(shear, dim)
    m = np.eye(dim + 1)
    m[:dim, :dim] = linear

    if center is not None:
        c = np.asarray(center, dtype=float)
        to_origin = np.eye(dim + 1)
        to_origin[:dim, dim] = -c
        from_origin = np.eye(dim + 1)
        from_origin[:dim, dim] = c
        m = from_origin @ m @ to_origin

    if perspective is not None:
        p = np.atleast_1d(np.asarray(perspective, dtype=float))
        m[dim, :dim] = p[:dim]

    return m


def rotate(points: np.ndarray, angle: float, axis="z", center=None, scale=None,
           shear=None, perspective=None, degrees=True):
    """
    [2.1] Apply a rotation (plus optional modifiers) to ``points``.

    Returns ``(transform, transformed)`` where ``transform`` is the homogeneous
    matrix and ``transformed`` are the mapped row-points in the original dimension.
    """
    points = np.atleast_2d(np.asarray(points, dtype=float))
    n, dim = points.shape

    m = transform_matrix(dim, angle, axis=axis, center=center, scale=scale,
                         shear=shear, perspective=perspective, degrees=degrees)

    homogeneous = np.hstack([points, np.ones((n, 1))])
    mapped = homogeneous @ m.T
    w = mapped[:, dim:dim + 1]
    transformed = mapped[:, :dim] / w
    return m, transformed
