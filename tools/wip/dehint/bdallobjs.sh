TC=$PWD/tools/toolchain-4745/mingw32/bin
PATH="$TC:$PATH"
n=$1
for f in src/*.c; do
 b=$(basename $f .c)
 case $b in build) ;; esac
 fl="-O3"
 case $b in options) fl="-O3 --param builtin-expect-probability=83";; build) fl="-O3 --param builtin-expect-probability=98";; mode_client) fl="-O3 --param builtin-expect-probability=50";; globals) fl="-O3 -fno-common -fno-toplevel-reorder";; esac
 { printf '#line 1 "%s.c"\n' $b; cat $f; } | gcc -c $fl -Isrc -x c - -o build/bd/tmp_$b.o
 if cmp -s build/bd/tmp_$b.o build/obj/$b.o; then :; else echo "$n DIFF $b"; fi
 rm -f build/bd/tmp_$b.o
done
echo done $n
