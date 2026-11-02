#!/bin/sh
# hd.sh TAG: r4 trace heads with freq
grep -E '^Trace' /c/Users/Win11VM/Documents/GitHub/xebuildBugFix/build/v/aio_p1/$1/aio.bbro | grep 'round 4' | sed -E 's/Trace [0-9]+ \(round 4\): +([0-9]+) \[([0-9]+)\].*/\1:\2/' | tr '\n' ' ' | cut -c1-800; echo
