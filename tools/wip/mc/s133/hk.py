# hk.py list | hk.py NAME idx... : best34 + selected best18 hunks (c0-relative); overlap -> b18 hunk wins, k-hunk dropped
import sys, difflib
a = open('c0.c').read().split('\n'); b = open('b18.c').read().split('\n'); c = open(sys.argv[0].replace('hk.py','')+'best34.c').read().split('\n')
def hunks(x):
    return [o for o in difflib.SequenceMatcher(None, a, x, autojunk=False).get_opcodes() if o[0] != 'equal']
HB = hunks(b); HC = hunks(c)
if sys.argv[1] == 'list':
    for k, (t, i1, i2, j1, j2) in enumerate(HB): print(k, t, i1, i2, repr(' '.join(b[j1:j2])[:100]))
    sys.exit()
sel = [HB[int(x)] for x in sys.argv[2:]]
def ov(h, g): return not (h[2] < g[1] or g[2] < h[1]) if (h[1]!=h[2] and g[1]!=g[2]) else (g[1] <= h[1] <= g[2] or h[1] <= g[1] <= h[2])
use = [(h, b) for h in sel] + [(h, c) for h in HC if not any(ov(h, g) for g in sel)]
use.sort(key=lambda u: (u[0][1], u[0][2]))
out = []; p = 0
for (t, i1, i2, j1, j2), src in use:
    if i1 < p: continue
    out += a[p:i1] + src[j1:j2]; p = i2
out += a[p:]
open('v/%s.c' % sys.argv[1], 'w', newline='\n').write('\n'.join(out))
