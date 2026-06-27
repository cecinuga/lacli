# TODO

## [`src/lacli`](src/lacli/main.py)
- Improve a lot the error handling.

## [`src/lacli/download`](src/lacli/download)
- Add benchmarks mode: create a global state in `lacli.benchmark.timer` and handle all the logic in there; every bench point must only set the relative variable, and when the program stops, print the aggregated times.
- Add benchmarks timers: add a timer between each step of the load pipeline, run the integration tests, then check the aggregated times for each function. Optimize the slowest!!!
- If `n_thread` is `1`, disable multithreading and load the file sequentially.
- Add support for download files from remote, public URL
