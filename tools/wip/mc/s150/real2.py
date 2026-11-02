# real2.py DUMP [levels] [width] : beam over dummies (any key) + early insertion of existing blocks
# with the back-edge filter: a post-loop source may not target an arg-loop block (f2 ~790, s150).
# Positions right after a trace-end re-key (chg) are excluded: gcc can't insert there.
import sys, re, time, multiprocessing as mp
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s86'); import r4sim
D = 9999; LOOP = (593, 724)
def init(dump):
    global pre, g, first, TGT, KEY, INL, CH
    pre, g, first = r4sim.load(dump)
    import os
    T = [int(x) for x in os.environ.get('TAILT', '147,128,150,35,42,53,79,81').split(',')]
    i = min(first.index(x) for x in T)
    TGT = first[:i] + T + first[i+len(T):]
    t = open(dump).read(); a = t.find('Reordered sequence:'); b = t.find('basic blocks,', a); s = t[b:]
    INL = {}
    for m in re.finditer(r'^\s*(\d+) bb (\d+)\s', t[a:b], re.M):
        c, o = m.group(1), int(m.group(2))
        x = re.search(r'\(note \d+ \d+ \d+ %s \[bb %s\] NOTE_INSN_BASIC_BLOCK\)(.*?)(?=\n;; bb \d+ artificial_defs|\Z)' % (c, c), s, re.S)
        ln = [int(v) for v in re.findall(r'\.c:(\d+)', x.group(1))] if x else []
        INL[o] = bool(ln) and all(LOOP[0] <= v <= LOOP[1] for v in ln)
    KEY = {}
    for G in g.values():
        for e in G:
            if e[0] == 'ins': KEY[e[2]] = e[3]
    CH = []
    for G in first:
        cur = None
        for at, e in enumerate(g[G]):
            if e[0] == 'visit': cur = e[1]
            if e[0] == 'chg': continue
            for k in (0, -1, -2, -3): CH.append(('dum', G, at + 1, k))
            for b2 in first:
                if b2 == G or b2 not in KEY or KEY[b2] < -4 or str(b2) in os.environ.get('NOEI', '').split(','): continue
                if INL.get(b2) and not INL.get(cur): continue
                CH.append(('ei', G, at + 1, b2))
def sc(o):
    o = [b for b in o if b < D]; return sum(a != b for a, b in zip(o, TGT)) + abs(len(o) - len(TGT))
def run(cs):
    gg = dict(g)
    for n, c in sorted(enumerate(cs), key=lambda x: (-x[1][2], x[0])):
        L = list(gg[c[1]])
        L.insert(c[2], ('ins', 'this', D + 1 + n, c[3]) if c[0] == 'dum' else ('ins', 'this', c[3], KEY[c[3]]))
        gg[c[1]] = L
    try: return sc(r4sim.sim(pre, gg, {}))
    except Exception: return 99
def work(cs):
    out = []
    for c in CH:
        if c in cs: continue
        n = tuple(sorted(cs + (c,))); out.append((run(list(n)), n))
    out.sort(key=lambda x: x[0])
    return [x for x in out if x[0] == 0], out[:600]
if __name__ == '__main__':
    d = sys.argv[1]; LV = int(sys.argv[2]); W = int(sys.argv[3]); init(d)
    print('nch', len(CH), 'inloop', sorted(b for b, v in INL.items() if v)[:40]); sys.stdout.flush()
    pool = mp.Pool(3, init, (d,)); beam = [()]; sol = set(); t = time.time()
    for lv in range(1, LV + 1):
        cand = {}
        for s0, top in pool.imap_unordered(work, beam, 2):
            for s, x in s0:
                if x not in sol: sol.add(x); print('SOL', lv, x); sys.stdout.flush()
            for s, x in top: cand[x] = s
        best = sorted(cand.items(), key=lambda x: x[1])[:W]; beam = [x for x, s in best]
        print('level', lv, 'best', best[0], 'worst', best[-1][1], 'nsol', len(sol), round(time.time() - t)); sys.stdout.flush()
        if sol: break
