#!/bin/sh
# ev.sh NAME : fncmp, inv, hot-diff vs b0
n=$1; c=$(sh f.sh $n.c); sh dd.sh $n.c >/dev/null; iv=$(python inv.py $n); python hs.py $n > d/$n/hs.txt
h=$(diff d/b0/hs.txt d/$n/hs.txt | grep -c '^[<>]'); echo "$n fncmp=$c $iv hot=$h" | tee -a log.txt
