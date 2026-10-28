#!/bin/sh
# pe.sh VARIANT.c : profile_estimate predictions for the post-loop blocks of mode_client
B=/c/Users/Win11VM/Documents/GitHub/xebuildBugFix/tools/toolchain-4745/mingw32/bin
D=/c/Users/Win11VM/AppData/Local/Temp/pe8/$(basename $1 .c); mkdir -p $D; cp $1 $D/v.c; cd $D
PATH=$B:$PATH gcc -S -O3 --param builtin-expect-probability=50 -fdump-tree-profile_estimate-details v.c -o v.s || exit 1
awk '/^;; Function mode_client/,0' v.c.*profile_estimate > mc.txt
L=$(grep -n "loop exit heuristics: 98" mc.txt | tail -1 | cut -d: -f1)
sed -n "$((L-6)),\$p" mc.txt | sed -n '1,/^;; Function\|^  <bb 2>/p' | grep -v "^ *$" | sed -n '1,/^;;   basic block/p' | grep -v "^;;   basic"
