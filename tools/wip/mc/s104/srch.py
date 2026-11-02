# srch.py: abstract-edit search over r4sim (key overrides + dummy zero-byte heap insertions)
import sys, itertools
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip')
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s86')
import fibsim, r4sim
D0 = 9000
def sim(pre, groups, ov={}, dum={}):
    # dum: {('p',idx): key} insert into next-round heap before pre[idx]; {(blk,j): key} insert into round-4 heap before groups[blk][j]
    heap = fibsim.Heap(); loc = {2: (heap, heap.insert(0, 2))}; new = None; nd = [D0]
    def dummy(h, k):
        nd[0] += 1; loc[nd[0]] = (h, h.insert(k, nd[0]))
    for idx, e in enumerate(pre):
        if ('p', idx) in dum and new is not None: dummy(new, dum[('p', idx)])
        if e[0] == 'round':
            if new is not None: heap = new
            new = fibsim.Heap()
        elif e[0] == 'get':
            heap.extract_min(); loc.pop(e[1], None)
        elif e[0] == 'visit':
            if e[1] in loc: h, n = loc.pop(e[1]); h.delete_node(n)
        elif e[0] == 'ins':
            h = heap if e[1] == 'this' else new
            k = ov.get(e[2], e[3]) if h is new else e[3]
            loc[e[2]] = (h, h.insert(k, e[2]))
        elif e[0] == 'push':
            loc[e[1]] = (new, new.insert(ov.get(e[1], e[2]), e[1]))
        elif e[0] == 'chg':
            h, n = loc[e[1]]; k = ov.get(e[1], e[2]) if h is new else e[2]
            loc[e[1]] = (h, h.replace_key(n, k))
    if ('p', len(pre)) in dum: dummy(new, dum[('p', len(pre))])
    heap = new; loc = {b: v for b, v in loc.items() if v[0] is heap}
    vis = set(); order = []
    while heap.min is not None:
        z = heap.extract_min(); b = z.data; loc.pop(b, None)
        if b in vis: continue
        vis.add(b)
        if b > D0: continue
        order.append(b)
        for j, e in enumerate(groups.get(b, [])):
            if (b, j) in dum: dummy(heap, dum[(b, j)])
            if e[0] == 'visit':
                vis.add(e[1])
                if e[1] in loc: h, n = loc.pop(e[1]); h.delete_node(n)
            elif e[0] == 'ins':
                if e[2] in vis: continue
                if e[2] in loc:
                    k = ov.get(e[2], e[3]); h, n = loc[e[2]]
                    if n.key != k: loc[e[2]] = (h, h.replace_key(n, k))
                    continue
                loc[e[2]] = (heap, heap.insert(ov.get(e[2], e[3]), e[2]))
            elif e[0] == 'chg':
                if e[1] in loc:
                    h, n = loc[e[1]]; loc[e[1]] = (h, h.replace_key(n, ov.get(e[1], e[2])))
    return order
T = list(map(int, '142 113 116 119 122 134 115 129 131 141 126 147 105 49 125 121 108 55 139 138 62 33 29 69 140 127 145 35 42 53 79 81 75 83 88 154 97 155 98 93 95'.split()))
def dist(o):
    # number of blocks out of place (LCS-based)
    import difflib
    sm = difflib.SequenceMatcher(None, o, T, autojunk=False)
    return len(T) - sum(m.size for m in sm.get_matching_blocks())
if __name__ == '__main__':
    pre, g, first = r4sim.load(sys.argv[1])
    base = sim(pre, g); print('base', dist(base), base == first)
    blocks = sorted(set(first) | {141, 139, 145, 138, 140, 127, 55, 108})
    keys = list(range(-12, 2)) + [-1000000]
    pts = [('p', i) for i in range(len(pre) - 40, len(pre) + 1)] + [(b, j) for b in g for j in range(len(g[b]) + 1)]
    res = []
    for b in blocks:
        for k in keys: res.append((dist(sim(pre, g, {b: k})), 'ov', b, k))
    for p in pts:
        for k in (-12, -8, -5, -4, -3, -2, -1, 0, 1):
            res.append((dist(sim(pre, g, {}, {p: k})), 'dum', p, k))
    res.sort(key=lambda r: r[0])
    for r in res[:25]: print(r)
    single = [r for r in res if r[0] < dist(base)]
    print('improving singles', len(single))
    best = []
    for a, c in itertools.combinations(single[:120], 2):
        if a[1] == 'ov' and c[1] == 'ov' and a[2] == c[2]: continue
        ov = {}; du = {}
        for r in (a, c):
            (ov if r[1] == 'ov' else du)[r[2]] = r[3]
        o = sim(pre, g, ov, du); best.append((dist(o), a[1:], c[1:]))
    best.sort(key=lambda r: r[0])
    for r in best[:25]: print(r)
