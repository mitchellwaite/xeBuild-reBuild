# hk.py NAME MODE idx... : MODE=add (apply listed best18 hunks onto c0) | del (best18 minus listed hunks)
import sys, difflib
a = open('c0.c').read().split('\n'); b = open('b18.c').read().split('\n')
ops = [o for o in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes()]
H = [i for i, o in enumerate(ops) if o[0] != 'equal']
if sys.argv[1] == 'list':
    for k, i in enumerate(H):
        t, i1, i2, j1, j2 = ops[i]; print(k, t, i1, repr(' '.join(b[j1:j2])[:110])); 
    sys.exit()
name, mode = sys.argv[1], sys.argv[2]; sel = set(int(x) for x in sys.argv[3:])
out = []
for i, (t, i1, i2, j1, j2) in enumerate(ops):
    if t == 'equal': out += a[i1:i2]; continue
    k = H.index(i); use = (k in sel) if mode == 'add' else (k not in sel)
    out += b[j1:j2] if use else a[i1:i2]
open('v/%s.c' % name, 'w', newline='\n').write('\n'.join(out))
