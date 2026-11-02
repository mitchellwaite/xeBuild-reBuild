"""hq.py TAG 'b:v1,v2;b2:...' : exhaustive hsim over listed f values on slot_TAG's history (true inv)."""
import sys, os, itertools
R = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, os.path.join(R, r'tools\wip\mc\s18')); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hsim, ev
Rr, keys = hsim.load(os.path.join(R, 'build', 'v', 'mc28', 'slot_' + sys.argv[1]))
f0, P0 = hsim.measured(keys)
spec = [(int(a.split(':')[0]), [int(v) for v in a.split(':')[1].split(',')]) for a in sys.argv[2].split(';')]
def tinv(o):
    inv, miss, oo = ev.score_order([str(b) for b in o]); return inv + 5 * len([b for b in miss if b not in ev.CASES])
res = []
for vals in itertools.product(*[v for b, v in spec]):
    f = dict(f0)
    for (b, _), v in zip(spec, vals): f[b] = v
    o = hsim.sim(Rr, f, P0); res.append((tinv(o), vals, ' '.join(map(str, o[11:]))))
res.sort()
print('base', f0.get(112), f0.get(103), [b for b, v in spec])
for r in res[:10]: print(r)
