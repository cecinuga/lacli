"""
CLI entry point.

Loads numeric CSV matrices via PyArrow (see `run`) and dispatches the parsed command /
feature to the matching `la_cli.core` routine. Results are printed to stdout and, when
``-out`` is given, written to CSV by `la_cli.writer`.
"""
from pathlib import Path
import numpy as np
from la_cli.arg import get_argparse
import la_cli.benchmark.bench as bench
import pyarrow.csv as pv
from la_cli.core import bmo, checks, rotation, factorization, least_squares
from la_cli.writer import write_csv

read_opts = pv.ReadOptions(
    autogenerate_column_names=True,  # niente header → genera f0, f1, f2, ...
    use_threads=True,                # parsing multi-thread interno (default True)
    block_size=8 * 1024 * 1024,      # 8MB per blocco, vedi sotto
)

parse_opts = pv.ParseOptions(
    delimiter=',',
    quote_char=False,                # niente quoting, accelera il parser
    escape_char=False,               # niente escape
    newlines_in_values=False,        # newline è SEMPRE fine riga, accelera
)

def run(path: Path) -> np.ndarray:
    """Parse `path` as a CSV matrix via pyarrow and return it as a 2D numpy array."""
    table = bench.bench(
        "load",
        pv.read_csv,
        path,
        read_opts,
        parse_opts,
    )
    return np.column_stack([col.to_numpy() for col in table.columns])


def _dispatch(args):
    """Run the operation selected by `args.command` / `args.feature` and return its result."""
    command, feature = args.command, args.feature

    # [0] Basic Matrix Operations
    if command == 'bmo':
        if feature == 'matmul':
            return bmo.matmul(run(args.file), run(args.file2))
        if feature == 'add':
            return bmo.add(run(args.file), run(args.file2))
        if feature == 'scalar-mul':
            return bmo.scalar_mul(run(args.file), args.scalar)
        if feature == 'dot':
            return bmo.dot(run(args.file), run(args.file2))
        if feature == 'scalar-sum':
            return bmo.scalar_sum(run(args.file), args.scalar)
        if feature == 'inverse':
            return bmo.inverse(run(args.file))
        if feature == 'transpose':
            return bmo.transpose(run(args.file))
        if feature == 'rank':
            return bmo.rank(run(args.file))

    # [1] Checks
    if command == 'checks':
        a = run(args.file)
        if feature == 'invertible':
            return checks.is_invertible(a)
        if feature == 'independent':
            return checks.are_independent(a)
        if feature == 'orthogonal':
            return checks.are_orthogonal(a)
        if feature == 'symmetric':
            return checks.is_symmetric(a)
        if feature == 'triangular':
            return checks.is_triangular(a)
        if feature == 'positive-definite':
            return checks.is_positive_definite(a)

    # [2] Rotations
    if command == 'rotation' and feature == 'matrix':
        transform, transformed = rotation.rotate(
            run(args.file), args.angle, axis=args.axis, center=args.center,
            scale=args.scale, shear=args.shear, perspective=args.perspective,
        )
        return {"transform": transform, "transformed": transformed}

    # [3] Factorization
    if command == 'factorization':
        a = run(args.file)
        if feature == 'gauss-jordan':
            return {"rref": factorization.gauss_jordan(a)}
        if feature == 'lu':
            p, l, u = factorization.lu(a)
            return {"P": p, "L": l, "U": u}
        if feature == 'ldu':
            p, l, d, u = factorization.ldu(a)
            return {"P": p, "L": l, "D": d, "U": u}
        if feature == 'qr':
            q, r = factorization.qr(a)
            return {"Q": q, "R": r}
        if feature == 'cholesky':
            return {"L": factorization.cholesky(a)}
        if feature == 'orthogonal':
            q, p = factorization.orthogonal(a)
            return {"Q": q, "P": p}
        if feature == 'svd':
            u, s, vt = factorization.svd(a)
            return {"U": u, "S": s, "Vt": vt}
        if feature == 'eigen':
            values, vectors = factorization.eigen(a)
            return {"eigenvalues": values, "eigenvectors": vectors}

    # Least Squares
    if command == 'least-squares':
        if feature == 'solve':
            return least_squares.least_squares(run(args.file), run(args.file2))
        if feature == 'regression':
            return least_squares.linear_regression(run(args.file), run(args.file2))
        if feature == 'weighted':
            return least_squares.weighted_least_squares(
                run(args.file), run(args.file2), run(args.weights))
        if feature == 'regularized':
            return least_squares.regularized_least_squares(
                run(args.file), run(args.file2), args.scalar)
        if feature == 'regularization':
            return least_squares.regularization(
                run(args.file), run(args.file2), run(args.gamma))

    raise ValueError(f"unknown command/feature: {command}/{feature}")


def _present(result) -> None:
    """Print a result (scalar, array, or named multi-output) to stdout."""
    if isinstance(result, dict):
        for name, value in result.items():
            print(f"# {name}")
            print(np.asarray(value))
    else:
        print(result if np.isscalar(result) else np.asarray(result))


if __name__ == '__main__':
    args = get_argparse().parse_args()

    if args.b:
        bench.enable()

    result = bench.bench("op", _dispatch, args)
    _present(result)

    if args.out:
        written = write_csv(result, args.out)
        print("written: " + ", ".join(str(p) for p in written))
