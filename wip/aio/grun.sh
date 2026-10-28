#!/bin/sh
# grun.sh <dir>: applyIniOptions in <dir>/a.c with gcc's guessed profile (no
# .gcda): -dA asm and dumps like dumps.sh, then lab.txt, trl.txt, al.txt and
# the blk/fncmp/label-mismatch/padding counts.  GFL overrides the flags.
R=$(cd "$(dirname "$0")/../.." && pwd -P)
S=$(cd "$(dirname "$0")" && pwd -P)
TC=$R/tools/toolchain-4745/mingw32/bin
FL="${GFL:--O3 --param builtin-expect-probability=83 -fno-ipa-profile -fno-reorder-functions}"
cd "$S/$1" || exit 1
rm -f a.c.*r.* a.c.*t.*
PATH="$TC:$PATH" gcc -S -masm=intel -dA $FL -fno-asynchronous-unwind-tables -I "$R/src" "$(pwd -W)/a.c" -o o.s \
  -fdump-rtl-bbro-details -fdump-rtl-cprop_hardreg-blocks-details -fdump-rtl-alignments 2>/dev/null || { echo compile failed; exit 1; }
awk '/^;; Function applyIniOptions/,/^;; Function parseRawPatch/' a.c.274r.bbro > aio.bbro
cd "$S"
[ -f orig.dis ] || $TC/objdump.exe -d -M intel --no-show-raw-insn --start-address=0x4259a0 --stop-address=0x427000 $R/xeBuild.exe > orig.dis
python lab.py $1/o.s | grep -v '^\* -:\.  *$' > $1/lab.txt
python trl.py $1 > $1/trl.txt
$TC/as.exe --32 $1/o.s -o $1/o.o 2>/dev/null
$TC/objdump.exe -d -M intel --no-show-raw-insn $1/o.o | awk '/<_applyIniOptions>:/,/<_parseRawPatch>:/' > $1/ours.dis
python discmp.py orig.dis $1/ours.dis > $1/al.txt
cd "$R"
blk=$(python wip/blk.py "wip/aio/$1/a.c" applyIniOptions $FL | grep -c '^[-+][^-+]')
fn=$(python re/fncmp.py "wip/aio/$1/a.c" applyIniOptions $FL | grep -c '^[-+][^-+]')
cd "$S"
lab=$(grep -c '^\*' $1/lab.txt)
echo "blk $blk fncmp $fn lab $lab align-diffs $(($(wc -l < $1/al.txt) - 1))"
