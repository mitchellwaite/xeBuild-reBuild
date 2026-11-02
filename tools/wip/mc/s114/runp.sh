#!/bin/sh
# runp.sh base seedlo seedhi : perturb + f2, print seed f2
D=$(cd $(dirname $0); pwd); B=$1
for s in $(seq $2 $3); do o=$D/p/$(basename $B .c)_$s.c; python $D/pert.py $B $o $s; cp $D/b0.ref ${o%.c}.ref; echo "$s $(sh $D/../s101/f2.sh $o)"; done
