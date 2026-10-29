"""grid4.py: inject into the two send calls (39, 41) and HDD logs (40, 42) with weight combos"""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import search as S
base = [tuple(x) for x in (eval(sys.argv[1]) if len(sys.argv) > 1 else [])]
out = []
for ws, wh in itertools.product(['p', 'qq', 'q', 'b'], ['pp', 'pq', 'qq', 'p']):
    for src in ('rok', 'fail'):
        inj = base + [(39, src, ws), (41, src, ws), (40, src, wh), (42, src, wh)]
        r = S.score(inj, 'g4')
        if r is None: continue
        print(S.key(r), r['inv'], r['pre'], r['fncmp'], len(r['missing']), src, ws, wh, ' '.join(r['order'][:6]), flush=True)
