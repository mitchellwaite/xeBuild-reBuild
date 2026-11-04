#!/bin/sh
# sh tools/wip/dehint/iw23dump.sh <name> <file.c>: all tree dumps (with vops) of <file.c> in build/iw/a23/d_<name>, then the names around unswitch and sccp in writeFsTable.
R=$(cd "$(dirname "$0")/../../.." && pwd)
export PATH="$R/tools/toolchain-4745/mingw32/bin:$PATH"
D="$R/build/iw/a23/d_$1"; mkdir -p "$D"; cp "$2" "$D/a.c"
(cd "$D" && gcc -c -O3 -I"$R/src" a.c -fdump-tree-all-vops 2>/dev/null)
python "$R/tools/wip/dehint/iw15stack.py" "$D" writeFsTable pre sccp | cut -c1-400
