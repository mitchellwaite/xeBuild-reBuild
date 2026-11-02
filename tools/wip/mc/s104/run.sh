#!/bin/sh
# run.sh X.c : f2 + round-4 pop order
H=/c/Users/Win11VM/Documents/GitHub/xebuildBugFix/tools/wip/mc
A=$(cd $(dirname $1); pwd)/$(basename $1); set -- $A; f=$(sh $H/s101/f2.sh $1); sh $H/s104/bi.sh $1 > /dev/null 2>&1
D=$(dirname $1)/dmp_$(basename $1 .c)
o=$(python $H/s86/r4sim.py $D/mc.bbro | tail -1)
echo "$(basename $1) f2=$f $o"
