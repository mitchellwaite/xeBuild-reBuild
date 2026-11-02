#!/bin/sh
# run1.sh NAME COND : build variant a/NAME.c from b18.c, print f2 + round-3 traces
cd $(dirname $0)
python mk.py ${BASE:-b18.c} a/$1.c "$2" || exit 1
f=$(sh ../s101/f2.sh a/$1.c); sh ../s123/dump.sh a/$1.c dd_$1 >/dev/null 2>&1
echo "$1 $f $(grep 'round 3' dd_$1/mc.bbro | grep -v STC | sed 's/Trace [0-9]* (round 3)://' | tr '\n' '|')"
