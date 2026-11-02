#!/bin/sh
# s.sh SRC TAG: brief (ev counts, cm, first label diffs, head of traces)
cd /c/Users/Win11VM/Documents/GitHub/xebuildBugFix
sh tools/wip/aio/p1/t.sh $1 $2 2>&1 | tail -3 | cut -c1-300; [ -f build/v/aio_p1/$2/o.o ] || exit 1; python tools/wip/aio/p1/cm.py $2 | head -${3:-14}; grep -c '^\*' build/v/aio_p1/$2/lab.txt
