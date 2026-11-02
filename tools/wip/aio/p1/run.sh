#!/bin/sh
# run.sh SRC.c TAG: -dA asm + bbro/cprop/align dumps for SRC.c under build/v/aio_p1/TAG, then lab.txt, trl.txt, ev counts. GFL overrides flags.
R=/c/Users/Win11VM/Documents/GitHub/xebuildBugFix
A=$R/tools/wip/aio/p1

TC=$R/tools/toolchain-4745/mingw32/bin
FL="${GFL:--O3 --param builtin-expect-probability=83 -fno-ipa-profile -fno-reorder-functions}"
D=$R/build/v/aio_p1/$2
mkdir -p $D
cp "$1" $D/a.c
cd $D || exit 1
rm -f a.c.*r.* a.c.*t.*
PATH="$TC:$PATH" gcc -S -masm=intel -dA $FL $GX -fno-asynchronous-unwind-tables -I "$R/src" a.c -o o.s \
  -fdump-tree-profile_estimate-blocks-details -fdump-rtl-bbro-details -fdump-rtl-cprop_hardreg-blocks-details -fdump-rtl-alignments 2>err.txt || { cat err.txt; echo compile failed; exit 1; }
awk '/^;; Function applyIniOptions/,/^;; Function parseRawPatch/' a.c.274r.bbro > aio.bbro
cd $A
python lab.py $D/o.s | grep -v '^\* -:\.  *$' > $D/lab.txt
python trl.py $D > $D/trl.txt
$TC/as.exe --32 $D/o.s -o $D/o.o 2>/dev/null
$TC/objdump.exe -d -M intel --no-show-raw-insn $D/o.o | awk '/<_applyIniOptions>:/,/<_parseRawPatch>:/' > $D/ours.dis
python discmp.py ../orig.dis $D/ours.dis > $D/al.txt
lab=$(grep -c '^\*' $D/lab.txt)
echo "lab $lab align-diffs $(($(wc -l < $D/al.txt) - 1))"
