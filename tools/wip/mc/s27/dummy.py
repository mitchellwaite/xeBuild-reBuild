"""dummy.py TAG : what-if on slot_TAG's real history: one extra heap node (a zero-flow arm block)
inserted right after block X's trace is built in round 4 (after X's events), with key K
(-f or a priority key); the dummy's own pop is dropped from the order.  Prints the best (X, K)."""
import sys, os
R = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, os.path.join(R, r'tools\wip\mc\s18')); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(R, r'tools\wip'))
import hsim, ev, fibsim, mcsim2

Rr, keys = hsim.load(os.path.join(R, 'build', 'v', 'mc27', 'slot_' + sys.argv[1]))
f0, P0 = hsim.measured(keys)


def sim(R_, f, P, X, K, n=1):
    heap = fibsim.Heap(); new = None
    loc = {1002: (heap, heap.insert(0, 1002))}
    order = []

    def key(b, k):
        if b not in f: return k
        if k <= -1000000:
            return -(1000000 + 100 * P.get(b, 0) + f[b]) if P.get(b, 0) > 0 else -f[b]
        if k >= 10000: return k
        return -f[b]

    def apply(e):
        if e[0] == 'visit':
            if e[1] in loc:
                h, nd = loc.pop(e[1]); h.delete_node(nd)
        elif e[0] == 'ins':
            h = heap if e[1] == 'this' else new
            if e[2] in loc: return
            loc[e[2]] = (h, h.insert(key(e[2], e[3]), e[2]))
        elif e[0] == 'push':
            if e[1] in loc: return
            loc[e[1]] = (new, new.insert(key(e[1], e[2]), e[1]))
        elif e[0] == 'chg':
            if e[1] in loc:
                h, nd = loc[e[1]]; k = key(e[1], e[2])
                if k != nd.key: loc[e[1]] = (h, h.replace_key(nd, k))
    for ri, r in enumerate(R_, 1):
        if new is not None: heap = new
        new = fibsim.Heap()
        for e in r['pre']: apply(e)
        while heap.min is not None:
            z = heap.extract_min(); b = z.data; loc.pop(b, None)
            if isinstance(b, str): continue
            order.append((ri, b))
            for e in r['g'].get(b, []): apply(e)
            if ri == 4 and (b == X or (isinstance(X, tuple) and b in X)):
                for i in range(n):
                    heap.insert(K, 'dummy%d' % i)
    return [b for r, b in order if r == 4 and b in mcsim2.pos]


def tinv(o):
    inv, miss, oo = ev.score_order([str(b) for b in o]); return inv + 5 * len([b for b in miss if b not in ev.CASES])


base = sim(Rr, f0, P0, None, 0)
print('base', tinv(base), ' '.join(map(str, base[12:])))
res = []
for X in base:
    for K in (0, -1, -2, -3, -4, -1000101, -1000100):
        for n in (1, 2, 3):
            o = sim(Rr, f0, P0, X, K, n)
            res.append((tinv(o), X, K, n, ' '.join(map(str, o[12:]))))
res.sort()
for r in res[:8]: print(r)
if os.environ.get('PAIRS'):
    res = []
    T = [b for b in base if b not in (129,)]
    for i, a in enumerate(T):
        for b2 in T[i + 1:]:
            for K in (-1000101, 0, -1):
                o = sim(Rr, f0, P0, (a, b2), K, 1)
                res.append((tinv(o), a, b2, K, ' '.join(map(str, o[12:]))))
    res.sort()
    for r in res[:10]: print(r)
