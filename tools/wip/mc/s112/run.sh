#!/bin/sh
# run.sh v1.c v2.c ... : f2 + round-4 keys
S=/c/Users/Win11VM/Documents/GitHub/xebuildBugFix/tools/wip/mc/s112
for f in "$@"; do (b=$(basename $f .c); cp $S/b0.ref $S/$b.ref 2>/dev/null; r=$(sh $S/../s111/ev.sh $S/$b.c); k=$(cd $S; python keys.py dmp_$b 2>&1 | cut -c1-330); echo "$r | $k" >> $S/log.txt; echo "$r | $k") & done; wait
