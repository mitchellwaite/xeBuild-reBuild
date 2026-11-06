#!/bin/sh
# mode_client attempt 7: two (or three) feeds into the same target replaced by one 1-term
# feed from any position (mc7reloc).  Logs in build/mc/w7/pair_*.log.
cd "$(dirname "$0")/../../.."
B=${B:-build/mc/w7/base63.c}
R="python tools/wip/dehint/mc7reloc.py -base $B -k 1"
F1='if \(__builtin_constant_p\(mode \+ 620\)\) goto ndl;'
F2='if \(__builtin_constant_p\(mode \+ 255562\)\) goto ndl;'
F3='if \(__builtin_constant_p\(mode \+ 157368\)\) goto ndl;'
$R -rm "$F1" -rm "$F2" -ins 'if ({cp}) goto ndl;' -o build/mc/w7/pair_n12.c > build/mc/w7/pair_n12.log 2>&1
$R -rm "$F1" -rm "$F3" -ins 'if ({cp}) goto ndl;' -o build/mc/w7/pair_n13.c > build/mc/w7/pair_n13.log 2>&1
$R -rm "$F2" -rm "$F3" -ins 'if ({cp}) goto ndl;' -o build/mc/w7/pair_n23.c > build/mc/w7/pair_n23.log 2>&1
$R -rm "$F1" -rm "$F2" -rm "$F3" -ins 'if ({cp}) goto ndl;' -o build/mc/w7/pair_n123.c > build/mc/w7/pair_n123.log 2>&1
$R -rm 'if \(__builtin_constant_p\(mode \+ 130\)\) goto dtg;' -rm 'if \(__builtin_constant_p\(mode \+ 156949\)\) goto dtg;' -ins 'if ({cp}) goto dtg;' -o build/mc/w7/pair_dtg.c > build/mc/w7/pair_dtg.log 2>&1
$R -rm 'if \(__builtin_constant_p\(i \+ 321\)\) goto u2;' -rm 'if \(__builtin_constant_p\(mode \+ 50750\)\) goto u2;' -ins 'if ({cp}) goto u2;' -o build/mc/w7/pair_u2.c > build/mc/w7/pair_u2.log 2>&1
for f in build/mc/w7/pair_*.log; do echo "== $f"; grep -c HIT "$f"; tail -n 4 "$f"; done
