#!/bin/sh
# par.sh files... : run.sh 4-way parallel, append to res.txt
cd /c/Users/Win11VM/Documents/GitHub/xebuildBugFix/tools/wip/mc/s104
printf '%s\n' "$@" | xargs -P 4 -I{} sh run.sh {} >> res.txt
echo PARDONE
