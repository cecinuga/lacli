"""
CLI entry point: loads a numeric CSV-like file into a Matrix using parallel threads.

Every line is intended to be an array of the matrix. To load the matrix, the file is
split into byte chunks (one per thread plus a remainder), each chunk is lexed
concurrently, and the resulting per-chunk token lists are stitched back into a Matrix.
"""
import os
import sys
from lacli.load.file import load
from lacli.arg import get_argparse

print(sys.version)                      # must contain "free-threaded build"

if __name__ == '__main__':
    args = get_argparse().parse_args()

    if args.thread == None:
        raise ValueError('n_thread setted to None')

    fd = os.open(args.file, os.O_RDONLY)
    load(fd, args.thread)
    os.close(fd)
