#!/usr/bin/env bash
# Genera un CSV di numeri casuali.
# Uso: ./gen_random_csv.sh row=<int> col=<int> type=<int|double> [out=<file>]

set -euo pipefail

# -------- 1. Parsing argomenti in formato key=value --------
rows="" cols="" type="" out=""

for arg in "$@"; do
    case "$arg" in
        row=*)  rows="${arg#row=}"  ;;
        col=*)  cols="${arg#col=}"  ;;
        type=*) type="${arg#type=}" ;;
        out=*)  out="${arg#out=}"   ;;
        -h|--help)
            cat <<EOF
Uso: $0 row=<int> col=<int> type=<int|double> [out=<file>]

  row    numero di righe   (intero positivo)
  col    numero di colonne (intero positivo)
  type   int    -> interi in [0, 100)
         double -> reali  in [0, 1)  con 6 cifre decimali
  out    file di output (default: stdout)
EOF
            exit 0
            ;;
        *)
            echo "Errore: argomento non riconosciuto '$arg'" >&2
            exit 2
            ;;
    esac
done

# -------- 2. Validazione --------
[[ -n "$rows" && -n "$cols" && -n "$type" ]] \
    || { echo "Errore: row, col e type sono obbligatori. Usa --help." >&2; exit 2; }

[[ "$rows" =~ ^[1-9][0-9]*$ ]] \
    || { echo "Errore: row deve essere un intero positivo (no zero, no segno), ricevuto '$rows'" >&2; exit 2; }

[[ "$cols" =~ ^[1-9][0-9]*$ ]] \
    || { echo "Errore: col deve essere un intero positivo, ricevuto '$cols'" >&2; exit 2; }

[[ "$type" == "int" || "$type" == "double" ]] \
    || { echo "Errore: type deve essere 'int' o 'double', ricevuto '$type'" >&2; exit 2; }

# -------- 3. Generazione (tutto dentro awk, in un solo processo) --------
generate() {
    awk -v rows="$rows" -v cols="$cols" -v type="$type" '
    BEGIN {
        srand()                                 # seed = time(NULL); senza, awk userebbe sempre lo stesso seed
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

# -------- 4. Output: file se richiesto, altrimenti stdout --------
if [[ -n "$out" ]]; then
    generate > "$out"
    echo "Scritto CSV ${rows}x${cols} (${type}) in: $out" >&2
else
    generate
fi
