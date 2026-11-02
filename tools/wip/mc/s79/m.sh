#!/bin/sh
# m.sh SRC.c : fncmp, sig2 count, and dd order summary
n=$(basename $1 .c)
c=$(sh f.sh $1); sh ours.sh $1 o_$n.txt; s=$(python sig2.py origs.txt o_$n.txt | grep -c '^[-+]')
echo "$n fncmp=$c sig2=$s"
sh dd.sh $1 | sed 's/\[T[^]]*\] //g' | cut -c1-600
