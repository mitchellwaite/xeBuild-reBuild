#!/bin/sh
# rv.sh NAME BASE.c [pat n repl]...
n=$1; shift; b=$1; shift
python gen.py $b $n.c "$@" || exit 1
c=$(sh f.sh $n.c); sh ours.sh $n.c o_$n.txt 2>/dev/null; s=$(python sig2.py origs.txt o_$n.txt | grep -c '^[-+]')
sh dd.sh $n.c >/dev/null 2>&1; iv=$(python inv.py $n)
echo "$n fncmp=$c sig2=$s $iv" | tee -a log.txt
