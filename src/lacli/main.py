"""
CLI entry point: loads a numeric CSV-like file into a Matrix by splitting it into byte
chunks, lexing each concurrently, and stitching the per-chunk tokens back together.
"""
import sys
from pathlib import Path
import os
from lacli.arg import get_argparse
import lacli.benchmark.bench as bench
import lacli.loader.file as file

print(sys.version)
print(f"parallelism enabled: {not sys._is_gil_enabled()}")

def run(path: Path, thread: int):
    """Open `path`, load it into a Matrix using `thread` threads, then close the descriptor."""
    fd = os.open(path, os.O_RDONLY)
    try:
        matrix = bench.bench("load", file.load, fd, thread)
    finally:
        os.close(fd)
    return matrix

if __name__ == '__main__':
    args = get_argparse().parse_args()
    if args.thread is None:
        raise ValueError('thread numbers setted to None')
    if args.b:
        bench.enable()

    run(args.file, args.thread)
