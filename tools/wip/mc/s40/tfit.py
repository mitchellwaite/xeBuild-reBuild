"""tfit.py TAB.jsonl BASETAG 'b:d,..' SEED ITERS OUT.json: SA over subsets of neutral entries; objective =
hsim-predicted tinv + 0.5 * L1(sum df - target) (tail blocks); one entry per slot."""
import sys, os, json, random, math
R0 = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, R0 + r'\tools\wip\mc\s18'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hsim, pot
R, keys = hsim.load(os.path.join(R0, 'build', 'v', 'mc40', 'slot_' + sys.argv[2])); f0, P0 = hsim.measured(keys)
tgt = {int(a.split(':')[0]): int(a.split(':')[1]) for a in sys.argv[3].split(',') if a}
E = {}
for l in open(sys.argv[1]):
    x = json.loads(l)
    if x['nev'] or not x['df'] or any(None in v for v in x['df'].values()): continue
    k = json.dumps(x['df'], sort_keys=True)
    if k not in E or x['fncmp'] < E[k]['fncmp']: E[k] = x
E = list(E.values())
def slot(x):
    v, a = x['add']
    return json.dumps(v[0][0]) if v else json.dumps(a[0][1:2] + a[0][3:] if a[0][1] != 'top' else a[0][:1])
TB = [49, 115, 112, 103, 55, 126, 125, 61, 33, 29, 67, 127, 117, 130, 35, 42, 53, 77, 79]
def fof(S):
    f = dict(f0)
    for i in S:
        for b, (a, c) in E[i]['df'].items():
            if int(b) in f: f[int(b)] += c - a
    return f
def obj(S):
    f = fof(S); p = pot.tinv(hsim.sim(R, f, P0))
    d = sum(abs(f[b] - f0[b] - tgt.get(b, 0)) for b in TB if b in f)
    return W[0] * p + 0.5 * d + 0.0005 * sum(E[i]['fncmp'] for i in S), p
W = [0.05]
random.seed(int(sys.argv[4])); S = set(); cur, cp = obj(S); best = (99, 1e9, set()); T = 3.0; N = int(sys.argv[5])
for it in range(N):
    S2 = set(S); i = random.randrange(len(E))
    if i in S2: S2.remove(i)
    else: S2 = {j for j in S2 if slot(E[j]) != slot(E[i])}; S2.add(i)
    W[0] = min(1.0, 0.05 + 1.5 * it / N); cur = obj(S)[0] if it % 500 == 0 else cur
    try: o, p = obj(S2)
    except Exception: continue
    if o <= cur or random.random() < math.exp((cur - o) / T): S, cur, cp = S2, o, p
    if W[0] >= 1.0 and (cur, cp) < (best[1], best[0]): best = (cp, cur, set(S)); print(it, cp, round(cur, 2), len(S), flush=True)
    T = max(0.05, T * (1 - 5.0 / N))
out = {'pred': best[0], 'adds': [E[i]['add'] for i in sorted(best[2])]}
json.dump(out, open(sys.argv[6], 'w')); print(out['pred'], len(out['adds']))
