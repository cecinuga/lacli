"""Benchmarking helper: measures wall-clock time of a `with` block."""
from contextlib import contextmanager
from dataclasses import dataclass
import time

@dataclass
class TimerResult:
    """Elapsed time of a timed block, stored in nanoseconds with ms/s convenience accessors."""
    ns: int = 0
    @property
    def ms(self) -> float:
        return self.ns / 1e6
    @property
    def s(self) -> float:
        return self.ns / 1e9

@contextmanager
def timer(label="block"):
    """
    Context manager that times the wrapped block.

    Input: `label` (unused for now, intended for identifying the block).
    Output: yields a `TimerResult` whose `.ns` is filled in once the block exits.
    """
    result = TimerResult()
    t0 = time.perf_counter_ns()
    try:
        yield result
    finally:
        result.ns = time.perf_counter_ns() - t0
