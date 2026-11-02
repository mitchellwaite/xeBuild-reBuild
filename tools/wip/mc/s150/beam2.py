# beam2.py DUMP MODE [levels] [width] : parallel beam over r4 shape changes; hash-only seen set.
# MODE all = every type; real = no moving of 128 away from trace 127's natural first insertion,
# no key overrides on 128 (unreachable per s146/s147/s149).
# types: dum, key, rm, mv, sw, pp (order of final round-3 pushes), ph (tail block pushed at end of
# round 3 i.e. in the initial r4 heap, as if its pred trace was built in round 3).
import sys, itertools, time, multiprocessing as mp
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s86'); import r4sim
D = 9999
TAIL = [150,147,79,128,81,42,53,35,144,145,75]
def init(dump, mode):
    global pre0, g0, first, TGT, PP, MODE, POSN
    MODE = mode
    pre0, g0, first = r4sim.load(dump)
    i = first.index(150); TGT = first[:i] + [147,128,150,35,42,53,79,81] + first[i+8:]
    PP = [j for j, e in enumerate(pre0) if e[0] == 'push' and e[1] in (35, 42, 53)][-3:]
    POSN = {b: n for n, b in enumerate(TGT)}
def score(o):
    o = [b for b in o if b < D]
    h = sum(a != b for a, b in zip(o, TGT)) + abs(len(o) - len(TGT))
    if h == 0: return (0, 0)
    p = [POSN.get(b, 999) for b in o]
    inv = sum(p[i] > p[j] for i in range(len(p)) for j in range(i+1, min(i+12, len(p))))
    return (h, inv)
def run(st):
    G, ov, pre = st[:3]
    try: return r4sim.sim(list(pre), {k: list(v) for k, v in G}, dict(ov))
    except Exception: return []
def moves(st):
    G, ov, pre, nd = st; gg = dict(G); keys = list(gg); ovd = dict(ov)
    for k in keys:
        L = gg[k]
        if nd < 3:
            for at in range(len(L) + 1):
                for kk in (0, -1, -2): yield ('dum', k, at, kk)
        for j, e in enumerate(L):
            if e[0] in ('ins', 'chg'):
                if not (MODE == 'real' and e[0] == 'ins' and e[2] == 128): yield ('rm', k, j)
            if j + 1 < len(L) and L[j] != L[j+1]: yield ('sw', k, j)
            if e[0] == 'ins' and not (MODE == 'real' and e[2] == 128):
                for k2 in keys:
                    for at in range(len(gg[k2]) + 1):
                        if k2 != k or at not in (j, j + 1): yield ('mv', k, j, k2, at)
    for b in TAIL:
        if MODE == 'real' and b == 128: continue
        for kk in (-2, -1, 1):
            if ovd.get(b) != kk: yield ('key', b, kk)
    for p in itertools.permutations(range(3)):
        if p != (0, 1, 2): yield ('pp', p)
    for b in TAIL:
        if MODE == 'real' and b == 128: continue
        for off in (0, 1, 2, 3):
            yield ('ph', b, off)
def apply(st, c):
    G, ov, pre, nd = st; t = c[0]
    if t in ('dum', 'rm', 'sw', 'mv'):
        gg = dict(G)
        def L(k): return list(gg[k])
        if t == 'dum': x = L(c[1]); x.insert(c[2], ('ins', 'this', D + nd, c[3])); gg[c[1]] = tuple(x); nd += 1
        elif t == 'rm': x = L(c[1]); del x[c[2]]; gg[c[1]] = tuple(x)
        elif t == 'sw': x = L(c[1]); x[c[2]], x[c[2]+1] = x[c[2]+1], x[c[2]]; gg[c[1]] = tuple(x)
        else:
            x = L(c[1]); e = x.pop(c[2]); at = c[4]
            if c[3] == c[1]:
                if at > c[2]: at -= 1
                x.insert(at, e); gg[c[1]] = tuple(x)
            else:
                gg[c[1]] = tuple(x); y = L(c[3]); y.insert(at, e); gg[c[3]] = tuple(y)
        G = tuple(gg.items())
    elif t == 'key': d = dict(ov); d[c[1]] = c[2]; ov = tuple(sorted(d.items()))
    elif t == 'pp':
        p = list(pre); ev = [p[j] for j in PP]
        for n, j in enumerate(PP): p[j] = ev[c[1][n]]
        pre = tuple(p)
    elif t == 'ph':
        p = list(pre); k = dict(ov).get(c[1], 0); p.insert(len(p) - c[2], ('push', c[1], k)); pre = tuple(p)
    return (G, ov, pre, nd)
def work(a):
    st, hist, K = a
    res = []; nsol = []
    for c in moves(st):
        ns = apply(st, c); s = score(run(ns))
        if s[0] == 0: nsol.append(hist + (c,))
        res.append((s, hash((ns[0], ns[1], ns[2])), c))
    res.sort(key=lambda x: x[0])
    return [(s, h, hist + (c,), st, c) for s, h, c in res[:K]], nsol, len(res)
if __name__ == '__main__':
    dump, mode = sys.argv[1], sys.argv[2]
    LV = int(sys.argv[3]) if len(sys.argv) > 3 else 5; W = int(sys.argv[4]) if len(sys.argv) > 4 else 300
    init(dump, mode)
    base = (tuple((k, tuple(v)) for k, v in g0.items()), (), tuple(pre0), 0)
    print('base', score(run(base)), 'nmoves', sum(1 for _ in moves(base))); sys.stdout.flush()
    pool = mp.Pool(4, init, (dump, mode)); beam = [(base, ())]; seen = set(); t0 = time.time(); nsols = 0
    for lv in range(1, LV + 1):
        cand = {}; n = 0
        for top, sols, nn in pool.imap_unordered(work, [(s, h, W) for s, h in beam], 4):
            n += nn
            for h in sols: nsols += 1; print('SOL', lv, h); sys.stdout.flush()
            for s, hh, h, st, c in top:
                if hh in seen: continue
                if hh not in cand or s < cand[hh][0]: cand[hh] = (s, h, st, c)
        best = sorted(cand.items(), key=lambda x: x[1][0])[:W]
        beam = [(apply(v[2], v[3]), v[1]) for hh, v in best]
        seen.update(hh for hh, v in best)
        print('level', lv, 'n', n, 'best', best[0][1][0] if best else None, 'worst', best[-1][1][0] if best else None, 'nsol', nsols, round(time.time() - t0))
        for hh, v in best[:5]: print('  ', v[0], v[1], run(apply(v[2], v[3]))[24:34])
        sys.stdout.flush()
        if nsols >= int(sys.argv[5] if len(sys.argv) > 5 else 200): break
