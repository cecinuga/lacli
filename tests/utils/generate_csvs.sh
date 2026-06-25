#!/usr/bin/env bash
# Generates N CSV files by invoking generate_csv.sh with random parameters.
# Usage: ./generate_csvs.sh <count> [outdir=<dir>]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GENERATOR="$SCRIPT_DIR/generate_csv.sh"

# -------- 1. Argument parsing --------
count=""
outdir="./benches/datasets"

for arg in "$@"; do
    case "$arg" in
        outdir=*) outdir="${arg#outdir=}" ;;
        -h|--help)
            cat <<EOF
Usage: $0 <count> [outdir=<dir>]

  count     number of CSV files to generate (positive integer)
  outdir    output directory (default: current directory)

Random parameter ranges per file:
  row    [1, 500]
  col    [1, 50]
  type   int | float  (50/50)
EOF
            exit 0
            ;;
        *)
            if [[ -z "$count" ]]; then
                count="$arg"
            else
                echo "Error: unrecognized argument '$arg'" >&2
                exit 2
            fi
            ;;
    esac
done

# -------- 2. Validation --------
[[ -n "$count" ]] \
    || { echo "Error: count is required. Usage: $0 <count> [outdir=<dir>]" >&2; exit 2; }

[[ "$count" =~ ^[1-9][0-9]*$ ]] \
    || { echo "Error: count must be a positive integer, got '$count'" >&2; exit 2; }

[[ -x "$GENERATOR" ]] \
    || { echo "Error: generator script not found or not executable: $GENERATOR" >&2; exit 2; }

mkdir -p "$outdir"

# -------- 3. Generation --------
types=("int" "float")

for ((k = 1; k <= count; k++)); do
    rows=$(( RANDOM % 500 + 1 ))
    cols=$(( RANDOM % 500 + 1 ))
    type="${types[RANDOM % 2]}"
    outfile="$(printf '%s/%d_%d_%s.csv' "$outdir" "$rows" "$cols" "$type")"

    "$GENERATOR" "row=$rows" "col=$cols" "type=$type" "out=$outfile"
done

echo "Generated $count CSV file(s) in: $outdir" >&2
