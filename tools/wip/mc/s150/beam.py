# beam.py DUMP [levels] [width] : beam search over r4 shape changes (state-based, sequential)
# change types: dum (dummy heap entry G,at,key), key (override b->k), rm (remove op),
# mv (move an ins op to another trace/position), sw (swap adjacent ops in a trace),
# pp (permute order of round-3 final pushes of 35/42/53), r3 (tail block built in round 3:
# it is emitted at the end of round 3 i.e. just before r4's first trace and removed from r4)
import sys, itertools, time
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s86'); import r4sim
pre0, g0, first = r4sim.load(sys.argv[1])
LV = int(sys.argv[2]) if len(sys.argv) > 2 else 5; W = int(sys.argv[3]) if len(sys.argv) > 3 else 400
D = 9999
i = first.index(150); TGT = first[:i] + [147,128,150,35,42,53,79,81] + first[i+8:]
TAIL = [150,147,79,128,81,42,53,35,144,145,75]
def score(o):
    o = [b for b in o if b < D]
    return sum(a != b for a, b in zip(o, TGT)) + abs(len(o) - len(TGT))
# state: (groups tuple-of-tuples dict, ov frozenset, pre tuple, r3 tuple, ndum)
def freeze(gg, ov, pre, r3, nd):
    return (tuple((k, tuple(gg[k])) for k in sorted(gg)), tuple(sorted(ov.items())), tuple(pre), tuple(r3), nd)
def run(st):
    G, ov, pre, r3, nd = st
    gg = {k: list(v) for k, v in G}
    try: o = r4sim.sim(list(pre), gg, dict(ov))
    except Exception: return []
    if r3: o = list(r3) + [b for b in o if b not in r3]
    return o
# round-3 last pushes of 35/53/42 indices
PP = [j for j, e in enumerate(pre0) if e[0] == 'push' and e[1] in (35, 42, 53)][-3:]
def moves(st):
    G, ov, pre, r3, nd = st; gg = dict(G); out = []
    keys = list(gg)
    for k in keys:
        L = gg[k]
        for at in range(len(L) + 1):
            if nd < 3:
                for kk in (0, -1, -2): out.append(('dum', k, at, kk))
        for j, e in enumerate(L):
            if e[0] in ('ins', 'chg'): out.append(('rm', k, j))
            if j + 1 < len(L) and L[j] != L[j+1]: out.append(('sw', k, j))
            if e[0] == 'ins':
                for k2 in keys:
                    for at in range(len(gg[k2]) + 1):
                        if k2 != k or at not in (j, j + 1): out.append(('mv', k, j, k2, at))
    for b in TAIL:
        for kk in (-2, -1, 1):
            if dict(ov).get(b) != kk: out.append(('key', b, kk))
    for p in itertools.permutations(range(3)):
        if p != (0, 1, 2): out.append(('pp', p))
    for b in TAIL:
        if b not in r3: out.append(('r3', b))
    return out
def apply(st, c):
    G, ov, pre, r3, nd = st; gg = {k: list(v) for k, v in G}; ov = dict(ov); pre = list(pre); r3 = list(r3)
    t = c[0]
    if t == 'dum': gg[c[1]].insert(c[2], ('ins', 'this', D + nd, c[3])); nd += 1
    elif t == 'key': ov[c[1]] = c[2]
    elif t == 'rm': del gg[c[1]][c[2]]
    elif t == 'sw': L = gg[c[1]]; L[c[2]], L[c[2]+1] = L[c[2]+1], L[c[2]]
    elif t == 'mv':
        e = gg[c[1]].pop(c[2]); at = c[4]
        if c[3] == c[1] and at > c[2]: at -= 1
        gg[c[3]].insert(at, e)
    elif t == 'pp':
        ev = [pre[j] for j in PP]
        for n, j in enumerate(PP): pre[j] = ev[c[1][n]]
    elif t == 'r3': r3.append(c[1])
    return freeze(gg, ov, pre, r3, nd)
base = freeze(g0, {}, pre0, [], 0)
print('base', score(run(base))); sys.stdout.flush()
beam = {base: ()}; seen = {base}; sols = []; t0 = time.time()
for lv in range(1, LV + 1):
    cand = []
    for st, hist in beam.items():
        for c in moves(st):
            ns = apply(st, c)
            if ns in seen: continue
            seen.add(ns); s = score(run(ns)); h = hist + (c,)
            cand.append((s, h, ns))
            if s == 0: sols.append(h); print('SOL', lv, h); sys.stdout.flush()
    cand.sort(key=lambda x: x[0])
    hist_ = {}
    for s, h, ns in cand[:W]: hist_[ns] = h
    beam = hist_
    print('level', lv, 'ncand', len(cand), 'best', cand[0][0] if cand else None,
          'beamworst', cand[min(W, len(cand)) - 1][0] if cand else None, 'nsol', len(sols), round(time.time() - t0)); sys.stdout.flush()
    from collections import Counter
    print('  dist', sorted(Counter(x[0] for x in cand).items())[:8]); sys.stdout.flush()
