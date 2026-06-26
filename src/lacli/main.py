"""
CLI entry point: loads a numeric CSV-like file into a Matrix by splitting it into byte
chunks, lexing each concurrently, and stitching the per-chunk tokens back together.
"""
import os
import sys
from argparse import Namespace
import lacli.load.file as file
from lacli.arg import get_argparse
from lacli.benchmark.timer import timer
from lacli.models.matrix import Matrix

print(sys.version)

def run(args: Namespace) -> Matrix:
    """Open `args.file`, load it into a Matrix with `args.thread` threads, then close the file."""
    fd = os.open(args.file, os.O_RDONLY)
    matrix = file.load(fd, args.thread)
    os.close(fd)
    return matrix

if __name__ == '__main__':
    args = get_argparse().parse_args()
    if args.thread == None:
        raise ValueError('thread numbers setted to None')

    run(args)
