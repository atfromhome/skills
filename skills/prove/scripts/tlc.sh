#!/usr/bin/env bash
# prove: run plain TLC on a spec and summarise the verdict.
# Usage: tlc.sh Spec.tla [-c Spec.cfg] [-o OUTDIR] [--dot] [--workers N] [--depth N]
# Exit: 0 = all checks pass, 1 = a rule is violated (invariant/property/deadlock), 2 = tool or model error.
set -u
SPEC=""; CFG=""; OUT=""; DOT=0; WORKERS=1; EXTRA=()
while [ $# -gt 0 ]; do
  case "$1" in
    -c|--config) CFG="$2"; shift 2;;
    -o|--out) OUT="$2"; shift 2;;
    --dot) DOT=1; shift;;
    --workers) WORKERS="$2"; shift 2;;
    --depth) EXTRA+=(-depth "$2"); shift 2;;
    *) SPEC="$1"; shift;;
  esac
done
[ -n "$SPEC" ] || { echo "usage: tlc.sh Spec.tla [-c Spec.cfg] [-o OUTDIR] [--dot]"; exit 2; }
[ -f "$SPEC" ] || { echo "spec not found: $SPEC"; exit 2; }
base="$(basename "$SPEC" .tla)"; dir="$(cd "$(dirname "$SPEC")" && pwd)"
[ -n "$CFG" ] || CFG="$dir/$base.cfg"
[ -f "$CFG" ] || { echo "config not found: $CFG"; exit 2; }
OUT="${OUT:-$dir/tlc-out}"; mkdir -p "$OUT"; OUT="$(cd "$OUT" && pwd)"
JAVA="${JAVA:-java}"
CACHE="${XDG_CACHE_HOME:-$HOME/.cache}/flow"
JAR="${TLA2TOOLS_JAR:-$CACHE/tla2tools.jar}"
command -v "$JAVA" >/dev/null 2>&1 || { echo "BLOCKED: java not found (run check_toolchain.sh)"; exit 2; }
[ -f "$JAR" ] || { echo "BLOCKED: tla2tools.jar not found at $JAR (set TLA2TOOLS_JAR)"; exit 2; }
CFGABS="$(cd "$(dirname "$CFG")" && pwd)/$(basename "$CFG")"
DUMP=()
[ "$DOT" = 1 ] && DUMP=(-dump dot,actionlabels "$OUT/states")
( cd "$dir" && "$JAVA" -XX:+UseParallelGC -cp "$JAR" tlc2.TLC -workers "$WORKERS" -cleanup \
    -metadir "$OUT/meta" -config "$CFGABS" "${DUMP[@]}" "${EXTRA[@]}" "$base.tla" ) > "$OUT/tlc.out" 2>&1
code=$?
ver=$(grep -m1 -oE 'TLC2 Version [^ ]+( of [^)]*\))?' "$OUT/tlc.out" || echo "TLC version unknown")
states=$(grep -m1 -oE '[0-9,]+ distinct states found' "$OUT/tlc.out" | tr -d , | grep -oE '^[0-9]+' || echo "?")
if grep -q "Model checking completed. No error has been found" "$OUT/tlc.out"; then
  verdict="PASS"; rule=""
elif grep -qE "^Error: Invariant .* is violated" "$OUT/tlc.out"; then
  verdict="VIOLATION"; rule=$(grep -m1 -oE "Invariant [A-Za-z0-9_]+ is violated" "$OUT/tlc.out" | awk '{print $2}')
elif grep -qE "^Error: Temporal properties were violated|^Error: Action property" "$OUT/tlc.out"; then
  verdict="VIOLATION"; rule="temporal property"
elif grep -q "^Error: Deadlock reached" "$OUT/tlc.out"; then
  verdict="VIOLATION"; rule="Deadlock"
else
  verdict="ERROR"; rule=""
fi
[ -f "$OUT/states.dot" ] && dotf="$OUT/states.dot" || dotf=""
printf '{"verdict":"%s","rule":"%s","distinct_states":"%s","tlc":"%s","exit":%s,"spec":"%s","config":"%s","tlc_out":"%s","dot":"%s"}\n' \
  "$verdict" "$rule" "$states" "$ver" "$code" "$SPEC" "$CFG" "$OUT/tlc.out" "$dotf" > "$OUT/summary.json"
cat "$OUT/summary.json"
case "$verdict" in
  PASS) exit 0;;
  VIOLATION) echo "--- counterexample (from tlc.out) ---"; sed -n '/^Error:/,/^[0-9]* states generated/p' "$OUT/tlc.out" | head -120; exit 1;;
  *) echo "--- TLC output tail ---"; tail -40 "$OUT/tlc.out"; exit 2;;
esac
