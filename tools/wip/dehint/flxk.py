"""flxk.py <N> <seed> [fl,fl] [p] [kmax]: dead tests with small arm sizes (0 = absent), sampled; also t optional.
Results append to xk.txt; a line per score so far.  MATCH lines print at the top."""
import os, random, sys
from concurrent.futures import ThreadPoolExecutor
import fllib as L, flx as X, flx7 as T, flxj as J


def build(fl, keep, t):
    """keep {test: k}; t True keeps the strlen block"""
    dead = [d for d in X.ALLDEAD if d not in keep and not (d == 't' and t)]
    s = X.gen(dead, fl)
    for n, k in keep.items():
        o, w, ind = J.ARM[n]
        s = L.sub(s, o, w % ''.join('%sbuf[%d] = 1;\n' % (ind, j) for j in range(k)))
    return s


def lab(fl, keep, t):
    return fl + '|' + ','.join('%s=%d' % kv for kv in sorted(keep.items())) + ('|t' if t else '')


def count(fl, keep, t):
    return len(keep) + (1 if t else 0) + (0 if fl == 'nest' else 1)


if __name__ == '__main__':
    N, seed = int(sys.argv[1]), int(sys.argv[2])
    fls = sys.argv[3].split(',') if len(sys.argv) > 3 else ['nest']
    p = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
    kmax = int(sys.argv[5]) if len(sys.argv) > 5 else 4
    rng = random.Random(seed)
    names = list(J.ARM)
    V, meta = {}, {}
    while len(V) < N:
        fl = rng.choice(fls)
        keep = {n: rng.randint(1, kmax) for n in names if rng.random() < p}
        t = rng.random() < 0.2
        n = lab(fl, keep, t)
        V[n] = build(fl, keep, t)
        meta[n] = count(fl, keep, t)

    def one(kv):
        i, (n, s) = kv
        o = L.compile(s, None, 'k%d_%d' % (seed, i))
        if o is None:
            return 10**7, '', n
        sc = L.score(o)
        v = T.vec(o)
        os.remove(o)
        return sc[0], v, n
    with ThreadPoolExecutor(4) as ex:
        rs = sorted(ex.map(one, enumerate(V.items())), key=lambda r: (r[0], meta[r[2]]))
    with open(L.BD + '/xk.txt', 'a', newline='\n') as f:
        for r in rs:
            f.write('%s\t%s\t%s\t%d\n' % (r[0], r[1], r[2], meta[r[2]]))
    for r in rs[:25]:
        print(r[0], r[1], r[2], 'tests', meta[r[2]])
