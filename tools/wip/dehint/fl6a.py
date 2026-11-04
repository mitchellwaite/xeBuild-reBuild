"""fl6a.py [drops ...]: every single natural edit (fl6lib.E), and pairs, at given drop sets."""
import itertools, sys
import fl6lib as F

DROPS = sys.argv[2:] or ['', 'T1,T3', 'T1,T2,T3', 'T2,T3', 'T1,T2']
mode = sys.argv[1] if len(sys.argv) > 1 else 'single'
V = {}
axes = [(a, v) for a in F.E for v in F.E[a]]
for d in DROPS:
    V[d + '|'] = F.state(d + '|')
    for a, v in axes:
        lb = '%s|%s=%s' % (d, a, v)
        try:
            V[lb] = F.state(lb)
        except Exception as e:
            print('skip', lb, e)
    if mode == 'pair':
        for (a, v), (b, w) in itertools.combinations(axes, 2):
            if a == b or {a, b} == {'copy', 'adv'}:
                continue
            lb = '%s|%s=%s,%s=%s' % (d, a, v, b, w)
            try:
                V[lb] = F.state(lb)
            except Exception:
                pass
print(len(V))
F.run(V, 'a_' + mode, 40)
