"""Sim over fake-edge designs on a vY-style history (renumbered to sp bbs, X = 999).
State: integer freqs + case edge freqs (-c) + the set TX of X's asm-goto targets (pushed when X
is visited) + ERF (erase fakes: 125/127 free, 125 pushed when 121 is visited).
python fake3.py bbro iters seed"""
import random, sys, os
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, ROOT + r'\wip'); sys.path.insert(0, ROOT + r'\wip\mc')
import fibsim, fibwhatif, mcsim2
ev = fibsim.parse(sys.argv[1]); R = fibwhatif.groups(ev)
IT = int(sys.argv[2]); random.seed(int(sys.argv[3]))
CASES = [129, 107, 109, 110, 113, 108, 119, 120, 121, 128, 116, 132]
COLD = [49, 112, 115, 103, 55, 126, 125, 61, 33, 29, 67, 127, 117, 130, 35, 42, 53, 77, 79]
XC = [112, 115, 117, 130, 103] + [c for c in CASES if c not in (110, 113)]
ERF = os.environ.get('ERF', '1') == '1'
MAXX = int(os.environ.get('MAXX', '99'))
def sim(f, TX):
    heap = fibsim.Heap(); new = None
    loc = {2: (heap, heap.insert(0, 2))}
    order = []
    def key(b, k):
        if b not in f: return k
        if k <= -100: return -(1000000 + 100 * f.get(-b, f[b]) + f[b])
        return -f[b]
    def ins(h, b):
        if b not in loc: loc[b] = (h, h.insert(-f[b], b))
    def apply(e):
        nonlocal heap, new
        if e[0] == 'visit':
            if e[1] in loc:
                h, n = loc.pop(e[1]); h.delete_node(n)
            if e[1] == 999:
                for t in TX: ins(new, t)
            if e[1] == 121 and ERF and ri == 4:
                ins(heap, 125)
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
            if b in TX and ri < 4:
                kk = -(1000000 + 100 * f.get(-b, f[b]) + f[b]) if b in CASES else -f[b]
                loc[b] = (new, new.insert(kk, b)); continue
            order.append((ri, b))
            for e in r['g'].get(b, []): apply(e)
    return [b for r, b in order if r == 4 and b in mcsim2.pos]
def inv(o):
    p = mcsim2.pos
    return sum(1 for a in range(len(o)) for b in range(a + 1, len(o)) if p[o[a]] > p[o[b]])
def ok(f, TX):
    for c in CASES:
        if f[c] > 10 or f[-c] > f[c]: return False
        if c not in TX and f[-c] != f[c]: return False
    if 112 not in TX and f[112] > f[110] / 2 + .5: return False
    if 115 not in TX and f[115] > f[113] / 2 + .5: return False
    if 117 not in TX and f[117] > f[116]: return False
    if 130 not in TX and f[130] > f[129]: return False
    if 103 not in TX and f[103] != 4: return False
    if f[103] < 4: return False
    if max(f[b] for b in COLD) > 10: return False
    C10 = f[121]
    a = 0 if ERF else f[127]
    if f[127] > C10 or f[126] > (C10 - a) / 2 + .5: return False
    if not ERF and f[125] > (C10 - a - f[126]) / 2 + .5: return False
    if not (f[55] <= f[49] / 2 + .5 and f[61] <= f[55] / 2 + .5 and f[67] <= f[61] / 2 + .5): return False
    if any(f[b] > 5 for b in (35, 42, 53, 77, 79)): return False
    disp = sum(f[-c] for c in CASES) + sum(f[t] - (f[-t] if t in CASES else 0) for t in TX)
    if disp > 86: return False
    if len(TX) > MAXX: return False
    return True
BASE = {112: 3, 115: 3, 127: 0, 126: 3, 125: 1, 49: 6, 55: 3, 61: 1, 67: 0, 103: 4, 117: 1, 130: 1, 29: 1, 33: 1, 35: 0, 42: 0, 53: 0, 77: 0, 79: 0}
for c in CASES: BASE[c] = BASE[-c] = 6
KEYS = COLD + CASES + [-c for c in CASES]
TX0 = frozenset(XC) if os.environ.get('ALLX') else frozenset()
best = (dict(BASE), TX0); bs = 999
cur, cs = best, bs
for it in range(IT):
    if random.random() < 0.002:
        f, TX = dict(BASE), TX0
    else:
        f, TX = dict(cur[0]), set(cur[1])
        for _ in range(random.choice((1, 1, 2, 3))):
            if random.random() < 0.15:
                t = random.choice(XC); TX ^= {t}
            else:
                b = random.choice(KEYS); f[b] = max(0, f[b] + random.choice((-2, -1, 1, 2)))
        TX = frozenset(TX)
    if not ok(f, TX): continue
    try: v = inv(sim(f, TX))
    except Exception: continue
    if v <= cs or random.random() < 0.01:
        cur, cs = (f, TX), v
    if v < bs:
        bs, best = v, (f, TX); print(it, v, sorted(TX), flush=True)
        if v == 0: break
print('best', bs, sorted(best[1]), best[0])
print(' '.join(map(str, sim(best[0], best[1]))))
