#!/bin/bash
# Disassemble an exe into GTIRB and print the address-annotated GNU listing
# that tools/re/ddfix.py consumes.  Run inside WSL from the repo root:
#   wsl -d Ubuntu -- bash tools/ddisasm/disasm.sh xeBuild.exe build
set -e
EXE=$1; OUT=${2:-build}
. "$(dirname "$0")/env.sh"
mkdir -p "$OUT"
ddisasm "$EXE" --ir "$OUT/xeBuild.gtirb" -j "$(nproc)" > "$OUT/ddisasm.log" 2>&1
# PE output only supports MASM syntax; "raw" + intel gives GNU as syntax.
gtirb-pprinter --ir "$OUT/xeBuild.gtirb" --format raw --syntax intel --keep-all \
  --listing-mode debug --asm "$OUT/xeBuild.dbg.s" 2>&1 | grep -v '^\[INFO\]' || true
echo "wrote $OUT/xeBuild.dbg.s"
