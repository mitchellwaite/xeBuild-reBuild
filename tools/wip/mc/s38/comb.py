"""comb.py TAB.jsonl BASETAG STATE.json OUT.json [K]: predict sets of <=K neutral table entries (sum of f deltas)
on BASETAG's history with hsim; exhaustive over pairs/triples of distinct-effect entries; writes top predicted sets."""
import sys, os, json, itertools
R0 = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, R0 + r'\tools\wip\mc\s18'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hsim, pot
R, keys = hsim.load(os.path.join(R0, 'build', 'v', 'mc38', 'slot_' + sys.argv[2]))
f0, P0 = hsim.measured(keys)
L = [json.loads(l) for l in open(sys.argv[1])]
E = {}
for x in L:
    if x['nev'] or not x['df']: continue
    k = json.dumps(x['df'], sort_keys=True)
    if k not in E or x['fncmp'] < E[k]['fncmp']: E[k] = x
E = list(E.values()); print('entries', len(E))
K = int(sys.argv[5]) if len(sys.argv) > 5 else 3
def pred(S):
    f = dict(f0)
    for x in S:
        for b, (a, c) in x['df'].items():
            b = int(b)
            if b in f and a is not None and c is not None: f[b] += c - a
    # same-site conflicts: two arm injections at the same (arm,n) or same voc site
    return pot.tinv(hsim.sim(R, f, P0))
res = []
for k in range(1, K + 1):
    for S in itertools.combinations(range(len(E)), k):
        sites = [json.dumps(E[i]['add']) for i in S]
        try: p = pred([E[i] for i in S])
        except Exception: continue
        res.append((p, sum(E[i]['fncmp'] for i in S), [E[i]['add'] for i in S]))
res.sort(key=lambda z: (z[0], z[1])); print('best preds', [r[0] for r in res[:20]])
json.dump(res[:300], open(sys.argv[4], 'w'))
