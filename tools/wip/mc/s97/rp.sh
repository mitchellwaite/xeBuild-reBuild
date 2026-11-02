#!/bin/sh
# rp.sh NAME BASE.c PREFIX PERM
n=$1; b=$2
python pf.py $b $n.c "$3" "$4" || exit 1
c=$(sh f.sh $n.c); sh ours.sh $n.c o_$n.txt 2>/dev/null; s=$(python sig2.py origs.txt o_$n.txt | grep -c '^[-+]')
sh dd.sh $n.c >/dev/null 2>&1; iv=$(python inv.py $n)
echo "$n $3 $4 fncmp=$c sig2=$s $iv" | tee -a log.txt
