# real3.py DUMP "ign ids" "target ids" [levels] [width] : beam for the whole r4 order with zero-byte blocks ignored;
# moves: dum (key 0..-3), ei (b's key), rm (op inserting an ignored block). Solution line says whether a zero-byte
# block sits right before block ALIGN (env, default none), which keeps that label unaligned (prev freq rule).
import sys, os, time, multiprocessing as mp
sys.path.insert(0, r'C:/Users/Win11VM/Documents/GitHub/xebuildBugFix/tools/wip/mc/s86'); import r4sim
D = 9000
def init(dump, ign, tgt):
    global pre, g, first, IGN, TGT, CH, KEY, AL
    pre, g, first = r4sim.load(dump); IGN = set(ign); TGT = tgt; AL = int(os.environ.get('ALIGN', '-1'))
    KEY = {e[2]: e[3] for G in g.values() for e in G if e[0] == 'ins'}
    CH = []
    for G in first:
        for at, e in enumerate(g[G]):
            if e[0] == 'chg': continue
            for k in (0, -1, -2, -3): CH.append(('dum', G, at + 1, k))
            if os.environ.get('EI'):
                for b in first:
                    if b != G and b in KEY and KEY[b] >= -4 and b not in IGN: CH.append(('ei', G, at + 1, b))
            if e[0] == 'ins' and e[2] in IGN: CH.append(('rm', G, at))
    if os.environ.get('PR'):
        ir = max(j for j, e in enumerate(pre) if e[0] == 'round')
        for j in range(ir + 1, len(pre) + 1):
            if pre[j-1][0] in ('visit', 'ins', 'push'):
                for k in (0, -1, -2, -3): CH.append(('pd', 0, j, k))
DK = {}; NZ = set(int(x) for x in os.environ.get('NZ','').split())
def seq(cs):
    DK.clear()
    for n, c in enumerate(sorted(enumerate(cs), key=lambda x: (-x[1][2], x[0]))):
        if c[1][0] in ('dum','pd'): DK[D + c[0]] = c[1][3]
    gg = dict(g); ch = sorted(enumerate(cs), key=lambda x: (-x[1][2], x[0])); pp = pre
    for n, c in ch:
        if c[0] == 'pd':
            pp = list(pp); pp.insert(c[2], ('push', D + n, c[3])); continue
        L = list(gg[c[1]])
        if c[0] == 'rm': del L[c[2]]
        else: L.insert(c[2], ('ins', 'this', D + n, c[3]) if c[0] == 'dum' else ('ins', 'this', c[3], KEY[c[3]]))
        gg[c[1]] = L
    try: return r4sim.sim(pp, gg, {})
    except Exception: return []
def sc(o):
    o = [b for b in o if b < D and b not in IGN]; return sum(a != b for a, b in zip(o, TGT)) + abs(len(o) - len(TGT))
def alok(o):
    if AL < 0 or AL not in o: return True
    i = o.index(AL); return (o[i-1] >= D and DK.get(o[i-1],0) < 0) or o[i-1] in NZ
def work(cs):
    out = []; sol = []
    for c in CH:
        if c in cs: continue
        n = tuple(sorted(cs + (c,))); o = seq(list(n)); s = sc(o)
        if s == 0: sol.append((alok(o), n, o))
        out.append((s, n))
    out.sort(key=lambda x: x[0]); return sol, out[:600]
if __name__ == '__main__':
    d = sys.argv[1]; ign = [int(x) for x in sys.argv[2].split()]; tgt = [int(x) for x in sys.argv[3].split()]
    LV = int(sys.argv[4]); W = int(sys.argv[5]); init(d, ign, tgt)
    o = seq([]); print('base', sc(o), 'nch', len(CH)); print(o); print(tgt); sys.stdout.flush()
    pool = mp.Pool(4, init, (d, ign, tgt)); beam = [()]; seen = set(); t = time.time(); nal = 0
    for lv in range(1, LV + 1):
        cand = {}
        for sol, top in pool.imap_unordered(work, beam, 2):
            for a, n, o in sol:
                if n not in seen:
                    seen.add(n); nal += a
                    if a or len(seen) < 50: print('SOL', lv, 'ALIGN_OK' if a else '-', n); sys.stdout.flush()
            for s, x in top: cand[x] = s
        best = sorted(cand.items(), key=lambda x: x[1])[:W]; beam = [x for x, s in best]
        print('level', lv, 'best', best[0], 'worst', best[-1][1], 'nsol', len(seen), 'alignok', nal, round(time.time() - t)); sys.stdout.flush()
        if nal >= 60: break
