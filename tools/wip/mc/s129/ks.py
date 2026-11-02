import sys, itertools
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s86')
import r4sim
pre, g, first = r4sim.load('d_pm/mc.bbro')
T = [112,115,103,55,126,125,61,33,29,67,127,130,117]
def score(o):
    o = o[o.index(49)+1:]
    o = o[:o.index(67)+5]
    import difflib
    sm = difflib.SequenceMatcher(None, o, T + o[o.index(67)+4:] if False else T)
    return len(T) - sum(b.size for b in sm.get_matching_blocks())
BL = [103,112,115,125,126,127,130,117,33,29,53,55,61]
res = []
for n in (1, 2):
    for bs in itertools.combinations(BL, n):
        for ks in itertools.product(range(-6, 1), repeat=n):
            ov = dict(zip(bs, ks))
            try: o = r4sim.sim(pre, g, ov)
            except Exception: continue
            res.append((score(o), ov, o))
res.sort(key=lambda x: x[0])
print('base', score(r4sim.sim(pre, g, {})))
for s, ov, o in res[:15]: print(s, ov, o[o.index(49)+1:o.index(49)+20])
