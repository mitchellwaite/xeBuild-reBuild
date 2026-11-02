#!/bin/sh
# run2.sh OUT NAME... : fncmp + nblocks + inv + tail order (no sig2)
out=$1; shift
for n in "$@"; do
c=$(sh f.sh $n.c); sh dd.sh $n.c >/dev/null 2>&1; nb=$(wc -l < d/$n/order.txt); o=$(python tail.py d/$n/order.txt | cut -d' ' -f1-22); iv=$(python inv.py $n)
echo "$n fncmp=$c nb=$nb $iv | $o" | tee -a $out
done
