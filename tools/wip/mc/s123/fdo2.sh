#!/bin/sh
# fdo.sh : profiled (matching) compile of src/mode_client.c with bbro dump -> pf/mc.bbro
R=/c/Users/Win11VM/Documents/GitHub/xebuildBugFix
TC=$R/tools/toolchain-4745/mingw32/bin
export PATH=$TC:$R/tools/toolchain-4745/bin:$PATH
S=$R/tools/wip/mc/s123; p=$S/pf; mkdir -p $p; pw=$(cd $p; pwd -W)
CF="-O3 -fno-toplevel-reorder -fno-ipa-profile -fno-reorder-functions --param builtin-expect-probability=50 -DBUILD_FDO --param align-loop-iterations=100"
ccp() { (cd $p && { printf '#line 1 "mode_client.c"\n'; cat $R/src/mode_client.c; } | gcc -S "$@" -I$R/src -x c - -o -); }
cd $R
ccp $CF -fprofile-arcs -ftest-coverage -fdump-tree-profile_estimate-blocks-details >/dev/null
python tools/re/gcda.py "$p/-.gcno" "$p/-.042t.profile_estimate" "$p/-.gcda" @src/mode_client.prof --only=mode_client,clientEraseBlock --threshold=64 --src=src/mode_client.c >/dev/null
ccp $CF -fbranch-probabilities -fprofile-dir="$pw" -fdump-rtl-bbro-details -fdump-rtl-cprop_hardreg-blocks-details > $p/x.s
for k in cprop_hardreg bbro; do F=$(ls $p/*.$k | grep -v "mc.$k$"); n=$(grep -n "^;; Function mode_client" $F | cut -d: -f1); tail -n +$n $F > $p/mc.$k; done
python $R/tools/wip/mc/s101/bbinfo2.py $p/mc.bbro > $p/bbinfo.txt
