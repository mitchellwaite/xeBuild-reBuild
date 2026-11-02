#!/bin/sh
# sw.sh BASE TAG : retarget each rkE ork to each case
b=$1; g=$2; n=0
for i in 11 12 13 14 15 16 17 18 19 20 21 43 44 45 46 47 48 49 50 51; do
 for t in c1 c12 s5 c8 c10 cdef t4 t5 c3; do
  n=$((n+1)); sh r.sh ${g}_${i}_$t $b "ork$i: goto rkE;" "ork$i: goto $t;" >/dev/null 2>&1
  grep "^${g}_${i}_$t " log.txt | tail -1 | cut -c1-60
 done
done
