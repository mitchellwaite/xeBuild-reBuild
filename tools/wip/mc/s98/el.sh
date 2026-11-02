#!/bin/sh
# el.sh TAG BASE SUBSTR K perm
t=$1; python lp.py $2 $t.c "$3" $4 $5 2>/dev/null || exit 1
c=$(sh f.sh $t.c); sh dd.sh $t.c >/dev/null 2>&1; iv=$(python inv.py $t)
echo "$t [$2 $3/$4 $5] fncmp=$c $iv" | tee -a log.txt
