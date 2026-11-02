#!/bin/sh
# tr.sh NAME : round 3 + first round-4 traces
cd $(dirname $0); sh ../s123/dump.sh v/$1.c dd/$1 >/dev/null 2>&1; grep "^Trace" dd/$1/mc.bbro | grep -v STC | grep "round [34]" | head -${2:-8} | sed 's/Trace [0-9]* (round \([34]\)):/r\1/' | tr '\n' '|'; echo
