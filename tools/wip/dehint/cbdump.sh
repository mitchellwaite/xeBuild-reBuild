#!/bin/sh
# sh tools/wip/dehint/cbdump.sh <file.c> <outdir> [gcc flags]: every tree and rtl dump of a draft (-O3), in <outdir>
root=$(cd "$(dirname "$0")/../../.." && pwd)
src=$(cd "$(dirname "$1")" && pwd)/$(basename "$1")
out=$2
shift 2
mkdir -p "$out"
cd "$out" || exit 1
PATH="$root/tools/toolchain-4745/mingw32/bin:$PATH"
gcc -S -masm=intel -fno-asynchronous-unwind-tables -O3 -I"$root/src" -fdump-tree-all -fdump-rtl-all-details "$@" "$src" -o out.s
