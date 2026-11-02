"""potscan.py TAB.jsonl BASE.json OUT.jsonl [MAXSCORE]: for each event-changing table entry, realize it and run an
hsim f-SA (L1-penalised) on its own history -> potential (min inv at small L1)."""
import sys, os, json, random, math, copy
os.environ['DUP'] = '1'; os.environ['LU'] = '1'
R0 = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, R0 + r'\tools\wip\mc\s18'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from concurrent.futures import ProcessPoolExecutor
BLX = [49, 115, 112, 103, 55, 126, 125, 61, 33, 29, 67, 127, 117, 130, 35, 42, 53, 77, 79]
def fsa(R, f0, P0, iters, LW, seed):
    import hsim, pot
    BL = [b for b in BLX if b in f0]
    random.seed(seed)
    def L(f): return sum(abs(f[b] - f0[b]) for b in BL)
    f = dict(f0); cur = pot.tinv(hsim.sim(R, f, P0)); best = (cur, 0, dict(f)); T = 2.0
    for it in range(iters):
        g = dict(f); b = random.choice(BL); g[b] = max(0, min(12, g[b] + random.choice([-1, 1])))
        try: s = pot.tinv(hsim.sim(R, g, P0))
        except Exception: continue
        d = (s + LW * L(g)) - (cur + LW * L(f))
        if d <= 0 or random.random() < math.exp(-d / T): f, cur = g, s
        if (cur, L(f)) < best[:2]: best = (cur, L(f), dict(f))
        T = max(0.05, T * (1 - 4.0 / iters))
    return best
def job(x):
    i, st, info = x
    import gs2, ev, hsim
    tag = 'ps%d' % __import__('tt').tid()
    try: r = ev.ev(gs2.build(st), tag, True)
    except Exception: return None
    if r is None: return None
    try:
        R, k = hsim.load(os.path.join(R0, 'build', 'v', 'mc40', 'slot_' + tag)); f0, P0 = hsim.measured(k)
        b = min(fsa(R, f0, P0, 6000, 0.25, s) for s in (1, 2))
    except Exception as e: return None
    return {'i': i, 'add': info, 'score': r['score'], 'fncmp': r['fncmp'], 'o': ' '.join(map(str, r['o'][12:])),
            'pinv': b[0], 'pL1': b[1], 'pdf': {str(k): (f0[k], v) for k, v in b[2].items() if f0.get(k) != v}}
if __name__ == '__main__':
    base = json.load(open(sys.argv[2])); MS = int(sys.argv[4]) if len(sys.argv) > 4 else 40
    J = []
    for i, l in enumerate(open(sys.argv[1])):
        x = json.loads(l)
        if not x['nev'] or x['score'] > MS: continue
        st = copy.deepcopy(base); v, a, e = x['add']; st['v'] += v; st['a'] += a; st.setdefault('e', []); st['e'] += e
        J.append((i, st, x['add']))
    print('jobs', len(J), flush=True)
    out = open(sys.argv[3], 'a', newline='\n')
    with ProcessPoolExecutor(4) as ex:
        for r in ex.map(job, J):
            if r: out.write(json.dumps(r) + '\n'); out.flush()
