"""fl4x.py: subsets of the 4 parseIni tests of the 9->5 state, arms 1-3, the raw test anchored by its statement."""
import itertools, re
import fllib as L, fl4lib as F, fl4g as G, fl4r as R, fl4final as Z

S = Z.build()
s0 = G.mk(F.st(Z.TESTS))
k, ind = R.sites(s0)[62]
LINE = s0[k:s0.index('\n', k) + 1]
print('site 62 is before:', repr(LINE), 'nth', s0[:k].count(LINE))
NTH = s0[:k].count(LINE)


def ins(s, cond, arm):
    p = -1
    for _ in range(NTH + 1):
        p = s.index(LINE, p + 1)
    return R.ins(s, p, ind, cond, arm)


def mk(tl, ex):
    s = G.mk(F.st(tl))
    if ex:
        s = ins(s, 'off < -1', '; '.join(['*buf = 0', 'buf[size] = 0', 'buf[1] = 0'][:ex]))
    s = L.sub(s, Z.KU, '')
    return L.sub(s, Z.KEYCMP[0], Z.KEYCMP[1])


V = {}
SITES = ['off3', 'off4', 'x']
for ex in (0, 1, 2, 3):
    for a, b, c in itertools.product((0, 1, 2, 3), repeat=3):
        tl = ','.join('%s=%d' % (n, v) for n, v in zip(SITES, (a, b, c)) if v)
        V['%s ex=%d' % (tl, ex)] = mk(tl, ex)
print(len(V))
rs = F.run(V, 'x', show=16)
