import sys, os
R = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, os.path.join(R, r'tools\wip\mc\s18')); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(R, r'tools\wip'))
import hsim, fibsim, mcsim2
Rr, keys = hsim.load(os.path.join(R, 'build', 'v', 'mc39', 'slot_' + sys.argv[1]))
f, P = hsim.measured(keys)
WATCH = set(int(x) for x in sys.argv[2].split(','))
def show(h):
    out = []
    def rec(n, d):
        x = n; first = True
        while first or x is not n:
            first = False
            out.append('  ' * d + '%s(%d,deg%d)' % (x.data, x.key, x.degree))
            if x.child: rec(x.child, d + 1)
            x = x.right
    if h.root: rec(h.root, 0)
    return '\n'.join(out)
heap = fibsim.Heap(); new = None; loc = {1002: (heap, heap.insert(0, 1002))}
def key(b, k):
    if b not in f: return k
    if k <= -1000000: return -(1000000 + 100 * P.get(b, 0) + f[b]) if P.get(b, 0) > 0 else -f[b]
    if k >= 10000: return k
    return -f[b]
def apply(e, ri, popped):
    if e[0] == 'visit':
        if e[1] in loc: h, nd = loc.pop(e[1]); h.delete_node(nd)
    elif e[0] == 'ins':
        h = heap if e[1] == 'this' else new
        if e[2] in loc: return
        loc[e[2]] = (h, h.insert(key(e[2], e[3]), e[2]))
        if ri == 4 and e[2] in WATCH: print('   ins', e[2], 'key', key(e[2], e[3]), 'during', popped)
    elif e[0] == 'push':
        if e[1] in loc: return
        loc[e[1]] = (new, new.insert(key(e[1], e[2]), e[1]))
    elif e[0] == 'chg':
        if e[1] in loc:
            h, nd = loc[e[1]]; k = key(e[1], e[2])
            if k != nd.key: loc[e[1]] = (h, h.replace_key(nd, k))
for ri, r in enumerate(Rr, 1):
    if new is not None: heap = new
    new = fibsim.Heap()
    for e in r['pre']: apply(e, ri, 'pre')
    if ri == 4: print('round 4 start heap:'); print(show(heap))
    while heap.min is not None:
        z = heap.extract_min(); b = z.data; loc.pop(b, None)
        if ri == 4: print('POP', b, z.key)
        for e in r['g'].get(b, []): apply(e, ri, b)
        if ri == 4 and b == int(sys.argv[3]): print(show(heap))
