"""wi2.py: hsim-group what-if: move the round-4 ins events of 77/79 to other groups (blocks) in round 4.
python wi2.py SLOTDIR"""
import sys, copy
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s18')
import hsim
R, keys = hsim.load(sys.argv[1])
T = [35, 42, 53, 77, 79]
o = hsim.sim(R, {}, {}); print('base', [b for b in o if b in T], hsim.inv(o))
r = R[3]
src = {}
for b, evs in r['g'].items():
    for e in evs:
        if e[0] == 'ins' and e[2] in (77, 79): src[e[2]] = b
print('ins from', src, 'groups', list(r['g'].keys()))
res = {}
for ga in list(r['g'].keys()):
    for gb in list(r['g'].keys()):
        R2 = copy.deepcopy(R); g = R2[3]['g']
        ev = {}
        for b in g:
            for e in g[b]:
                if e[0] == 'ins' and e[2] in (77, 79): ev[e[2]] = e
            g[b] = [e for e in g[b] if not (e[0] == 'ins' and e[2] in (77, 79))]
        g[ga] = g[ga] + [ev[77]]; g[gb] = g[gb] + [ev[79]]
        try: o = hsim.sim(R2, {}, {})
        except Exception as x: continue
        t = tuple(b for b in o if b in T); res.setdefault(t, []).append((ga, gb, hsim.inv(o)))
for t, l in res.items(): print(t, len(l), l[:8])
