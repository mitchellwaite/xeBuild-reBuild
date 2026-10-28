"""Sim: asm-goto fake edges from a block X between 104 and 105 into cold targets T.
The targets are pushed to the next-round heap when X is visited (round 2), re-pushed
when extracted in rounds 2-3, and their frequencies become free.  Hill-climb integer
frequencies for inv 0.  python fake.py bbro iters seed T1,T2,... [order perms]"""
import random, sys, os, itertools
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, ROOT + r'\wip'); sys.path.insert(0, ROOT + r'\wip\mc')
import fibsim, fibwhatif, mcsim2
WANT = mcsim2.WANT
ev = fibsim.parse(sys.argv[1]); R = fibwhatif.groups(ev)
IT = int(sys.argv[2]); random.seed(int(sys.argv[3]))
T = [int(x) for x in sys.argv[4].split(',')] if len(sys.argv) > 4 and sys.argv[4] else []
FREE = [int(x) for x in os.environ.get('FREE', '').split(',') if x]
AFTER = int(os.environ.get('AFTER', '104'))   # inject after visiting this block (round 2)
COLD = [49, 112, 115, 103, 55, 126, 125, 61, 33, 29, 67, 127, 117, 130, 35, 42, 53, 77, 79]
C = 7
MX = int(os.environ.get('MX', '9'))
CASES = [129, 107, 109, 110, 113, 108, 119, 120, 121, 128, 116, 132]
VC = os.environ.get('VC') == '1'
def sim(freq, T):
    heap = fibsim.Heap(); new = None
    loc = {2: (heap, heap.insert(0, 2))}
    order = []
    def key(b, k):
        if b not in freq: return k
        f = freq[b]
        return -(1000000 + 100 * f + f) if k <= -100 else -f
    def apply(e):
        nonlocal heap, new
        if e[0] == 'visit':
            if e[1] in loc:
                h, n = loc.pop(e[1]); h.delete_node(n)
            if e[1] == AFTER:
                for t in T:
                    if t not in loc: loc[t] = (new, new.insert(-freq[t], t))
        elif e[0] == 'ins':
            h = heap if e[1] == 'this' else new
            if e[2] in loc: return
            loc[e[2]] = (h, h.insert(key(e[2], e[3]), e[2]))
        elif e[0] == 'push':
            loc[e[1]] = (new, new.insert(key(e[1], e[2]), e[1]))
        elif e[0] == 'chg':
            if e[1] in loc:
                h, n = loc[e[1]]; loc[e[1]] = (h, h.replace_key(n, key(e[1], e[2])))
    for ri, r in enumerate(R, 1):
        if new is not None: heap = new
        new = fibsim.Heap()
        for e in r['pre']: apply(e)
        while heap.min is not None:
            z = heap.extract_min(); b = z.data; loc.pop(b, None)
            if b in T and ri < 4:
                loc[b] = (new, new.insert(-freq[b], b)); continue
            order.append((ri, b))
            for e in r['g'].get(b, []): apply(e)
    return order
npre = sum(len(r['order']) for r in R[:3])
def score(f):
    o = sim(f, T)
    o = [b for r, b in o if r == 4 and b in mcsim2.pos]
    p = mcsim2.pos
    inv = sum(1 for a in range(len(o)) for b in range(a + 1, len(o)) if p[o[a]] > p[o[b]])
    return inv, o
def ok(f, T=None):
    T = (T_INJ + FREE)
    if VC and sum(f[c] for c in CASES) + sum(f[t] for t in T) > 88: return False
    if 112 not in T and f[112] > 4: return False
    if 115 not in T and f[115] > 4: return False
    if f[103] < 4: return False
    if max(f.values()) > MX: return False
    if 117 not in T and f[117] > f[116]: return False
    if 130 not in T and f[130] > f[129]: return False
    if 49 not in T and not (f[55] <= f[49] / 2 + .5 and f[61] <= f[55] / 2 + .5 and f[67] <= f[61] / 2 + .5): return False
    if any(f[b] > 5 for b in (35, 42, 53, 77, 79)): return False
    a = f[127] if 127 not in T else 0
    if 126 not in T and f[126] > (C - a) / 2 + .5: return False
    if 125 not in T and f[125] > (C - a - (0 if 126 in T else f[126])) / 2 + .5: return False
    return True
BASE = {112: 4, 115: 4, 127: 0, 126: 3, 125: 2, 49: 6, 55: 3, 61: 1, 67: 0, 103: 4, 117: 1, 130: 1, 29: 1, 33: 1, 35: 0, 42: 0, 53: 0, 77: 0, 79: 0}
BASE.update({c: 6 for c in CASES})
T_INJ = T
best = None; bs = 999
for it in range(IT):
    if best is None or random.random() < 0.01:
        f = dict(BASE)
    else:
        f = dict(best)
        for b in random.sample(COLD + (CASES if VC else []), random.choice((1, 1, 2, 3))):
            f[b] = max(0, min(12, f[b] + random.choice((-2, -1, 1, 2))))
    if not ok(f): continue
    try: inv, o = score(f)
    except Exception as ex: continue
    if inv <= bs:
        if inv < bs: print(it, inv, f, flush=True)
        bs, best = inv, f
        if inv == 0: break
print('best', bs, best); print(' '.join(map(str, score(best)[1])))
