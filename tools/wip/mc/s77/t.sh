#!/bin/sh
# t.sh NAME base old new ... : make variant, print fncmp and cold sig
n=$1; shift; b=$1; shift
python v.py $b v_$n.c "$@" || exit 1
c=$(sh f.sh v_$n.c); echo "$n fncmp=$c"
