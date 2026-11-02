#!/bin/sh
# run.sh SRC.c TAG: plain compile with dumps into build/v/mu_p1/TAG, ev diff counts, trace tail vs target order.
R=/c/Users/Win11VM/Documents/GitHub/xebuildBugFix
cd $R; export PATH="$R/tools/toolchain-4745/mingw32/bin:$PATH"
D=build/v/mu_p1/$2; mkdir -p $D
FL="-O3 -fno-toplevel-reorder --param builtin-expect-probability=68 -fno-ipa-profile -fno-reorder-functions $FX"
{ printf '#line 1 "mode_update.c"\n'; cat "$1"; } > $D/m.c
(cd $D && gcc.exe -S $FL -I$R/src -fdump-rtl-bbro-details -fdump-tree-profile_estimate-blocks-details m.c -o m.s && as.exe --32 m.s -o o.o) || exit 1
rm -f $D/m.c.*.mu
cd tools/wip/mu/p1
python tr.py ../../../../$D | tail -32 | cut -c1-${3:-110}
python - "$R/$D/o.o" <<'PY'
import sys,ev
r=ev.score(sys.argv[1]); print('EV',r if r else 'all functions same')
PY
python refseq.py ../../../../$D/o.o | grep -c '^[-+][^-+]'
