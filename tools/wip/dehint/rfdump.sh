#!/bin/sh
# rfdump.sh <dir> <src.c> [flags]: compile with all tree dumps (and flags, e.g. -fdump-rtl-ira -fdump-rtl-bbro-details) into dir.
# Then: python tools/wip/dehint/rfcfg.py <dir> vrp1 dom2 dom3 optimized   (compact CFG + registered threads per pass)
#       python tools/wip/dehint/rffn.py <dump> [fn]                       (one function out of a dump)
ROOT=$(cd "$(dirname "$0")/../../.." && pwd)
export PATH=$ROOT/tools/toolchain-4745/mingw32/bin:$PATH
d=$1; s=$2; shift 2
mkdir -p "$d"; cp "$s" "$d/a.c"; cd "$d" || exit 1
gcc -S -masm=intel -O3 -I"$ROOT/src" -fno-asynchronous-unwind-tables -fdump-tree-all-details -fdump-tree-all-blocks "$@" a.c -o a.s
