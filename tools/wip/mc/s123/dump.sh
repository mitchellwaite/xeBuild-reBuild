#!/bin/sh
# dump.sh SRC.c OUTDIR : dce(-blocks) + bbro dumps for a non-profiled variant
R=/c/Users/Win11VM/Documents/GitHub/xebuildBugFix
export PATH=$R/tools/toolchain-4745/mingw32/bin:$R/tools/toolchain-4745/bin:$PATH
S=$(cd $(dirname $1); pwd)/$(basename $1); mkdir -p $2; cd $2; rm -f *.c.27*
gcc -S -O3 -fno-toplevel-reorder -fno-ipa-profile -fno-reorder-functions --param builtin-expect-probability=50 -I$R/src $S -o x.s -fdump-rtl-cprop_hardreg-blocks-details -fdump-rtl-bbro-details
for k in cprop_hardreg bbro; do F=$(ls *.c.*.$k | head -1); n=$(grep -n "^;; Function mode_client" $F | cut -d: -f1); tail -n +$n $F > mc.$k; done
