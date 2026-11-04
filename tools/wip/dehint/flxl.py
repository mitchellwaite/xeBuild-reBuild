"""flxl.py <rounds> [beam] [kmax]: beam search from xk.txt's best over dead-test arm sizes (nest).
Neighbours change one test's k (0 = absent) or toggle t.  Prints any MATCH."""
import os, re, sys
from concurrent.futures import ThreadPoolExecutor
import fllib as L, flx as X, flx7 as T, flxj as J, flxk as K

rounds = int(sys.argv[1])
beam = int(sys.argv[2]) if len(sys.argv) > 2 else 20
kmax = int(sys.argv[3]) if len(sys.argv) > 3 else 6
names = list(J.ARM)


def parse(lb):
    a = lb.split('|')
    keep = dict((kv.split('=')[0], int(kv.split('=')[1])) for kv in a[1].split(',') if kv)
    return a[0], keep, len(a) > 2


seen = {}
for ln in open(L.BD + '/xk.txt'):
    p = ln.rstrip('\n').split('\t')
    if len(p) >= 4:
        seen[p[2]] = (float(p[0]), p[1], int(p[3]))


def top():
    return sorted(seen.items(), key=lambda kv: (kv[1][0] + 0.5 * kv[1][2]))[:beam]


out = open(L.BD + '/xk.txt', 'a', newline='\n')
for rnd in range(rounds):
    V = {}
    for lb, _ in top():
        fl, keep, t = parse(lb)
        for n in names:
            for k in range(0, kmax + 1):
                kk = dict(keep)
                if k == 0:
                    kk.pop(n, None)
                else:
                    kk[n] = k
                nb = K.lab(fl, kk, t)
                if nb not in seen and nb not in V:
                    V[nb] = K.build(fl, kk, t)
        nb = K.lab(fl, keep, not t)
        if nb not in seen and nb not in V:
            V[nb] = K.build(fl, keep, not t)

    def one(kv):
        i, (n, s) = kv
        o = L.compile(s, None, 'l%d' % i)
        if o is None:
            return 10**7, '', n
        sc = L.score(o)
        v = T.vec(o)
        os.remove(o)
        return sc[0], v, n
    with ThreadPoolExecutor(4) as ex:
        rs = list(ex.map(one, enumerate(V.items())))
    for sc, v, n in rs:
        fl, keep, t = parse(n)
        seen[n] = (sc, v, K.count(fl, keep, t))
        out.write('%s\t%s\t%s\t%d\n' % (sc, v, n, seen[n][2]))
    out.flush()
    print('round', rnd, 'new', len(V))
    for lb, q in top()[:8]:
        print(' ', q, lb)
    sys.stdout.flush()
print('MATCHES', [(lb, q[2]) for lb, q in seen.items() if q[0] == 0][:40])
