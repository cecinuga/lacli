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
        prog='lacli',
        description='linear algebra in your console',
        suggest_on_error=True,
    )
    commands = parser.add_subparsers(dest='command', required=True, metavar='command')

    common = _common_parser()
    one = _one_matrix(common)
    two = _two_matrix(common)
    scalar = _matrix_scalar(common)

    # [0] Basic Matrix Operations
    bmo = commands.add_parser('bmo', help='basic matrix operations')
    bmo_feat = bmo.add_subparsers(dest='feature', required=True, metavar='feature')
    bmo_feat.add_parser('matmul', parents=[two], help='[0.1] matrix multiplication')
    bmo_feat.add_parser('add', parents=[two], help='[0.2] matrix sum')
    bmo_feat.add_parser('scalar-mul', parents=[scalar], help='[0.3] matrix-scalar multiplication')
    bmo_feat.add_parser('dot', parents=[two], help='[0.4] scalar dot product of two vectors')
    bmo_feat.add_parser('scalar-sum', parents=[scalar], help='[0.5] add a scalar to every entry')
    bmo_feat.add_parser('inverse', parents=[one], help='[0.6] inverse')
    bmo_feat.add_parser('transpose', parents=[one], help='[0.7] transpose')
    bmo_feat.add_parser('rank', parents=[one], help='[0.8] rank')

    # [1] Checks
    checks = commands.add_parser('checks', help='matrix property checks')
    checks_feat = checks.add_subparsers(dest='feature', required=True, metavar='feature')
    checks_feat.add_parser('invertible', parents=[one], help='[1.1] invertibility check')
    checks_feat.add_parser('independent', parents=[one], help='[1.2] column independence check')
    checks_feat.add_parser('orthogonal', parents=[one], help='[1.3] column orthogonality check')
    checks_feat.add_parser('symmetric', parents=[one], help='[1.4] symmetry check')
    checks_feat.add_parser('triangular', parents=[one], help='[1.5] triangular check')
    checks_feat.add_parser('positive-definite', parents=[one], help='[1.6] positive-definite check')

    # [2] Rotations
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

    # [3] Factorization
    factorization = commands.add_parser('factorization', help='matrix factorizations')
    factorization_feat = factorization.add_subparsers(dest='feature', required=True, metavar='feature')
    factorization_feat.add_parser('gauss-jordan', parents=[one], help='[3.1] Gauss-Jordan elimination (RREF)')
    factorization_feat.add_parser('lu', parents=[one], help='[3.2] LU decomposition')
    factorization_feat.add_parser('ldu', parents=[one], help='[3.3] LDU decomposition')
    factorization_feat.add_parser('qr', parents=[one], help='[3.4] QR decomposition')
    factorization_feat.add_parser('cholesky', parents=[one], help='[3.5] Cholesky decomposition')
    factorization_feat.add_parser('orthogonal', parents=[one], help='[3.6] orthogonal (polar) decomposition')
    factorization_feat.add_parser('svd', parents=[one], help='[3.7] singular value decomposition')
    factorization_feat.add_parser('eigen', parents=[one], help='[3.8] eigenvalue decomposition')

    return parser
