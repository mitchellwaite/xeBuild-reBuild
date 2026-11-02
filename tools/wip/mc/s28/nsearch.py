"""nsearch.py BASE.json BASETAG INJ.jsonl [K] : event-neutral realizer. Levers = injscan rows with nev==0
and nonempty df; predict f = base f + sum of deltas, simulate in hsim on BASETAG's history, rank by
true inversions; print top combos (then compile-check with ev.py)."""
import sys, os, json, itertools
R = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, os.path.join(R, r'tools\wip\mc\s18')); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hsim, pot
base = json.load(open(sys.argv[1])); bt = sys.argv[2]
K = int(sys.argv[4]) if len(sys.argv) > 4 else 3
Rr, keys = hsim.load(os.path.join(R, 'build', 'v', 'mc28', 'slot_' + bt))
f0, P0 = hsim.measured(keys)
L = []
seen = set()
for l in open(sys.argv[3]):
    x = json.loads(l)
    if x['nev'] or not x['df'] or x['dP']: continue
    d = tuple(sorted((int(k), v[1] - v[0]) for k, v in x['df'].items()))
    if d in seen: continue
    seen.add(d); L.append((x['e'], dict(d)))
print(len(L), 'levers')
res = []
for k in range(1, K + 1):
    for c in itertools.combinations(range(len(L)), k):
        sites = [L[i][0][0] for i in c]
        f = dict(f0)
        for i in c:
            for b, dv in L[i][1].items(): f[b] = f.get(b, 0) + dv
        o = hsim.sim(Rr, f, P0)
        res.append((pot.tinv(o), [L[i][0] for i in c], ' '.join(map(str, o[12:]))))
res.sort(key=lambda x: x[0])
for r in res[:15]: print(r[0], json.dumps(r[1]), r[2])
json.dump(res[:300], open('nsearch_%s.json' % bt, 'w'))
