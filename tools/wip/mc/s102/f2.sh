#!/bin/sh
# f2.sh SRC.c : minimal-diff count (GNU diff --minimal) of normalized asm vs original
R=/c/Users/Win11VM/Documents/GitHub/xebuildBugFix
export PATH=$R/tools/toolchain-4745/bin:$PATH
P=$(cd $(dirname $1); pwd)/$(basename $1 .c); cd $R; FNCMP_DUMP="$P" FNCMP_LITERALS=1 python tools/wip/mc/s102/fncmp2.py "$P.c" mode_client -I$R/src -O3 -fno-toplevel-reorder -fno-ipa-profile -fno-reorder-functions --param builtin-expect-probability=50 $FX > "$P.d" 2>&1
if grep -q "error:" "$P.d"; then echo 9999; else diff --minimal "$P.ref" "$P.mine" | grep -c "^[<>]"; fi
