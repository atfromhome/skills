#!/usr/bin/env bash
# prove: report what is available for model checking. Never installs anything
# unless --fetch-tla2tools is passed (downloads tla2tools.jar into the user cache only).
# Exit: 0 = TLC runnable, 2 = TLC not runnable (gate must be reported as blocked).
set -u
FETCH=0
[ "${1:-}" = "--fetch-tla2tools" ] && FETCH=1
CACHE="${XDG_CACHE_HOME:-$HOME/.cache}/vflow"
ok=1

echo "== Java"
JAVA="${JAVA:-java}"
if command -v "$JAVA" >/dev/null 2>&1; then
  ver=$("$JAVA" -version 2>&1 | head -1)
  major=$("$JAVA" -version 2>&1 | head -1 | sed -E 's/.*version "([0-9]+)(\.[0-9]+)*.*/\1/')
  [ "$major" = "1" ] && major=$("$JAVA" -version 2>&1 | head -1 | sed -E 's/.*version "1\.([0-9]+).*/\1/')
  echo "found: $ver"
  if [ "${major:-0}" -lt 11 ] 2>/dev/null; then echo "PROBLEM: TLC needs Java 11+ (17+ recommended)"; ok=0; fi
else
  echo "PROBLEM: no java on PATH (set JAVA=/path/to/java). Install a JDK/JRE 17+ (e.g. Temurin, or 'mise use java@21')."
  ok=0
fi

echo "== tla2tools.jar (TLC)"
JAR="${TLA2TOOLS_JAR:-}"
if [ -z "$JAR" ]; then
  for c in "$CACHE/tla2tools.jar" "$HOME/.local/share/tla2tools.jar" "/usr/local/lib/tla2tools.jar" "/opt/tla/tla2tools.jar" "./tla2tools.jar"; do
    [ -f "$c" ] && JAR="$c" && break
  done
fi
if [ -z "$JAR" ] && [ "$FETCH" = 1 ]; then
  mkdir -p "$CACHE" && curl -fsSL -o "$CACHE/tla2tools.jar" \
    https://github.com/tlaplus/tlaplus/releases/latest/download/tla2tools.jar && JAR="$CACHE/tla2tools.jar"
fi
if [ -n "$JAR" ] && [ -f "$JAR" ]; then
  echo "found: $JAR"
  if [ "$ok" = 1 ]; then "$JAVA" -cp "$JAR" tlc2.TLC -version 2>&1 | grep -m1 -o "TLC2 Version.*" | sed 's/^/version: /'; fi
else
  echo "PROBLEM: tla2tools.jar not found. Set TLA2TOOLS_JAR, or rerun with --fetch-tla2tools (downloads to $CACHE)."
  ok=0
fi

echo "== Optional: pstack statechart (richer charts + shortest bug paths)"
if command -v node >/dev/null 2>&1; then
  nv=$(node --version | sed 's/^v//'); echo "node: v$nv (pstack statechart needs >= 22.18 to run TypeScript directly)"
  IFS=. read -r a b _ <<<"$nv"
  if [ "$a" -lt 22 ] || { [ "$a" -eq 22 ] && [ "$b" -lt 18 ]; }; then echo "note: node too old for pstack statechart; vflow fallback will be used"; fi
else
  echo "note: no node; vflow fallback (scripts/dot2mermaid.py) will be used"
fi
found=""
for d in "$HOME/.cursor/plugins" "$HOME/.claude/plugins" "$HOME/.claude/skills" "$HOME/.agents/skills" "./.cursor" "./.claude" "./.agents"; do
  [ -d "$d" ] || continue
  f=$(find "$d" -path '*statechart/scripts/statechart' -type f 2>/dev/null | head -1)
  [ -n "$f" ] && found="$f" && break
done
[ -n "$found" ] && echo "pstack statechart: $found" || echo "pstack statechart: not found (optional)"
command -v mise >/dev/null 2>&1 && echo "mise: $(mise --version 2>/dev/null | head -1)" || echo "mise: not found (pstack statechart uses it to install Java/TLC on first run)"
command -v python3 >/dev/null 2>&1 && echo "python3: $(python3 --version 2>&1)" || echo "note: no python3; dot2mermaid.py fallback unavailable"

echo "== Verdict"
if [ "$ok" = 1 ]; then echo "TLC_READY=yes JAR=$JAR"; exit 0; else echo "TLC_READY=no  -> record the gate as BLOCKED with the problems above; do not skip it."; exit 2; fi
