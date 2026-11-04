"""flxn.py <arm state label> [vars] [kmax]: one more dead test with k stores anywhere, on top of an arm-size state."""
import os, sys
from collections import Counter
import fllib as L, flxk as K, flx6 as D


def parse(lb):
    a = lb.split('|')
    keep = dict((kv.split('=')[0], int(kv.split('=')[1])) for kv in a[1].split(',') if kv)
    return a[0], keep, len(a) > 2


def ins(s, pos, v, k):
    ln = s[pos:s.index('\n', pos)]
    i = ln[:len(ln) - len(ln.lstrip())]
    return s[:pos] + '%sif (%s < -1) {\n%s%s}\n' % (i, v, ''.join('%s\tbuf[%d] = 1;\n' % (i, j) for j in range(k)), i) + s[pos:]


if __name__ == '__main__':
    base = K.build(*parse(sys.argv[1]))
    vs = (sys.argv[2] if len(sys.argv) > 2 else 'off,i,size').split(',')
    kmax = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    print('base', L.score(L.compile(base, None, 'bn'))[:3])
    V, meta = {}, {}
    for p in D.points(base):
        ln = base.count('\n', 0, p) + 1
        for v in vs:
            for k in range(1, kmax + 1):
                n = '%d_%s_%d' % (ln, v, k)
                V[n] = ins(base, p, v, k)
                meta[n] = base[p:base.index('\n', p)].strip()[:60]
    print(len(V))
    rs = L.sweep(V, prefix='n', show=0)
    for n, (sc, st, fd, sd) in rs[:14]:
        print(sc, n, meta[n], fd, sd)
    print(sorted(Counter(r[0] for n, r in rs).items())[:8])
