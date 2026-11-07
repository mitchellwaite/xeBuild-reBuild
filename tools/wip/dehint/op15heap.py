"""Attempt 15: print the round-4 fibheap structure of TAG's bbro replay (p1/sim3.py) around
the extractions of given blocks, to see what decides a tie.

python tools/wip/dehint/op15heap.py TAG [-k K1,K2] [-at N1,N2] [-w b1,b2]
  -at: print the heap before the Nth r4 extraction (default: before each of -w's blocks)
  -w:  blocks to watch (default 169,179,220)
  -k:  only show nodes whose key is in this list (default: the watched blocks' keys)"""
import os, sys
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(H, '..', 'aio', 'p1'))
sys.path.insert(0, os.path.join(H, '..'))
import fibsim
import sim3
R = os.path.join(H, '..', '..', '..', 'build', 'v', 'aio_p1')


def tree(n, keys, depth=0, out=None):
    out = [] if out is None else out
    out.append('%s%d[%d]d%d%s' % ('  ' * depth, n.data, n.key, n.degree, '*' if n.mark else ''))
    c = n.child
    if c is not None:
        x = c
        while True:
            tree(x, keys, depth + 1, out)
            x = x.right
            if x is c:
                break
    return out


def roots(h):
    r = []
    if h.root is None:
        return r
    x = h.root
    while True:
        r.append(x)
        x = x.right
        if x is h.root:
            break
    return r


def show(h, keys):
    for r in roots(h):
        t = tree(r, keys)
        if any(int(l.split('[')[1].split(']')[0]) in keys for l in t):
            print('  root', ' | '.join(l.strip() for l in t if int(l.split('[')[1].split(']')[0]) in keys or l is t[0]))
        else:
            print('  root %d[%d]d%d (%d nodes)' % (r.data, r.key, r.degree, len(t)))


def main():
    a = sys.argv[1:]
    tag = a[0]
    watch = [169, 179, 220]
    if '-w' in a:
        watch = [int(x) for x in a[a.index('-w') + 1].split(',')]
    at = None
    if '-at' in a:
        at = [int(x) for x in a[a.index('-at') + 1].split(',')]
    pre, g3, f3, g4, f4 = sim3.load(os.path.join(R, tag, 'aio.bbro'))
    # replay like sim3.sim but hook round 4
    orig_extract = fibsim.Heap.extract_min
    state = {'r4': None, 'n': 0, 'keys': None}

    def ext(self):
        if state['r4'] is self and self.min is not None and self.min.key != fibsim.GMIN:
            n = state['n']
            b = self.min.data
            if (at and n in at) or (not at and b in watch):
                keys = state['keys']
                print('before r4 extraction %d (min %d key %d), heap n=%d' % (n, b, self.min.key, self.n))
                show(self, keys)
            state['n'] += 1
        return orig_extract(self)
    fibsim.Heap.extract_min = ext
    # find the round-4 heap: sim3 sets heap=new after round 3; detect by the first extraction
    # of f4[0]
    kk = {}
    for gs in (g3, g4):
        for evs in gs.values():
            for e in evs:
                if e[0] == 'ins':
                    kk[e[2]] = e[3]
                elif e[0] == 'push':
                    kk[e[1]] = e[2]
    for e in pre:
        if e[0] == 'ins':
            kk[e[2]] = e[3]
        elif e[0] == 'push':
            kk[e[1]] = e[2]
    keys = set(kk.get(b) for b in watch)
    if '-k' in a:
        keys = set(int(x) for x in a[a.index('-k') + 1].split(','))
    state['keys'] = keys
    orig_sim_insert = fibsim.Heap.insert
    heaps = []

    def ins(self, key, data):
        if self not in heaps:
            heaps.append(self)
        return orig_sim_insert(self, key, data)
    fibsim.Heap.insert = ins
    # run once to find which heap object holds f4[0]
    first4 = f4[0]
    found = {}

    def ins2(self, key, data):
        if data == first4 and 'h' not in found and len(heaps) >= 3:
            found['h'] = self
        return ins(self, key, data)
    fibsim.Heap.insert = ins2
    # sim3 creates heaps: pre (rounds 1-2 + round-3 new), round 3 'new' = round-4 heap.
    # Simplest: mark r4 heap lazily as the heap from which f4[0] is first extracted.
    orig2 = ext

    def ext2(self):
        if self.min is not None and self.min.data == first4 and self.min.key != fibsim.GMIN and state['r4'] is not self:
            # only the round-4 heap pops f4[0] as a trace start
            state['r4'] = self
            state['n'] = 0
        return orig2(self)
    fibsim.Heap.extract_min = ext2
    o3, o4 = sim3.sim(pre, g3, g4)
    print('r3 same', o3 == f3, 'r4 same', o4 == f4)
    print('r4 order', ' '.join(map(str, o4)))


main()
