#!/bin/sh
# Attempt 70: dump one build.c variant with -fdump-tree-all-vops? no: plain -fdump-tree-all into build/bd/a70/<name>/
# sh tools/wip/dehint/bdgen/a70_dump.sh <variant.c> <name> [extra gcc flags]
R=$(cd "$(dirname "$0")/../../../.." && pwd)
TC="$R/tools/toolchain-4745/mingw32/bin"
PATH="$TC:$PATH"
src=$1; name=$2; shift 2
out="$R/build/bd/a70/$name"
mkdir -p "$out"
cp "$src" "$out/build.c"
cd "$out" && { printf '#line 1 "build.c"\n'; cat build.c; } > in.c && gcc -c -O3 -I"$R/src" -fdump-tree-all "$@" in.c -o o.o
