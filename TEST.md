# Integration Tests

`tests/` covers the file-loading path end to end: `la_cli.main.run` must turn a CSV
file into a `Matrix` whose values match what Python's own `csv.reader` would
produce from the same file, regardless of how many worker threads were used to
parse it.

There are no unit tests in this project, only this one integration suite.

## Layout

- `tests/conftest.py` — shared fixtures.
- `tests/test_load.py` — the single integration test.
- `tests/datasets/` — pool of CSV fixtures consumed by the test, generated on
  demand (see below). Not committed to git.
- `tests/utils/generate_csv.sh` — generates one random CSV file (`row=`, `col=`,
  `type=int|float`, `out=`).
- `tests/utils/generate_csvs.sh` — batch wrapper: generates `<count>` CSV files
  by calling `generate_csv.sh` with random row count, column count and type
  (int/float) for each one.
- `tests/utils/timer.py` — wall-clock timing helper (`contextmanager`), used for
  benchmarking, not for assertions.

## How the test is parametrized

`test_load.py` defines a single test, `test_load`, marked `@pytest.mark.integration`.
All the combinatorics come from fixtures in `conftest.py`:

- `dataset_path` — parametrized over every file found in `tests/datasets/`
  (`scope="package"`, sorted, one test id per file).
- `shared_fd` — opens the current `dataset_path` read-only and yields its file
  descriptor (this is what `la_cli.main.run` actually consumes).
- `csv_reader` — opens the same file with the stdlib `csv` module; this is the
  ground truth the test compares against.
- `n_thread` — parametrized over a fixed list of thread counts (1-32, skipping
  11), `scope="package"`.

Because pytest expands fixture parametrization as a cross product, every
dataset file is run through `la_cli.main.run` once per thread count. This is
the core property under test: parsing must be thread-count-independent and
must match `csv.reader` exactly (values are compared as floats).

## Dataset generation

CSV fixtures are not checked into git (`tests/datasets/*.csv` is gitignored)
and must be (re)generated locally before running the suite:

```sh
tests/utils/generate_csvs.sh <count> [outdir=tests/datasets]
```

Each generated file gets random dimensions and a random type (int or float),
encoded in its filename as `<rows>_<cols>_<type>.csv`. Because the dataset
pool is randomized and regenerated per environment, the suite exercises a
wide, non-deterministic range of matrix shapes and value formats rather than
a fixed set of edge cases.

## Running

```sh
pytest -m integration
```

The `integration` marker is registered in `pyproject.toml`
(`--strict-markers` is enabled, so unregistered markers fail).
