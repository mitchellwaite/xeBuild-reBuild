#!/bin/sh
# dumpall.sh SLOTDIR : full rtl/tree dumps of the profiled compile (dumps land in SLOTDIR, as fdorun9)
R="$(pwd)"; D="$R/$1"; B="$R/tools/toolchain-4745/mingw32/bin"; export PATH="$B:$PATH"
M="$(cygpath -w "$(dirname "$D")")\m.c"
cd "$D" && gcc -S -masm=intel -O3 -fno-toplevel-reorder -fno-ipa-profile -fno-reorder-functions -fno-asynchronous-unwind-tables --param builtin-expect-probability=50 -fbranch-probabilities -fprofile-dir="$(cygpath -w "$D")" -fdump-rtl-all-blocks -fdump-tree-all -I "$(cygpath -w "$R/wip/app")" "$M" -o - > all.s
