#!/bin/sh
# run3.sh NAME OLD NEW [BASE]: literal replace in base, f2 + r3 traces
cd $(dirname $0)
python - "$2" "$3" ${4:-b18.c} a/$1.c <<'P'
import sys
s=open(sys.argv[3]).read(); assert sys.argv[1] in s, sys.argv[1]
open(sys.argv[4],'w',newline='\n').write(s.replace(sys.argv[1],sys.argv[2],1))
P
f=$(sh ../s101/f2.sh a/$1.c); sh ../s123/dump.sh a/$1.c dd_$1 >/dev/null 2>&1
echo "$1 $f $(grep 'round 3' dd_$1/mc.bbro | grep -v STC | sed 's/Trace [0-9]* (round 3)://' | tr '\n' '|')"
