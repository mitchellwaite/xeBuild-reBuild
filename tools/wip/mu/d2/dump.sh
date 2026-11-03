#!/bin/sh
# dump.sh SRC TAG [flags]: all tree + rtl dumps of SRC into build/v/mu_d2/TAG, plus .s
R=/c/Users/Win11VM/Documents/GitHub/xebuildBugFix
PATH="$R/tools/toolchain-4745/mingw32/bin:$PATH"
D=$R/build/v/mu_d2/$2; mkdir -p $D; { printf '#line 1 "mode_update.c"\n'; cat $1; } > $D/m.c
cd $D; gcc -S -O3 ${3:-} -fdump-tree-all -fdump-tree-pre-details -fdump-rtl-all -I$R/src m.c -o m.s
