"""diag.py SRC.c [TAG]: compile -O3 with dumps, show ev, r4 pops with keys (plain numbering assumed for no-dn sources) vs dsim.WANT."""
import glob
import os
import sys

import dsim
import mu

src = sys.argv[1]
tag = sys.argv[2] if len(sys.argv) > 2 else 'diag'
fl = sys.argv[3] if len(sys.argv) > 3 else '-O3'
txt = open(src, newline='').read()
o, err = mu.compile_text(txt, tag, fl, True)
if not o:
    print(err)
    sys.exit(1)
sc = mu.score(o)
print('ev', mu.total(sc), {k: v[0] for k, v in sc.items()})
d = os.path.join(mu.OUT, tag)
M = dsim.load(glob.glob(d + '/*bbro')[0])
o3, o4 = dsim.sim(M)
keys = {}
for g in list(M['g3'].values()) + list(M['g4'].values()) + [M['pre']]:
    for e in g:
        if e[0] == 'ins':
            keys[e[2]] = e[3]
        elif e[0] == 'push':
            keys[e[1]] = e[2]
print('model same', o3 == M['f3'], o4 == M['f4'])
print('r4:', ' '.join('%d:%s' % (b, keys.get(b) if abs(keys.get(b, 0)) < 1000 else 'P') for b in o4))
print('want:', ' '.join(map(str, dsim.WANT)))
got = [b for b in o4 if b not in dsim.FLEX]
print('order ok', got == dsim.WANT)
