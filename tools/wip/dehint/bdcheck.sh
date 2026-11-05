#!/bin/sh
# sh tools/wip/dehint/bdcheck.sh file.c fn [extra flags]: fn's blocks from the .optimized dump (freq, what they end in)
f=$1; fn=$2; shift 2
d=build/bd/dump_$$; mkdir -p $d
R=$PWD
PATH="$R/tools/toolchain-4745/mingw32/bin:$PATH"
( cd $d && { printf '#line 1 "build.c"\n'; cat "$R/$f"; } | gcc -c -O3 --param builtin-expect-probability=98 -I"$R/src" -fdump-tree-optimized-blocks-details "$@" -x c - -o o.o )
awk -v fn="$fn" '$1==";;" && $2=="Function" && $3==fn {p=1; next} $1==";;" && $2=="Function" {p=0} p' $d/*.optimized | grep -E 'basic block|BLOCK|log_printf|crc32|return|if .' | cut -c1-110
rm -f $d/*; rmdir $d
