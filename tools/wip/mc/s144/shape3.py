# shape3.py DUMP : dummy-free, source-translatable edits only: reorder the inserts inside one trace group
# (successor-edge order) for any r4 group, and 146 key -1/0. Exhaustive over 1-3 group permutations.
import sys, itertools
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s86'); import r4sim
pre, g, first = r4sim.load(sys.argv[1])
T = list(map(int, "62 33 29 69 146 128 151 35 42 53 79 81".split()))
i143 = first.index(143); PREF = first[:i143+1]
def score(o):
    if 143 not in o: return 99
    s = sum(a != b for a, b in zip(o[:i143+1], PREF)); j = o.index(143)
    return s + sum(a != b for a, b in zip(o[j+1:j+1+len(T)], T))
opts = []
for b in first:
    ins = [e for e in g[b] if e[0] == 'ins']
    if len(ins) < 2: continue
    oth = [e for e in g[b] if e[0] != 'ins']
    for p in itertools.permutations(ins):
        if list(p) != ins: opts.append((b, list(p) + oth))
k146 = [-1, 0]
res = []
for n in range(0, 3):
    for combo in itertools.combinations(opts, n):
        if len({c[0] for c in combo}) < n: continue
        gg = dict(g)
        for b, L in combo: gg[b] = L
        for k in k146:
            for b in gg:
                gg[b] = [('ins', 'this', 146, k) if (e[0] == 'ins' and e[2] == 146) else e for e in gg[b]]
            try: o = r4sim.sim(pre, gg, {})
            except Exception: continue
            res.append((score(o), k, [(c[0], [e[2] for e in c[1] if e[0] == 'ins']) for c in combo], o[i143+1:i143+13]))
res.sort(key=lambda r: r[0]); print(len(opts), len(res))
for r in res[:10]: print(r)
