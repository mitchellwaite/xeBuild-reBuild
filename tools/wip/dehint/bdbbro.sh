#!/bin/sh
# sh tools/wip/dehint/bdbbro.sh file.c fn [extra flags]: fn's traces from the bbro dump (rounds, blocks, frequencies)
# Keeps the dump text of fn in build/bd/bbro_fn.txt.
f=$1; fn=$2; shift 2
d=build/bd/dump_$$; mkdir -p $d
R=$PWD
PATH="$R/tools/toolchain-4745/mingw32/bin:$PATH"
( cd $d && { printf '#line 1 "build.c"\n'; cat "$R/$f"; } | gcc -c -O3 --param builtin-expect-probability=98 -I"$R/src" -fdump-rtl-bbro-details "$@" -x c - -o o.o )
awk -v fn="$fn" '/^;; Function /{p=($3==fn)} p' $d/*.bbro > build/bd/bbro_$fn.txt
grep -nE '^Trace|^Round|^Basic block|^Getting bb|^Connection|^Final order|^[0-9 ]+$' build/bd/bbro_$fn.txt | head -${BDLINES:-80}
rm -f $d/*; rmdir $d
