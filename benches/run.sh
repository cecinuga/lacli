#!/usr/bin/env bash

set -euo pipefail

PYTHON_DIR=$(uv python dir)
PYTHON_314=cpython-3.14-linux-x86_64-gnu
PYTHON_314T=cpython-3.14+freethreaded-linux-x86_64-gnu

ls $PYTHON_DIR

echo $PYTHON_DIR
