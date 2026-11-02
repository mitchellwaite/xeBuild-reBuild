"""fit.py TAB.jsonl BASETAG STATE.json SEED ITERS OUT.json [K]: SA over subsets of neutral table entries (hsim-predicted),
then realize the best K distinct predicted-0..2 subsets (real compile, unique n) and report."""
import sys, os, json, random, math, copy
os.environ['DUP'] = '1'; os.environ['LU'] = '1'
R0 = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, R0 + r'\tools\wip\mc\s18'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hsim, pot
R, keys = hsim.load(os.path.join(R0, 'build', 'v', 'mc35', 'slot_' + sys.argv[2])); f0, P0 = hsim.measured(keys)
E = {}
for l in open(sys.argv[1]):
    x = json.loads(l)
    if x['nev'] or not x['df'] or any(None in v for v in x['df'].values()): continue
    k = json.dumps(x['df'], sort_keys=True)
    if k not in E or x['fncmp'] < E[k]['fncmp']: E[k] = x
E = list(E.values()); print('entries', len(E))
def slot(x):
    v, a, e = x['add']
    if v: return 'v' + json.dumps(v[0][0])
    if a: return 'a' + json.dumps(a[0][:3] if os.environ.get('NOSLOT') else a[0][:2])
    return 'e' + e[0][0]
def fpred(S):
    f = dict(f0)
    for i in S:
        for b, (a, c) in E[i]['df'].items():
            b = int(b)
            if b in f: f[b] += c - a
    return f
def pred(S): return pot.tinv(hsim.sim(R, fpred(S), P0))
random.seed(int(sys.argv[4])); S = set(); cur = pred(S); found = {}; T = 2.0; bst = 99; TH = int(os.environ.get('TH', '2')); N = int(sys.argv[5])
cost = lambda S, p: p + 0.0005 * sum(E[i]["fncmp"] for i in S) + 0.1 * len(S)
for it in range(N):
    S2 = set(S); i = random.randrange(len(E))
    if i in S2: S2.remove(i)
    else: S2 = {j for j in S2 if slot(E[j]) != slot(E[i])}; S2.add(i)
    try: p = pred(S2)
    except Exception: continue
    if cost(S2, p) <= cost(S, cur) or random.random() < math.exp((cost(S, cur) - cost(S2, p)) / T): S, cur = S2, p
    if cur <= TH: found[frozenset(S)] = cur
    if cur < bst: bst = cur; print(it, 'best', cur, len(S), flush=True)
    T = max(0.05, T * (1 - 5.0 / N))
cand = sorted(found.items(), key=lambda z: (z[1], len(z[0])))[:int(sys.argv[7]) if len(sys.argv) > 7 else 5]
print('found', len(found), [(c, len(s)) for s, c in cand], flush=True)
import gs2, ev
res = []
for k, (Sx, p) in enumerate(cand):
    st = copy.deepcopy(json.load(open(sys.argv[3]))); st.setdefault('e', [])
    nn = 300
    for i in sorted(Sx):
        v, a, e = copy.deepcopy(E[i]['add'])
        for x in a: x[3] = nn; nn += 10
        for x in e: x[3] = nn; nn += 10
        st['v'] += v; st['a'] += a; st['e'] += e
    r = ev.ev(gs2.build(st), 'fit%s' % sys.argv[4], True)
    print('cand', p, len(Sx), 'REAL', r and r['score'], r and r['fncmp'], r and ' '.join(map(str, r['o'][12:])), flush=True)
    if r: res.append((r['score'], r['fncmp'], st))
res.sort(key=lambda z: z[:2])
if res: json.dump(res[0][2], open(sys.argv[6], 'w')); print('BEST', res[0][:2])
