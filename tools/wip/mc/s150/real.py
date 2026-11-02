# real.py DUMP [levels] [width] : beam restricted to source-realisable r4 changes on a swapped base
# (dump of sw.c: t6 with asm goto r5x,r3x so 81 is inserted before 79).
#   dum: zero-byte dead block (asm volatile + unreachable) JMP'ed from a freq-0 source -> key 0 entry
#        at any op position inside that source block's segment of the trace; same dz may be used once
#   ei : early insertion of an existing block b by an edge from a freq-0 source (b's own key kept)
#   sw : swap two adjacent ins ops of one source block (asm goto label order)
# Sources: blocks printed with [0] in the round-4 trace lines. Prints every 0 solution.
import sys, re, time, multiprocessing as mp
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s86'); import r4sim
D = 9999
def init(dump):
    global pre0, g0, first, TGT, F0, KEY, POSN, FREQ
    pre0, g0, first = r4sim.load(dump)
    i = first.index(150)
    TGT = first[:i] + [147,128,150,35,42,53,79,81] + first[i+8:]
    POSN = {b: n for n, b in enumerate(TGT)}
    t = open(dump).read(); FREQ = {}
    for l in re.findall(r'^Trace \d+ \(round \d+\):(.*)$', t, re.M):
        for b, f in re.findall(r'(\d+) \[(\d+)\]', l): FREQ[int(b)] = int(f)
    F0 = {b for b, f in FREQ.items() if f == 0}
    KEY = {}
    for G in g0.values():
        for e in G:
            if e[0] == 'ins': KEY[e[2]] = e[3]
def score(o):
    o = [b for b in o if b < D]
    h = sum(a != b for a, b in zip(o, TGT)) + abs(len(o) - len(TGT))
    if h == 0: return (0, 0)
    p = [POSN.get(b, 999) for b in o]
    return (h, sum(p[i] > p[j] for i in range(len(p)) for j in range(i+1, min(i+12, len(p)))))
def run(st):
    try: return r4sim.sim(pre0, {k: list(v) for k, v in st[0]}, {})
    except Exception: return []
def moves(st):
    G, nd = st
    for k, L in G:
        cur = None
        for j, e in enumerate(L):
            if e[0] == 'visit': cur = e[1]
            if cur in F0:
                # position j+1 lies in cur's segment (before the next visit)
                if nd < 4: yield ('dum', k, j + 1, cur)
                for b in first:
                    if b == cur or b == k or b not in KEY or KEY[b] < -4: continue
                    yield ('ei', k, j + 1, cur, b)
            if j + 1 < len(L) and e[0] == 'ins' and L[j+1][0] == 'ins':
                yield ('sw', k, j)
def apply(st, c):
    G, nd = st; gg = dict(G); x = list(gg[c[1]])
    if c[0] == 'dum': x.insert(c[2], ('ins', 'this', D + nd, 0)); nd += 1
    elif c[0] == 'ei': x.insert(c[2], ('ins', 'this', c[4], KEY[c[4]]))
    elif c[0] == 'sw': x[c[2]], x[c[2]+1] = x[c[2]+1], x[c[2]]
    gg[c[1]] = tuple(x)
    return (tuple(gg.items()), nd)
def work(a):
    st, hist, K = a; res = []; sols = []
    for c in moves(st):
        ns = apply(st, c); s = score(run(ns))
        if s[0] == 0: sols.append(hist + (c,))
        res.append((s, hash(ns[0]), c))
    res.sort(key=lambda x: x[0])
    return [(s, h, hist + (c,), st, c) for s, h, c in res[:K]], sols, len(res)
if __name__ == '__main__':
    dump = sys.argv[1]; LV = int(sys.argv[2]) if len(sys.argv) > 2 else 5; W = int(sys.argv[3]) if len(sys.argv) > 3 else 300
    init(dump)
    base = (tuple((k, tuple(v)) for k, v in g0.items()), 0)
    print('base', score(run(base)), 'nmoves', sum(1 for _ in moves(base)), 'f0', sorted(F0)); sys.stdout.flush()
    pool = mp.Pool(3, init, (dump,)); beam = [(base, ())]; seen = set(); t0 = time.time(); ns = 0
    for lv in range(1, LV + 1):
        cand = {}; n = 0
        for top, sols, nn in pool.imap_unordered(work, [(s, h, W) for s, h in beam], 4):
            n += nn
            for h in sols:
                ns += 1
                if ns <= 300: print('SOL', lv, h); sys.stdout.flush()
            for s, hh, h, st, c in top:
                if hh in seen: continue
                if hh not in cand or s < cand[hh][0]: cand[hh] = (s, h, st, c)
        best = sorted(cand.items(), key=lambda x: x[1][0])[:W]
        beam = [(apply(v[2], v[3]), v[1]) for hh, v in best]
        seen.update(hh for hh, v in best)
        print('level', lv, 'n', n, 'best', best[0][1][0] if best else None, 'worst', best[-1][1][0] if best else None, 'nsol', ns, round(time.time() - t0))
        for hh, v in best[:6]: print('  ', v[0], v[1], run(apply(v[2], v[3]))[24:34])
        sys.stdout.flush()
        if ns: break
