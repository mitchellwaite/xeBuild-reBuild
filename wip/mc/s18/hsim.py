"""hsim.py: replay a REAL bbro history of a slot (renumbered to sp numbers) with design keys.
Event keys of sp blocks are replaced: priority events (key <= -1e6) -> -(1e6 + 100*P + f), else -f.
Used for local what-if searches around a realized design (much better tie fidelity than fake7).
python hsim.py SLOTDIR [b=f/P ...]   prints the simulated order + inversions for the measured keys"""
import os, sys, json
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, ROOT + r'\wip'); sys.path.insert(0, ROOT + r'\wip\mc'); sys.path.insert(0, ROOT + r'\wip\mc\s18')
import fibsim, fibwhatif, mcsim2, analyze


def load(sd):
    bbro, sp = analyze.spmap(sd)
    ren = {}
    for b, s in sp.items():
        if isinstance(s, int): ren[b] = s
        elif s == 'k94': ren[b] = 94
    def rn(b):
        return ren.get(b, b + 1000)
    tmp = os.path.join(sd, 'bbro_mc.txt')
    open(tmp, 'w').write(bbro)
    ev = fibsim.parse(tmp)
    out = []
    for e in ev:
        if e[0] in ('get', 'visit'): out.append((e[0], rn(e[1])))
        elif e[0] == 'ins': out.append(('ins', e[1], rn(e[2]), e[3]))
        elif e[0] == 'push': out.append(('push', rn(e[1]), e[2]))
        elif e[0] == 'chg': out.append(('chg', rn(e[1]), e[2]))
        else: out.append(e)
    R = fibwhatif.groups(out)
    o, inv, keys, named = analyze.analyze(sd)
    return R, keys


RXEV = {}
for _it in os.environ.get('RXEV', '').split(','):
    if _it:
        _s, _t = map(int, _it.split(':')); RXEV.setdefault(_s, []).append(_t)


def sim(R, f, P, entry=1002):
    heap = fibsim.Heap(); new = None
    loc = {entry: (heap, heap.insert(0, entry))}
    order = []
    def key(b, k):
        if b not in f: return k
        if k <= -1000000: return -(1000000 + 100 * P.get(b, 0) + f[b]) if P.get(b, 0) > 0 else -f[b]
        if k >= 10000: return k
        return -f[b]
    def apply(e):
        if e[0] == 'visit':
            if e[1] in loc:
                h, n = loc.pop(e[1]); h.delete_node(n)
        elif e[0] == 'ins':
            h = heap if e[1] == 'this' else new
            if e[2] in loc: return
            loc[e[2]] = (h, h.insert(key(e[2], e[3]), e[2]))
        elif e[0] == 'push':
            if e[1] in loc: return
            loc[e[1]] = (new, new.insert(key(e[1], e[2]), e[1]))
        elif e[0] == 'chg':
            if e[1] in loc:
                h, n = loc[e[1]]; k = key(e[1], e[2])
                if k != n.key: loc[e[1]] = (h, h.replace_key(n, k))
    for ri, r in enumerate(R, 1):
        if new is not None: heap = new
        new = fibsim.Heap()
        for e in r['pre']: apply(e)
        while heap.min is not None:
            z = heap.extract_min(); b = z.data; loc.pop(b, None)
            order.append((ri, b))
            for e in r['g'].get(b, []): apply(e)
            if ri == 4 and b in RXEV:
                for t in RXEV[b]:
                    if t in loc and P.get(t, 0) > 0:
                        h, n = loc[t]; k = -(1000000 + 100 * P[t] + f[t])
                        if k != n.key: loc[t] = (h, h.replace_key(n, k))
    return [b for r, b in order if r == 4 and b in mcsim2.pos]


NEED = [129, 107, 109, 110, 113, 108, 119, 120, 121, 128, 116, 132, 49, 112, 115, 103, 55, 126, 125, 61, 33, 29, 67,
        127, 117, 130, 35, 42, 53, 77, 79]


def inv(o):
    p = mcsim2.pos
    s = set(o)
    return sum(1 for a in range(len(o)) for b in range(a + 1, len(o)) if p[o[a]] > p[o[b]]) + 5 * sum(1 for b in NEED if b not in s)


def measured(keys):
    f, P = {}, {}
    for b, (p, v) in keys.items():
        if isinstance(b, str):
            if b == 'k94': f[94], P[94] = v, p
            continue
        f[b] = v if v is not None and v >= 0 else 0
        P[b] = p or 0
    return f, P


if __name__ == '__main__':
    R, keys = load(sys.argv[1])
    f, P = measured(keys)
    for a in sys.argv[2:]:
        b, v = a.split('='); fv, pv = v.split('/'); f[int(b)] = int(fv); P[int(b)] = int(pv)
    o = sim(R, f, P)
    print('inv', inv(o)); print(' '.join(map(str, o)))
