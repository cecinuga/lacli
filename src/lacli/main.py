"""
CLI entry point: loads a numeric CSV-like file into a Matrix using parallel threads.

Every line is intended to be an array of the matrix. To load the matrix, the file is
split into byte chunks (one per thread plus a remainder), each chunk is lexed
concurrently, and the resulting per-chunk token lists are stitched back into a Matrix.
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
    fd = os.open(args.file, os.O_RDONLY)
    matrix = file.load(fd, args.thread)
    os.close(fd)
    return matrix

if __name__ == '__main__':
    args = get_argparse().parse_args()
    if args.thread == None:
        raise ValueError('thread numbers setted to None')

    run(args)
