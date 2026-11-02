#!/bin/sh
# r.sh NAME BASE old new ... : variant + fncmp/sig2 + tail order
n=$1; shift; b=$1; shift
python mk.py $b $n.c "$@" || exit 1
c=$(sh f.sh $n.c); sh ours.sh $n.c o_$n.txt 2>/dev/null; s=$(python sig2.py origs.txt o_$n.txt | grep -c '^[-+]')
o=$(sh dd.sh $n.c >/dev/null; python tail.py d/$n/order.txt)
echo "$n fncmp=$c sig2=$s | $o"
