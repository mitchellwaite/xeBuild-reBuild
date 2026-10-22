#!/bin/sh
R=$(cd "$(dirname "$0")/../.." && pwd -P)
# align.sh <dir> <overrides>: run.sh, then assemble o.s and compare applyIniOptions' bytes (padding) with the original
S=$(cd "$(dirname "$0")" && pwd -P)
TC=$R/tools/toolchain-4745/mingw32/bin
cd $S
# the original's applyIniOptions and which of its labels need alignment
[ -f orig.dis ] || $TC/objdump.exe -d -M intel --no-show-raw-insn --start-address=0x4259a0 --stop-address=0x427000 $R/xeBuild.exe > orig.dis
[ -f alignreq.txt ] || python alignreq.py > alignreq.txt
sh run.sh $1 $2 | tr '\n' ' '
$TC/as.exe --32 $1/o.s -o $1/o.o 2>/dev/null
$TC/objdump.exe -d -M intel --no-show-raw-insn $1/o.o | awk '/<_applyIniOptions>:/,/<_parseRawPatch>:/' > $1/ours.dis
python discmp.py orig.dis $1/ours.dis > $1/al.txt
echo "align-diffs: $(($(wc -l < $1/al.txt) - 1)) $(head -1 $1/al.txt)"
