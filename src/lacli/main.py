"""
CLI entry point: loads a numeric CSV-like file into a Matrix by splitting it into byte
chunks, lexing each concurrently, and stitching the per-chunk tokens back together.
"""
import sys
from pathlib import Path
import os
from lacli.arg import get_argparse
from lacli.benchmark.timer import timer
from lacli.models.matrix import Matrix
from lacli.loader.file import load
import lacli.benchmark.const as bench

print(sys.version)
print(f"parallelism enabled: {not sys._is_gil_enabled()}")

def run(file: Path, thread: int) -> Matrix:
    """Open `file`, load it into a Matrix using `thread` threads, then close the descriptor."""
    fd = os.open(file, os.O_RDONLY)
    try:
        matrix = load(fd, thread)
    finally:
        os.close(fd)
    return matrix

if __name__ == '__main__':
    args = get_argparse().parse_args()
    if args.thread is None:
        raise ValueError('thread numbers setted to None')
    if args.b:
        bench.BENCHMARK_MODES["load"] = True
        bench.BENCHMARK_MODES["load_read"] = True
        bench.BENCHMARK_MODES["load_read_file"] = True
        bench.BENCHMARK_MODES["load_merge"] = True

    run(args.file, args.thread)
