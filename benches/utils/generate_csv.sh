#!/usr/bin/env bash
# Generates a CSV of random numbers.
# Usage: ./gen_random_csv.sh row=<int> col=<int> type=<int|double> [out=<file>]

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
Usage: $0 row=<int> col=<int> type=<int|double> [out=<file>]

  row    number of rows    (positive integer)
  col    number of columns (positive integer)
  type   int    -> integers in [0, 100)
         double -> reals    in [0, 1)  with 6 decimal digits
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

[[ "$type" == "int" || "$type" == "double" ]] \
    || { echo "Error: type must be 'int' or 'double', got '$type'" >&2; exit 2; }

# -------- 3. Generation (all inside awk, single process) --------
generate() {
    awk -v rows="$rows" -v cols="$cols" -v type="$type" '
    BEGIN {
        srand()                                 # seed = time(NULL); without this, awk would always use the same seed
        for (i = 1; i <= rows; i++) {
            line = ""
            for (j = 1; j <= cols; j++) {
                if (type == "int") {
                    val = int(rand() * 100)     # rand() in [0,1)  ->  int*100 in [0,99]
                } else {
                    val = sprintf("%.6f", rand())
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
