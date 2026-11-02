#!/bin/sh
# mkmatch.sh OUT.c: regenerate match.c's code (before the comment tidy) from n8c.c with mk.py
R=/c/Users/Win11VM/Documents/GitHub/xebuildBugFix; cd $R
c() { echo "__builtin_constant_p(xb.blSuffix[1] + $1)"; }
F="if (__builtin_expect($(c 15), 0)) { if ($(c 16)) { if ($(c 17)) { if ($(c 18)) { if (__builtin_expect($(c 19), 1)) goto dz2; } } } }"
python tools/wip/aio/p1/mk.py "$1" xb1 noecdg old2 gl=smcnoeject:optE,cygnos:optC,nosecurity:optS,nandmu:optU dzm "dzd=$F"
