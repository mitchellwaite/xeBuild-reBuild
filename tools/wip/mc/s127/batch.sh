#!/bin/sh
# batch.sh LISTFILE : each line "NAME EDITS..." (b18-based, gen0.py); runs 4 parallel, then tr
cd $(dirname $0)
cat $1 | xargs -P4 -L1 sh -c 'sh run0.sh "$0" "$@" >/dev/null; echo "$0 $(grep "^$0 " res.txt | tail -1 | cut -d" " -f2) $(sh tr.sh $0 6)"'
