"""combsa.py TAB.jsonl BASETAG SEED ITERS OUT.json : SA over subsets of neutral table entries (sum of f deltas),
hsim-predicted on BASETAG's history; at most one entry per injection slot (same voc site or same (label/arm))."""
import sys, os, json, random, math
R0 = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, R0 + r'\tools\wip\mc\s18'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hsim, pot
R, keys = hsim.load(os.path.join(R0, 'build', 'v', 'mc37', 'slot_' + sys.argv[2]))
f0, P0 = hsim.measured(keys)
E = {}
for l in open(sys.argv[1]):
    x = json.loads(l)
    if x['nev'] or not x['df']: continue
    k = json.dumps(x['df'], sort_keys=True)
    if k not in E or x['fncmp'] < E[k]['fncmp']: E[k] = x
E = list(E.values())
def slot(x):
    v, a = x['add']
    return json.dumps(v[0][0]) if v else json.dumps(a[0][:2])
def pred(S):
    f = dict(f0)
    for i in S:
        for b, (a, c) in E[i]['df'].items():
            b = int(b)
            if b in f and a is not None and c is not None: f[b] += c - a
    return pot.tinv(hsim.sim(R, f, P0))
random.seed(int(sys.argv[3])); S = set(); cur = pred(S); best = (cur, set()); T = 2.0; N = int(sys.argv[4])
cost = lambda S, p: p + 0.0005 * sum(E[i]["fncmp"] for i in S) + 0.05 * len(S)
for it in range(N):
    S2 = set(S); i = random.randrange(len(E))
    if i in S2: S2.remove(i)
    else:
        S2 = {j for j in S2 if slot(E[j]) != slot(E[i])}; S2.add(i)
    try: p = pred(S2)
    except Exception: continue
    if cost(S2, p) <= cost(S, cur) or random.random() < math.exp((cost(S, cur) - cost(S2, p)) / T): S, cur = S2, p
    if (cur, len(S)) < (best[0], len(best[1])): best = (cur, set(S)); print(it, cur, len(S), flush=True)
    T = max(0.05, T * (1 - 5.0 / N))
out = {'pred': best[0], 'adds': [E[i]['add'] for i in sorted(best[1])], 'df': [E[i]['df'] for i in sorted(best[1])]}
json.dump(out, open(sys.argv[5], 'w')); print(out)
