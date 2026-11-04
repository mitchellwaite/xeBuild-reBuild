"""fl4l.py <state>: state +/- one test at the seven sites with arms 1-5"""
import sys
import fllib as L, fl4lib as F, fl4g as G
s0 = sys.argv[1]
d0 = dict(kv.split('=') for kv in s0.split(',') if kv)
V = {}
for n in F.SITES:
    for k in ('', 1, 2, 3, 4, 5):
        d = dict(d0)
        if k == '':
            d.pop(n, None)
        else:
            d[n] = str(k)
        l = ','.join('%s=%s' % (a, d[a]) for a in F.SITES if a in d)
        V[l] = G.mk(F.st(l))
print(len(V))
F.run(V, 'l', show=14)
