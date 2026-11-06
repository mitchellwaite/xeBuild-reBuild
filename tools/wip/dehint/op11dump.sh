#!/bin/sh
# Attempt 11: tree dumps for an options.c variant (parseOption's tail).
# sh tools/wip/dehint/op11dump.sh <file.c> <outdir> [extra -fdump flags]
set -e
R=$(cd "$(dirname "$0")/../../.." && pwd)
src=$1; out=$2; shift 2
mkdir -p "$out"
PATH="$R/tools/toolchain-4745/mingw32/bin:$PATH"
{ printf '#line 1 "options.c"\n'; cat "$src"; } > "$out/o.c"
cd "$out"
gcc -c -O3 --param builtin-expect-probability=83 -I"$R/src" o.c -o o.o \
  -fdump-tree-profile_estimate -fdump-tree-vrp1-details -fdump-tree-optimized-blocks \
  -fdump-tree-dom2-details -fdump-tree-vrp2-details "$@"
