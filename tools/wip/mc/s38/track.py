"""track.py TAB.jsonl BASETAG STATE.json TARGET('b:v,..') SEED ITERS OUT.json : SA over neutral table subsets minimizing
L1(f_pred - TARGET) + 0.3*tinv_pred; realize best 4 subsets, keep the real one with least measured L1 (+inv)."""
import sys, os, json, random, math, copy
os.environ['DUP'] = '1'; os.environ['LU'] = '1'
R0 = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, R0 + r'\tools\wip\mc\s18'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hsim, pot
R, keys = hsim.load(os.path.join(R0, 'build', 'v', 'mc38', 'slot_' + sys.argv[2])); f0, P0 = hsim.measured(keys)
TG = {int(a.split(':')[0]): int(a.split(':')[1]) for a in sys.argv[4].split(',')}
E = {}
for l in open(sys.argv[1]):
    x = json.loads(l)
    if x['nev'] or not x['df'] or any(None in v for v in x['df'].values()): continue
    k = json.dumps(x['df'], sort_keys=True)
    if k not in E or x['fncmp'] < E[k]['fncmp']: E[k] = x
E = list(E.values())
def slot(x):
    v, a, e = x['add']
    if v: return 'v' + json.dumps(v[0][0])
    if a: return 'a' + json.dumps(a[0][:3])
    return 'e' + e[0][0]
def fpred(S):
    f = dict(f0)
    for i in S:
        for b, (a, c) in E[i]['df'].items():
            b = int(b)
            if b in f: f[b] += c - a
    return f
def L1(f): return sum(abs(f.get(b, 0) - v) for b, v in TG.items()) + sum(max(0, f[b] - f0[b]) for b in f if b not in TG and b < 140 and b in (107,108,110,113,116,119,120,121,128,129,132))
def cost(S):
    f = fpred(S); return L1(f) + 0.3 * pot.tinv(hsim.sim(R, f, P0)) + 0.001 * sum(E[i]['fncmp'] for i in S)
random.seed(int(sys.argv[5])); S = set(); cur = cost(S); T = 2.0; N = int(sys.argv[6]); top = {}
for it in range(N):
    S2 = set(S); i = random.randrange(len(E))
    if i in S2: S2.remove(i)
    else: S2 = {j for j in S2 if slot(E[j]) != slot(E[i])}; S2.add(i)
    try: c = cost(S2)
    except Exception: continue
    if c <= cur or random.random() < math.exp((cur - c) / T): S, cur = S2, c
    top[frozenset(S)] = cur
    T = max(0.05, T * (1 - 5.0 / N))
cand = sorted(top.items(), key=lambda z: z[1])[:4]
print('L1 start', L1(f0), 'cands', [(round(c, 2), len(s), L1(fpred(s))) for s, c in cand], flush=True)
import gs2, ev
res = []
for Sx, c in cand:
    st = copy.deepcopy(json.load(open(sys.argv[3]))); st.setdefault('e', [])
    nn = max([x[3] for x in st['a'] + st['e']] + [0]) + 10
    for i in sorted(Sx):
        v, a, e = copy.deepcopy(E[i]['add'])
        for x in a + e: x[3] = nn; nn += 10
        st['v'] += v; st['a'] += a; st['e'] += e
    tag = 'tr%s' % sys.argv[5]
    r = ev.ev(gs2.build(st), tag, True)
    if not r: continue
    try: Rx, kx = hsim.load(os.path.join(R0, 'build', 'v', 'mc38', 'slot_' + tag)); fx, _ = hsim.measured(kx)
    except Exception: continue
    m = L1(fx); print('cand', round(c, 2), 'predL1', L1(fpred(Sx)), 'REAL L1', m, 'inv', r['score'], r['fncmp'], ' '.join(map(str, r['o'][12:])), flush=True)
    res.append((m + 0.3 * r['score'], r['score'], r['fncmp'], st))
res.sort(key=lambda z: z[:3])
if res: json.dump(res[0][3], open(sys.argv[7], 'w')); print('BEST', res[0][:3])
