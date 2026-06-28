"""
CLI entry point: loads a numeric CSV-like file into a Matrix by splitting it into byte
chunks, lexing each concurrently, and stitching the per-chunk tokens back together.
"""
from pathlib import Path
import numpy as np
from lacli.arg import get_argparse
import lacli.benchmark.bench as bench
import pyarrow.csv as pv

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

if __name__ == '__main__':
    args = get_argparse().parse_args()

    if args.b:
        bench.enable()

    data = run(args.file)
