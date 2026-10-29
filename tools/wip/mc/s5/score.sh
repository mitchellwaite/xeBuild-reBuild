#!/bin/sh
# score.sh VARIANT... : build each variant with var.py and score its cold order (mcvar.py)
cd /c/Users/Win11VM/Documents/GitHub/xebuildBugFix
for v in "$@"; do
  python tools/wip/mc/s5/var.py "$v" >/dev/null
  echo "$v $(FNCMP=1 python tools/wip/mc/mcvar.py "tools/wip/mc/s5/v_$v.c" -O3 --param builtin-expect-probability=50 2>&1 | head -2 | tr '\n' ' ')"
done
