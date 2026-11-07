#!/bin/sh
# sh tools/wip/dehint/bddump.sh file.c fn pass[,pass..] [extra gcc flags]: fn's text of each dump, in build/bd/dump/<fn>.<pass>
# pass: rtl names (ira, reload, sched2, jump2, bbro, expand, ..) or tree names as t-optimized, t-pre, t-profile_estimate, ..
f=$1; fn=$2; passes=$3; shift 3
R=$PWD
PATH="$R/tools/toolchain-4745/mingw32/bin:$PATH"
d=build/bd/dump_$$; mkdir -p $d build/bd/dump
fl=
for p in $(echo "$passes" | tr , ' '); do
  case $p in
    t-*) fl="$fl -fdump-tree-${p#t-}-details-blocks" ;;
    i-*) fl="$fl -fdump-ipa-${p#i-}-details" ;;
    *)   fl="$fl -fdump-rtl-$p-details" ;;
  esac
done
( cd $d && { printf '#line 1 "build.c"\n'; cat "$R/$f"; } | gcc -c -O3 --param builtin-expect-probability=${BDP:-98} -I"$R/src" $fl "$@" -x c - -o o.o )
for p in $(echo "$passes" | tr , ' '); do
  n=${p#t-}; n=${n#i-}
  for x in $d/*.$n; do
    [ -f "$x" ] && awk -v fn="$fn" '/^;; Function /{p=($3==fn)} p' "$x" > build/bd/dump/$fn.$n
  done
done
rm -f $d/*; rmdir $d
