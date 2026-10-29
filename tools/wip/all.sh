#!/bin/sh
# fncmp every function of a draft: sh tools/wip/all.sh tools/wip/build.c fn1 fn2 ... [-- flags]
f=$1; shift
fns=; while [ $# -gt 0 ] && [ "$1" != -- ]; do fns="$fns $1"; shift; done
[ "$1" = -- ] && shift
for n in $fns; do
  r=$(FNCMP_LITERALS=1 python tools/re/fncmp.py "$f" "$n" "$@" 2>&1)
  if [ "$r" = MATCH ]; then echo "$n MATCH"; else echo "$n $(echo "$r" | grep -c '^[-+][^-+]')"; fi
done
