"""Benchmarking helper: measures wall-clock time of a `with` block."""
from contextlib import contextmanager
from dataclasses import dataclass
import time
import lacli.benchmark.const as bench

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
    Times the wrapped `with` block; `label` is currently unused. Yields a `TimerResult`
    whose `.ns` is only populated once the block exits.
    """
    if bench.BENCHMARK_MODES[label]:
        result = TimerResult()
        t0 = time.perf_counter_ns()
        try:
            yield result
        finally:
            result.ns = time.perf_counter_ns() - t0
            print(f"time elapsed for {label}: {round(result.s, 3)}")
    else: yield None
