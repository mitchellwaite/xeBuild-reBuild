#!/bin/sh
# bi.sh X.c : bbinfo of mode_client
R=/c/Users/Win11VM/Documents/GitHub/xebuildBugFix
export PATH=$R/tools/toolchain-4745/mingw32/bin:$PATH
D=$(dirname $1)/dmp_$(basename $1 .c); mkdir -p $D; cd $D
gcc -S -I$R/src -O3 -fno-toplevel-reorder -fno-ipa-profile -fno-reorder-functions --param builtin-expect-probability=50 -fdump-rtl-bbro-details $1 -o x.s
F=$(ls *.bbro); n=$(grep -n "^;; Function mode_client" $F | cut -d: -f1); tail -n +$n $F > mc.bbro; rm $F
python $R/tools/wip/mc/s101/bbinfo2.py mc.bbro
