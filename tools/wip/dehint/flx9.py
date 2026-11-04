"""flx9.py <fl> [label edits]: tie vector for all 256 dead subsets; prints those under 20 lines."""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
import fllib as L, flx as X, flx3 as A, flx7 as T

fl = sys.argv[1]
ch = dict(kv.split('=') for kv in sys.argv[2].split(',')) if len(sys.argv) > 2 and sys.argv[2] else {}
V = {}
for r in range(len(X.ALLDEAD) + 1):
    for rm in itertools.combinations(X.ALLDEAD, r):
        V['+'.join(x for x in X.ALLDEAD if x not in rm)] = A.apply(X.gen(rm, fl), ch)


def one(kv):
    i, (n, s) = kv
    o = L.compile(s, None, 'nv%d' % i)
    sc = L.score(o)
    v = T.vec(o)
    os.remove(o)
    return sc[0], v, n


with ThreadPoolExecutor(4) as ex:
    rs = sorted(ex.map(one, enumerate(V.items())), key=lambda r: r[0])
for r in rs:
    if r[0] < 20:
        print(r[0], r[1], 'keep:', r[2])
