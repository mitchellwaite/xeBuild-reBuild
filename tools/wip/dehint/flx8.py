"""flx8.py <state label> [TAG env]: one strlen-dead block (dies after dom3) at every statement point."""
import os, sys
import fllib as L, flx as X, flx3 as A, flx4 as F, flx6 as D

BLK = '%s{\n%s\tchar t_[4];\n%s\tstrcpy(t_, "ab");\n%s\tif (strlen(t_) != 2)\n%s\t\tbuf[0] = 1;\n%s}\n'


def ins(s, pos):
    ln = s[pos:s.index('\n', pos)]
    i = ln[:len(ln) - len(ln.lstrip())]
    return s[:pos] + BLK % (i, i, i, i, i, i) + s[pos:]


if __name__ == '__main__':
    fl, dead, ch = F.parse(sys.argv[1])
    base = A.apply(X.gen(dead, fl), ch)
    print('base', L.score(L.compile(base, None, 'b8'))[:3])
    V, meta = {}, {}
    for p in D.points(base):
        n = str(base.count('\n', 0, p) + 1)
        V[n] = ins(base, p)
        meta[n] = base[p:base.index('\n', p)].strip()[:60]
    rs = L.sweep(V, prefix='t8', show=0)
    for n, (sc, st, fd, sd) in rs[:14]:
        print(sc, n, meta[n], fd)
    from collections import Counter
    print(sorted(Counter(r[0] for n, r in rs).items())[:12])
