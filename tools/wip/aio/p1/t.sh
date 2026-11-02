#!/bin/sh
# t.sh SRC.c TAG: ev counts + run.sh + brief
cd /c/Users/Win11VM/Documents/GitHub/xebuildBugFix
python tools/wip/aio/p1/ev.py "$1" -t ev_$2 2>&1 | tail -1 | cut -c1-200
sh tools/wip/aio/p1/run.sh "$1" $2
(cd tools/wip/aio/p1; python lay.py ../../../../build/v/aio_p1/$2/o.s)
