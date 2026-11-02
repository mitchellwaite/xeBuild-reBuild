#!/bin/sh
# f.sh SRC.c : fncmp count + diff to SRC.d
R=/c/Users/Win11VM/Documents/GitHub/xebuildBugFix
export PATH=$R/tools/toolchain-4745/bin:$PATH
P=$(cd $(dirname $1); pwd)/$(basename $1 .c); cd $R;  FNCMP_LITERALS=1 python tools/re/fncmp.py "$P.c" mode_client -I$R/src -O3 -fno-toplevel-reorder -fno-ipa-profile -fno-reorder-functions --param builtin-expect-probability=50 $FX > "$P.d" 2>&1
if grep -q "error:" "$P.d"; then echo 9999; else grep -c "^[-+][^-+]" "$P.d"; fi
