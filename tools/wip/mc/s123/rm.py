# rm.py: r4sim with extra (forwarder) blocks removed; X mid-trace -> drop its visit/ins; X trace head ->
# rename X to its trace successor Y (Y inherits X's heap entries and group), or drop if X has no successor.
import sys, itertools, difflib
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip')
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s86')
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s104')
import r4sim, srch
from ord import traces, m as PM
pre, g, first = r4sim.load('dd/mc.bbro')
base = srch.sim(pre, g); assert base == first
want = srch.sim(pre, g, {152: 1, 75: 1})
EXTRA = [142, 150, 114, 157, 117, 124, 125, 134, 136, 138, 156, 154, 105, 106, 57, 66, 127, 112, 140, 45]
EXTRA = [x for x in EXTRA if x != 142]  # 142 is the real cinfo test (mis-mapped by map.py), not extra
tp = traces('pf/mc.bbro')
prof = [PM.get(b) for t, r, bs in tp if r == 4 for b in bs[:1]]
def remove(pre, g, X):
    X = set(X); ren = {}
    for x in X:
        if x in g:
            vis = [e[1] for e in g[x] if e[0] == 'visit' and e[1] not in X]
            ren[x] = vis[0] if vis else None
    def rn(b):
        seen = 0
        while b in ren and seen < 5: b = ren[b]; seen += 1
        return b
    def fix(evs):
        out = []
        for e in evs:
            if e[0] == 'visit':
                if e[1] in X: continue
                if e[1] in ren.values(): continue  # Y is now the head itself
                out.append(e)
            elif e[0] == 'ins':
                b = rn(e[2]) if e[2] in ren else e[2]
                if b is None or b in X: continue
                out.append((e[0], e[1], b, e[3]))
            elif e[0] == 'push':
                b = rn(e[1]) if e[1] in ren else e[1]
                if b is None or b in X: continue
                out.append((e[0], b, e[2]))
            elif e[0] == 'chg':
                b = rn(e[1]) if e[1] in ren else e[1]
                if b is None or b in X: continue
                out.append((e[0], b, e[2]))
            else: out.append(e)
        return out
    p2 = fix(pre); g2 = {}
    for b, evs in g.items():
        nb = rn(b) if b in ren else b
        if nb is None: continue
        g2.setdefault(nb, []); g2[nb] = fix(evs) + g2[nb] if b in ren else g2[nb] + fix(evs)
    return p2, g2
def strip(o, X): return [b for b in o if b not in X]
def lcsd(o, t):
    sm = difflib.SequenceMatcher(None, o, t, autojunk=False); return len(t) - sum(x.size for x in sm.get_matching_blocks())
def evals(X):
    p2, g2 = remove(pre, g, X)
    try: o = srch.sim(p2, g2)
    except Exception as ex: return None
    wx = strip(want, set(X) | {None}); ox = strip(o, set(X))
    common = [b for b in prof if b in set(ox)]; oc = [b for b in ox if b in set(common)]
    i1 = (oc.index(108) > oc.index(129)) if 108 in oc and 129 in oc else None
    return lcsd(ox, wx), lcsd(oc, common), o
if __name__ == '__main__':
    b0 = evals([])
    print('base: want-dist', b0[0], 'prof-dist', b0[1])
    res = []
    for n in (1, 2, 3):
        for X in itertools.combinations(EXTRA, n):
            r = evals(X)
            if r: res.append((r[0], r[1], X, r[2]))
    print('evaluated', len(res))
    print('want-dist hits (issue 3 ref order):', [r[2] for r in res if r[0] == 0][:20])
    res.sort(key=lambda r: (r[0], r[1]))
    for r in res[:15]: print('W', r[0], 'P', r[1], r[2])
    res.sort(key=lambda r: (r[1], r[0]))
    for r in res[:15]: print('P', r[1], 'W', r[0], r[2])
    singles = [r for r in res if len(r[2]) == 1]; singles.sort(key=lambda r: r[2])
    for r in singles: print('single', r[2], 'W', r[0], 'P', r[1])
