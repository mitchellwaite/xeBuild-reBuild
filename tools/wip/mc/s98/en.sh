#!/bin/sh
# en.sh TAG PREFIX perm : pf + measure
t=$1; python pf.py base.c $t.c "$2" $3 2>/dev/null || exit 1
c=$(sh f.sh $t.c); sh ours.sh $t.c o_$t.txt 2>/dev/null; s=$(python sig2.py origs.txt o_$t.txt | grep -c '^[-+]')
echo "$t [$2 $3] fncmp=$c sig2=$s" | tee -a log.txt
