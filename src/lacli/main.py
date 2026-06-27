"""
CLI entry point: loads a numeric CSV-like file into a Matrix by splitting it into byte
chunks, lexing each concurrently, and stitching the per-chunk tokens back together.
"""
from pathlib import Path
import os
import sys
from lacli.arg import get_argparse
from lacli.models.matrix import Matrix
from lacli.download.file import download

print(sys.version)

def run(file: Path, thread: int) -> Matrix:
    """Open `file`, load it into a Matrix using `thread` threads, then close the descriptor."""
    fd = os.open(file, os.O_RDONLY)
    try:
        matrix = download(fd, thread)
    finally:
        os.close(fd)
    return matrix

if __name__ == '__main__':
    args = get_argparse().parse_args()
    if args.thread is None:
        raise ValueError('thread numbers setted to None')

    run(args.file, args.thread)
