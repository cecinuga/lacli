from contextlib import contextmanager
from dataclasses import dataclass
import time

@dataclass
class TimerResult:
    ns: int = 0
    @property
    def ms(self) -> float:
        return self.ns / 1e6
    @property
    def s(self) -> float:
        return self.ns / 1e9

@contextmanager
def timer(label="block"):
    result = TimerResult()
    t0 = time.perf_counter_ns()
    try:
        yield result
    finally:
        result.ns = time.perf_counter_ns() - t0
