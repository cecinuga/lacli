"""
Argument parser, organized by command.

The CLI is split into one command per feature group (``bmo``, ``checks``, ``rotation``,
``factorization``); each command exposes one sub-command per single feature, so every
feature is reached through a command and never by direct access. Common flags
(``-f`` input file, ``-g`` second operand, ``-k`` scalar, ``-b`` benchmark, ``-out`` output
file) are shared through parent parsers to keep the sub-commands consistent.
"""
import argparse


def _common_parser() -> argparse.ArgumentParser:
    """Flags shared by every feature: benchmark toggle and optional CSV output path."""
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument('-b', action='store_true', default=False,
                  help='enable simple benchmark, from start to end the job')
    p.add_argument('-out', '--out', dest='out', type=str, default=None,
                  help='write the result to this CSV file (headerless, loader-compatible)')
    return p


def _one_matrix(common: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """Single-matrix feature: ``-f``."""
    p = argparse.ArgumentParser(add_help=False, parents=[common])
    p.add_argument('-f', '--file', type=str, required=True, help='the matrix file to load')
    return p


def _two_matrix(common: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """Two-operand feature: ``-f`` and ``-g``."""
    p = argparse.ArgumentParser(add_help=False, parents=[common])
    p.add_argument('-f', '--file', type=str, required=True, help='the first matrix file to load')
    p.add_argument('-g', '--file2', dest='file2', type=str, required=True,
                  help='the second matrix file to load')
    return p


def _matrix_scalar(common: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """Matrix-and-scalar feature: ``-f`` and ``-k``."""
    p = argparse.ArgumentParser(add_help=False, parents=[common])
    p.add_argument('-f', '--file', type=str, required=True, help='the matrix file to load')
    p.add_argument('-k', '--scalar', dest='scalar', type=float, required=True, help='the scalar value')
    return p


def get_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='linacon',
        description='linear algebra in your console',
        suggest_on_error=True,
    )
    commands = parser.add_subparsers(dest='command', required=True, metavar='command')

    common = _common_parser()
    one = _one_matrix(common)
    two = _two_matrix(common)
    scalar = _matrix_scalar(common)

    # Basic Matrix Operations
    bmo = commands.add_parser('bmo', help='basic matrix operations')
    bmo_feat = bmo.add_subparsers(dest='feature', required=True, metavar='feature')
    bmo_feat.add_parser('matmul', parents=[two], help='matrix multiplication')
    bmo_feat.add_parser('add', parents=[two], help='matrix sum')
    bmo_feat.add_parser('scalar-mul', parents=[scalar], help='matrix-scalar multiplication')
    bmo_feat.add_parser('dot', parents=[two], help='scalar dot product of two vectors')
    bmo_feat.add_parser('scalar-sum', parents=[scalar], help='add a scalar to every entry')
    bmo_feat.add_parser('inverse', parents=[one], help='inverse')
    bmo_feat.add_parser('transpose', parents=[one], help='transpose')
    bmo_feat.add_parser('rank', parents=[one], help='rank')

    # Checks
    checks = commands.add_parser('checks', help='matrix property checks')
    checks_feat = checks.add_subparsers(dest='feature', required=True, metavar='feature')
    checks_feat.add_parser('invertible', parents=[one], help='invertibility check')
    checks_feat.add_parser('independent', parents=[one], help='column independence check')
    checks_feat.add_parser('orthogonal', parents=[one], help='column orthogonality check')
    checks_feat.add_parser('symmetric', parents=[one], help='symmetry check')
    checks_feat.add_parser('triangular', parents=[one], help='triangular check')
    checks_feat.add_parser('positive-definite', parents=[one], help='positive-definite check')

    # Rotations
    rotation = commands.add_parser('rotation', help='rotations and affine transforms')
    rotation_feat = rotation.add_subparsers(dest='feature', required=True, metavar='feature')
    rotate = rotation_feat.add_parser('matrix', parents=[one],
                                      help='[2.1] rotate points with optional scale/shear/center/perspective')
    rotate.add_argument('--angle', type=float, required=True, help='rotation angle in degrees')
    rotate.add_argument('--axis', type=str, choices=['x', 'y', 'z'], default='z',
                        help='rotation axis for 3D points (default z)')
    rotate.add_argument('--center', type=float, nargs='+', default=None,
                        help='rotation center coordinates')
    rotate.add_argument('--scale', type=float, nargs='+', default=None,
                        help='per-axis scale (single value = uniform)')
    rotate.add_argument('--shear', type=float, nargs='+', default=None,
                        help='off-diagonal shear coefficients')
    rotate.add_argument('--perspective', type=float, nargs='+', default=None,
                        help='perspective coefficients (homogeneous bottom row)')

    # Factorization
    factorization = commands.add_parser('factorization', help='matrix factorizations')
    factorization_feat = factorization.add_subparsers(dest='feature', required=True, metavar='feature')
    factorization_feat.add_parser('gauss-jordan', parents=[one], help='Gauss-Jordan elimination (RREF)')
    factorization_feat.add_parser('lu', parents=[one], help='LU decomposition')
    factorization_feat.add_parser('ldu', parents=[one], help='LDU decomposition')
    factorization_feat.add_parser('qr', parents=[one], help='QR decomposition')
    factorization_feat.add_parser('cholesky', parents=[one], help='Cholesky decomposition')
    factorization_feat.add_parser('orthogonal', parents=[one], help='orthogonal (polar) decomposition')
    factorization_feat.add_parser('svd', parents=[one], help='singular value decomposition')
    factorization_feat.add_parser('eigen', parents=[one], help='eigenvalue decomposition')

    # Least Squares
    least_squares = commands.add_parser('least-squares', help='least squares solvers')
    least_squares_feat = least_squares.add_subparsers(dest='feature', required=True, metavar='feature')
    least_squares_feat.add_parser('solve', parents=[two], help='ordinary least squares (A=-f, b=-g)')
    least_squares_feat.add_parser('regression', parents=[two], help='linear regression (X=-f, y=-g)')
    weighted = least_squares_feat.add_parser('weighted', parents=[two], help='weighted least squares')
    weighted.add_argument('-w', '--weights', dest='weights', type=str, required=True,
                          help='per-observation weights file')
    ridge = least_squares_feat.add_parser('regularized', parents=[two], help='ridge least squares (-k = lambda)')
    ridge.add_argument('-k', '--scalar', dest='scalar', type=float, required=True,
                      help='regularization strength lambda')
    tikhonov = least_squares_feat.add_parser('regularization', parents=[two], help='Tikhonov regularization')
    tikhonov.add_argument('--gamma', dest='gamma', type=str, required=True,
                         help='Tikhonov regularization matrix file')

    return parser
