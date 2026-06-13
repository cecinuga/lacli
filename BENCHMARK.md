## Benchmark for [LAcli](https://github.com/cecinuga/lacli)

## Reproducing
To reproduce the benchmarks do this:
- The user need to have installed on his machine the languages listed in `Programming Language support` section
- The user need to set this environment variables: 
  - `export LACLI_BENCH_PYTHON_314`=(path to the Python 3.14 executable)
  - `export LACLI_BENCH_PYTHON_314T`=(path to the Python 3.14 free-threaded executable)
  - `export LACLI_BENCH_GO_125`=(path to the Go executable)
  - `export LACLI_BENCH_RUST_195`=(path to the Rust executable)
- `./run.sh` the benchmark script and view the results in stout

## Programming Language support
Every benchmark are run for: 
- Python3.14
- Python3.14 free-threaded
- Go 1.25
- Rust 1.95

## File types support:
- CSV

## File loading
The benchmark files are in `benches/load_bench`, they misure the how long it takes to load a file from disk to memory and prepare it for processing with LAcli commands, they are written in various languages for comparison to have a critical pov for choosing the right language for LAcli.
