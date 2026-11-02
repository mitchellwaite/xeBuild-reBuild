#!/bin/sh
# run.sh NAME EDITS... : gen, f2, gimple freqs of -s/-keys blocks
cd $(dirname $0); R=/c/Users/Win11VM/Documents/GitHub/xebuildBugFix
python gen.py "$@" || exit 1
n=$1; f=$(sh ../s101/f2.sh v/$n.c)
export PATH=$R/tools/toolchain-4745/mingw32/bin:$R/tools/toolchain-4745/bin:$PATH
mkdir -p pe/$n; (cd pe/$n; rm -f *; gcc -S -O3 -fno-toplevel-reorder -fno-ipa-profile -fno-reorder-functions --param builtin-expect-probability=50 -I$R/src ../../v/$n.c -o x.s -fdump-tree-profile_estimate-details 2>/dev/null)
P=$(ls pe/$n/*profile_estimate); fr=$(python pf.py $P)
echo "$n f2=$f $fr" | tee -a res.txt
