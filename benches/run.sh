#!/usr/bin/env bash

set -euo pipefail

PYTHON_DIR=$(uv python dir)

declare -A runtimes
declare -A benchs

keys=(python314 python314t)

runtimes[python314]=$LACLI_BENCH_PYTHON_314
runtimes[python314t]=$LACLI_BENCH_PYTHON_314T
benchs[python314]=./load_bench/314.py
benchs[python314t]=./load_bench/314t.py
