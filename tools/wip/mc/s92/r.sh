#!/bin/sh
# r.sh NAME BASE old new ... : variant + fncmp/sig2/inversions + tail order
n=$1; shift; b=$1; shift
python mk.py $b $n.c "$@" || exit 1
c=$(sh f.sh $n.c); sh ours.sh $n.c o_$n.txt 2>/dev/null; s=$(python sig2.py origs.txt o_$n.txt | grep -c '^[-+]')
sh dd.sh $n.c >/dev/null; o=$(python tail.py d/$n/order.txt | cut -d' ' -f1-22); iv=$(python inv.py $n)
echo "$n fncmp=$c sig2=$s $iv | $o" | tee -a log.txt
