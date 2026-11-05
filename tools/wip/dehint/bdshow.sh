#!/bin/sh
# sh tools/wip/dehint/bdshow.sh a,b,c [fn]: the diff against the reference with those tricks off
out=build/bd/show_$$.c
python tools/wip/dehint/bdtricks.py show "$1" -o $out >/dev/null
python tools/wip/dehint/bdlib.py $out -v $2
rm -f $out
