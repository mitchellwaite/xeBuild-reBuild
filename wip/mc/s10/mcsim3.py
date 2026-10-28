"""Event-driven replay with key overrides that also apply to 'Changing key' events.
python mcsim2.py <mc bbro> k=v ...   (v = frequency; priority keys are derived: -(1000000+100*f+f))"""
import sys
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\wip')
import fibsim, fibwhatif
WANT = [129,107,109,110,113,108,119,120,121,128,116,132,49,112,115,103,55,126,125,61,33,29,67,127,117,130,35,42,53,77,79,73,81,86,137,95,138,96,91,93]
pos = {b: i for i, b in enumerate(WANT)}

def sim(R, freq):
    heap = fibsim.Heap(); new = None
    loc = {2: (heap, heap.insert(0, 2))}
    order = []
    def key(b, k):
        if b not in freq: return k
        f = freq[b]
        if f < 0: return 10000
        return -(1000000 + 100 * f + f) if k <= -100 else -f
    def apply(e):
        nonlocal heap, new
        if e[0] == 'visit':
            if e[1] in loc:
                h, n = loc.pop(e[1]); h.delete_node(n)
        elif e[0] == 'ins':
            h = heap if e[1] == 'this' else new
            if e[2] in loc: return
            loc[e[2]] = (h, h.insert(key(e[2], e[3]), e[2]))
        elif e[0] == 'push':
            loc[e[1]] = (new, new.insert(key(e[1], e[2]), e[1]))
        elif e[0] == 'chg':
            if e[1] in loc:
                h, n = loc[e[1]]; loc[e[1]] = (h, h.replace_key(n, key(e[1], e[2])))
    for ri, r in enumerate(R, 1):
        if new is not None: heap = new
        new = fibsim.Heap()
        for e in r['pre']: apply(e)
        while heap.min is not None:
            z = heap.extract_min(); b = z.data; loc.pop(b, None)
            order.append(b)
            for e in r['g'].get(b, []): apply(e)
    return order

def score(o, npre):
    o = [b for b in o[npre:] if b in pos]
    pre = 0
    for a, b in zip(o, WANT):
        if a != b: break
        pre += 1
    inv = sum(1 for i in range(len(o)) for j in range(i + 1, len(o)) if pos[o[i]] > pos[o[j]])
    return pre, inv, o

if __name__ == '__main__':
    ev = fibsim.parse(sys.argv[1]); R = fibwhatif.groups(ev)
    npre = sum(len(r['order']) for r in R[:3])
    f = {int(a.split('=')[0]): int(a.split('=')[1]) for a in sys.argv[2:]}
    try:
        o = sim(R, f)
    except Exception as e:
        print('ERR', e); sys.exit()
    pre, inv, oo = score(o, npre)
    print('pre=%d inv=%d' % (pre, inv)); print(' '.join(map(str, oo)))
