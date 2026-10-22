#!/bin/sh
R=$(cd "$(dirname "$0")/../.." && pwd -P)
# dumps.sh <dir>: FDO compile of <dir>/a.c with -dA, bbro and cprop_hardreg dumps (uses the current -.gcda)
cd "$1"
PATH="$R/tools/toolchain-4745/mingw32/bin:$PATH" gcc -S -masm=intel -dA -fno-ipa-profile -fno-reorder-functions -O3 -fno-asynchronous-unwind-tables --param builtin-expect-probability=83 -fbranch-probabilities -fprofile-dir="$(pwd -W)" "$(pwd -W)/a.c" -o - -fdump-rtl-bbro-details -fdump-rtl-cprop_hardreg-blocks-details -fdump-rtl-alignments > o.s 2>/dev/null
awk '/^;; Function applyIniOptions/,/^;; Function parseRawPatch/' a.c.274r.bbro > aio.bbro
