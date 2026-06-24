#!/usr/bin/env bash
# Generates a CSV of random numbers.
# Usage: ./gen_random_csv.sh row=<int> col=<int> type=<int|float> [out=<file>]

set -euo pipefail

# -------- 1. Argument parsing (key=value format) --------
rows="" cols="" type="" out=""

for arg in "$@"; do
    case "$arg" in
        row=*)  rows="${arg#row=}"  ;;
        col=*)  cols="${arg#col=}"  ;;
        type=*) type="${arg#type=}" ;;
        out=*)  out="${arg#out=}"   ;;
        -h|--help)
            cat <<EOF
Usage: $0 row=<int> col=<int> type=<int|float> [out=<file>]

  row    number of rows    (positive integer)
  col    number of columns (positive integer)
  type   int    -> integers, randomly positive or negative, magnitude in [0, 100)
         float -> reals with random precision (1-10 decimal digits),
                   randomly chosen as: positive [1, 10001), negative (-10001, -1], or fractional [0, 1)
  out    output file (default: stdout)
EOF
            exit 0
            ;;
        *)
            echo "Error: unrecognized argument '$arg'" >&2
            exit 2
            ;;
    esac
done

# -------- 2. Validation --------
[[ -n "$rows" && -n "$cols" && -n "$type" ]] \
    || { echo "Error: row, col and type are required. Use --help." >&2; exit 2; }

[[ "$rows" =~ ^[1-9][0-9]*$ ]] \
    || { echo "Error: row must be a positive integer (no zero, no sign), got '$rows'" >&2; exit 2; }

[[ "$cols" =~ ^[1-9][0-9]*$ ]] \
    || { echo "Error: col must be a positive integer, got '$cols'" >&2; exit 2; }

[[ "$type" == "int" || "$type" == "float" ]] \
    || { echo "Error: type must be 'int' or 'float', got '$type'" >&2; exit 2; }

# -------- 3. Generation (all inside awk, single process) --------
generate() {
    awk -v rows="$rows" -v cols="$cols" -v type="$type" '
    BEGIN {
        srand()                                 # seed = time(NULL); without this, awk would always use the same seed
        for (i = 1; i <= rows; i++) {
            line = ""
            for (j = 1; j <= cols; j++) {
                if (type == "int") {
                    sign = (int(rand() * 2) == 0) ? 1 : -1
                    val  = sign * int(rand() * 100)
                } else {
                    prec     = int(rand() * 10) + 1     # 1..10 decimal digits
                    category = int(rand() * 3)           # 0=positive, 1=negative, 2=fractional
                    if (category == 0)
                        val = sprintf("%.*f", prec, rand() * 10000 + 1)
                    else if (category == 1)
                        val = sprintf("%.*f", prec, -(rand() * 10000 + 1))
                    else
                        val = sprintf("%.*f", prec, rand())
                }
                line = (j == 1) ? val : line "," val
            }
            print line
        }
    }'
}

# -------- 4. Output: file if requested, otherwise stdout --------
if [[ -n "$out" ]]; then
    if [[ ! -f "$out" ]]; then
        touch "$out"
    fi
    generate > "$out"
    echo "Written CSV ${rows}x${cols} (${type}) to: $out" >&2
else
    generate
fi
