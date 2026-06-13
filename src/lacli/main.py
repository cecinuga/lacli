import numpy as np
import dis
from sys import stdout

def main():
    with open('test_assets/matrix.json', 'r') as f:
        for line in f.readlines():
            for c in line:
                stdout.write(f"{c}")

        stdout.flush()

if __name__ == "__main__":
    main()

    import timeit
    setup = "xs = list(range(10000))"
    t1 = timeit.timeit("r=[]\nfor x in xs: r.append(x*2)", setup=setup, number=10000)
    t2 = timeit.timeit("[x*2 for x in xs]", setup=setup, number=10000)
    print(f"append loop: {t1:.3f}s   comprehension: {t2:.3f}s   ratio: {t1/t2:.2f}x")
