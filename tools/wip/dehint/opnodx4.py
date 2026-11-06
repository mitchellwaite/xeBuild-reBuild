"""Attempt 4: write build/op/nodx.c = src/options.c with parseButtonX's dx dummy gone (its feed,
asm goto, cold label, tail test and unreachable: 6 tricks), for OPBASE= sweeps with optricks."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

t = optlib.read_src(optlib.SRC)
edits = [
    ('\t\tif (__builtin_expect(__builtin_constant_p(xb.xellButton + 5), 1)) goto dx;\nbx: ;\n', ''),
    ('\t\t__asm__ goto ("" :::: dx);\n', ''),
    ('''dx: __attribute__((cold));
	b = 0x11;
	if (__builtin_constant_p(xb.xellButton + 6))
		goto bx;
	__builtin_unreachable();
''', ''),
]
for a, b in edits:
    assert a in t, a
    t = t.replace(a, b)
out = os.path.join(optlib.BUILD, 'nodx.c')
open(out, 'w', newline='\n').write(t)
print(optlib.fmt(optlib.score_text(t)))
