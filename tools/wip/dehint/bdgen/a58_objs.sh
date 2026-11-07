#!/bin/sh
# Attempt 58: compile every app object (not crypto) with build.sh's flags and an include overlay
# ahead of src, and name those that differ from build/obj (the last matching build).
# sh tools/wip/dehint/bdgen/a58_objs.sh <overlay dir> [build.c variant]
TC=$PWD/tools/toolchain-4745/mingw32/bin
PATH="$TC:$PATH"
ov=$1
bc=${2:-src/build.c}
out=build/bd/a58/objs
mkdir -p $out
for f in src/*.c; do
  b=$(basename $f .c)
  src=$f
  [ $b = build ] && src=$bc
  fl="-O3"
  case $b in
    options) fl="-O3 --param builtin-expect-probability=83" ;;
    build) fl="-O3 --param builtin-expect-probability=99" ;;
    globals) fl="-O3 -fno-common -fno-toplevel-reorder" ;;
  esac
  { printf '#line 1 "%s.c"\n' $b; cat $src; } | gcc -c $fl -I"$ov" -Isrc -x c - -o $out/$b.o || echo "ERR $b"
  cmp -s $out/$b.o build/obj/$b.o || echo "DIFF $b"
done
echo done
