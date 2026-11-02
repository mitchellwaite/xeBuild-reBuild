#!/bin/sh
# ours.sh SRC.c OUT.txt : mode_client asm with literals resolved
R=/c/Users/Win11VM/Documents/GitHub/xebuildBugFix
export PATH=$R/tools/toolchain-4745/mingw32/bin:$R/tools/toolchain-4745/bin:$PATH
gcc -S -masm=intel -fno-asynchronous-unwind-tables -I$R/src -O3 -fno-toplevel-reorder -fno-ipa-profile -fno-reorder-functions --param builtin-expect-probability=50 $FX "$1" -o "$2.s" && python $R/tools/wip/mc/s75/res.py "$2.s" > "$2"
