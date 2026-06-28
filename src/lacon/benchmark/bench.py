from lacon.benchmark.const import BENCHMARK_MODES
from lacon.benchmark.timer import timer

def bench(label:str, fn, *args):
    if BENCHMARK_MODES[label]:
        with timer(label) as t:
            res = fn(*args)
        print(f"time elapsed for {label}: {round(t.s, 3)}")
    else: res = fn(*args)
    return res

def enable():
    BENCHMARK_MODES["load"] = True
    BENCHMARK_MODES["op"] = True
