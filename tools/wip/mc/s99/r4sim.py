import sys, os
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip')
import fibsim
def load(dump):
    ev = fibsim.parse(dump)
    i4 = ev.index(('round', 4)); pre = ev[:i4]
    groups = {}; cur = None; first = []
    for e in ev[i4+1:]:
        if e[0] == 'get': cur = e[1]; groups.setdefault(cur, []); first.append(cur); continue
        groups[cur].append(e)
    return pre, groups, first
def sim(pre, groups, ov={}, extra_first=()):
    # replay rounds 1-3 exactly up to round 4 with key overrides on 'next' pushes/chg
    heap = fibsim.Heap(); loc = {2: (heap, heap.insert(0, 2))}; new = None
    for e in pre:
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
    heap = new; loc = {b: v for b, v in loc.items() if v[0] is heap}
    vis = set(); order = []
    while heap.min is not None:
        z = heap.extract_min(); b = z.data; loc.pop(b, None)
        if b in vis: continue
        order.append(b); vis.add(b)
        for e in groups.get(b, []):
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
if __name__ == '__main__':
    pre, g, first = load(sys.argv[1])
    ov = dict((int(a), int(b)) for a, b in (x.split('=') for x in sys.argv[2:]))
    o = sim(pre, g, ov)
    print(' '.join(map(str, o)))
    print('real ' + ' '.join(map(str, first)))
