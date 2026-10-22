"""Search bb-reorder's last STC round for keys that give a wanted trace order.

python wip/fibsolve.py <mode_update bbro dump> [max K]   (env: FIBD FIBALL FIBFIX)

Replays rounds before the last exactly (wip/fibsim.py) and the last one
event-driven (as wip/fibwhatif.py). Every key in (-100, 0] that lands in the
last round's heap is a symbol: the heap only compares keys, so the search
branches on each undetermined comparison (<, =, >; the dump's integers first)
over a weak order of the symbols, and prunes on the first extraction that
breaks WANT. FLEX are traces that connect_traces attaches elsewhere, so their
extraction time doesn't show in the layout. Prints the first solution as the
weak order (classes low key first) with the dump's keys.
"""
import os, sys, itertools
sys.path.insert(0, 'wip')
import fibsim, fibwhatif

# original layout's last-round traces, in order (mode_update, profile build numbering)
WANT = [43, 128, 81, 87, 82, 130, 73, 69, 77, 102, 112, 46, 90, 122, 118, 94, 48,
        117, 20, 125, 50, 30, 38, 54, 58, 64, 62]
FLEX = {44, 105, 13}


class Need(Exception):
    pass


class Sym:
    __slots__ = ('i', 'dump')

    def __init__(self, i, dump):
        self.i, self.dump = i, dump


class Order:
    """Weak order over symbols, built from decisions: eq (union-find), lt (class graph)."""

    def __init__(self, n, dec):
        self.p = list(range(n))
        self.lt = [set() for _ in range(n)]
        for a, b, r in dec:
            self.add(a, b, r)

    def f(self, a):
        while self.p[a] != a:
            self.p[a] = self.p[self.p[a]]
            a = self.p[a]
        return a

    def add(self, a, b, r):
        a, b = self.f(a), self.f(b)
        if a == b:
            return
        if r == 0:
            self.p[b] = a
            self.lt[a] |= self.lt[b]
            for s in self.lt:
                if b in s:
                    s.discard(b); s.add(a)
        elif r < 0:
            self.lt[a].add(b)
        else:
            self.lt[b].add(a)

    def less(self, a, b):
        a, b = self.f(a), self.f(b)
        seen, st = {a}, [a]
        while st:
            x = st.pop()
            for y in self.lt[x]:
                y = self.f(y)
                if y == b:
                    return True
                if y not in seen:
                    seen.add(y); st.append(y)
        return False

    def rel(self, a, b):
        if self.f(a) == self.f(b):
            return 0
        if self.less(a, b):
            return -1
        if self.less(b, a):
            return 1
        return None


class Ctx:
    def __init__(self, nsym, dec):
        self.ord = Order(nsym, dec)

    def cmp(self, x, y):
        if isinstance(x, Sym) and isinstance(y, Sym):
            r = self.ord.rel(x.i, y.i)
            if r is None:
                raise Need(x, y)
            return r
        kx = -50 if isinstance(x, Sym) else x
        ky = -50 if isinstance(y, Sym) else y
        return -1 if kx < ky else (1 if kx > ky else 0)


CTX = None
# FIBD=n: every key stays an integer within n of the dump's (and <= 0)
FIBD = int(os.environ.get('FIBD', 0)) or None
# FIBFIX=bb,bb: those keep the dump's key
FIBFIX = {int(b) for b in os.environ.get('FIBFIX', '').split(',') if b}


def feasible(syms, dec):
    """Difference constraints (Bellman-Ford) -> {sym index: key} or None."""
    n = len(syms)
    S = n
    E = []
    for b, s in syms.items():
        dd = 0 if b in FIBFIX else FIBD
        E.append((S, s.i, min(0, s.dump + dd)))       # x - S <= hi
        E.append((s.i, S, -(s.dump - dd)))            # S - x <= -lo
    for a, b, r in dec:
        if r < 0:
            E.append((b, a, -1))                      # x_a - x_b <= -1
        elif r > 0:
            E.append((a, b, -1))
        else:
            E.append((b, a, 0)); E.append((a, b, 0))
    d = [0] * (n + 1)
    for _ in range(n + 1):
        ch = False
        for u, v, w in E:
            if d[u] + w < d[v]:
                d[v] = d[u] + w; ch = True
        if not ch:
            return {i: d[i] - d[S] for i in range(n)}
    return None


class SNode(fibsim.Node):
    __slots__ = ()

    def cmp(self, o):
        return CTX.cmp(self.key, o.key)


class SHeap(fibsim.Heap):
    def insert(self, key, data):
        node = SNode(key, data)
        self.insert_root(node)
        if self.min is None or CTX.cmp(node.key, self.min.key) < 0:
            self.min = node
        self.n += 1
        return node

    def replace_key(self, node, key):
        if CTX.cmp(key, node.key) > 0:
            data = node.data
            self.delete_node(node)
            return self.insert(key, data)
        okey = node.key
        node.key = key
        y = node.parent
        if okey is not fibsim.GMIN and CTX.cmp(okey, key) == 0:
            return node
        if y is not None and node.cmp(y) <= 0:
            self.cut(node, y)
            self.cascading_cut(y)
        if node.cmp(self.min) <= 0:
            self.min = node
        return node


def closest(syms, dec, k):
    """Greedy: move equality classes toward the dump's keys while every decision holds."""
    dump = {s.i: s.dump for s in syms.values()}
    o = Order(len(syms), dec)
    cls = {}
    for i in dump:
        cls.setdefault(o.f(i), []).append(i)

    def ok(k):
        for a, b, r in dec:
            if (k[a] > k[b]) - (k[a] < k[b]) != r:
                return False
        return all(-100 < v <= 0 for v in k.values())
    moved = True
    while moved:
        moved = False
        for c in cls.values():
            dev = sum(dump[i] - k[i] for i in c)
            if not dev:
                continue
            step = 1 if dev > 0 else -1
            t = dict(k)
            for i in c:
                t[i] += step
            if ok(t) and sum(abs(t[i] - dump[i]) for i in c) < sum(abs(k[i] - dump[i]) for i in c):
                k = t; moved = True
    return k


def run(R, syms, dec):
    """-> ('ok', order) | ('fail', order) ; raises Need."""
    global CTX
    CTX = Ctx(len(syms), dec)
    last = len(R)
    heap = SHeap(); new = None
    loc = {2: (heap, heap.insert(0, 2))}
    order, wi, flex = [], 0, set()

    def key(b, k, ri, nxt):
        # symbolic only for keys that land in the last round's heap
        sym = ri == last or (ri == last - 1 and nxt)
        return syms[b] if sym and b in syms and -100 < k <= 0 else k

    def apply(e, ri):
        if e[0] == 'visit':
            if e[1] in loc:
                h, n = loc.pop(e[1]); h.delete_node(n)
        elif e[0] == 'ins':
            h = heap if e[1] == 'this' else new
            if e[2] in loc:
                return
            loc[e[2]] = (h, h.insert(key(e[2], e[3], ri, e[1] == 'next'), e[2]))
        elif e[0] == 'push':
            loc[e[1]] = (new, new.insert(key(e[1], e[2], ri, True), e[1]))
        elif e[0] == 'chg':
            if e[1] in loc:
                h, n = loc[e[1]]; loc[e[1]] = (h, h.replace_key(n, key(e[1], e[2], ri, h is new)))

    for ri, r in enumerate(R, 1):
        if new is not None:
            heap = new
        new = SHeap()
        for e in r['pre']:
            apply(e, ri)
        if ri < last:
            for b in r['order']:
                z = heap.extract_min(); loc.pop(z.data, None)
                assert z.data == b, (ri, b, z.data)
                for e in r['g'][b]:
                    apply(e, ri)
        else:
            while heap.min is not None:
                z = heap.extract_min(); b = z.data; loc.pop(b, None)
                order.append(b)
                if b in FLEX and b not in flex:
                    flex.add(b)
                elif wi < len(WANT) and b == WANT[wi]:
                    wi += 1
                else:
                    return 'fail', order
                for e in r['g'].get(b, []):
                    apply(e, ri)
    return ('ok' if wi == len(WANT) else 'fail'), order


def main():
    ev = fibsim.parse(sys.argv[1])
    R = fibwhatif.groups(ev)
    last = len(R)
    # symbols: every node whose small key enters the last round's heap
    names = {}
    for ri, r in enumerate(R, 1):
        evs = r['pre'] + [x for b in r['order'] for x in r['g'].get(b, [])]
        for e in evs:
            if e[0] == 'ins' and -100 < e[3] <= 0 and (ri == last or (ri == last - 1 and e[1] == 'next')):
                names.setdefault(e[2], e[3])
            if e[0] == 'push' and ri == last - 1 and -100 < e[2] <= 0:
                names.setdefault(e[1], e[2])
    syms = {b: Sym(i, k) for i, (b, k) in enumerate(names.items())}
    print('symbols', len(syms), names)
    # limited discrepancy search: a decision unlike the dump's integers costs 1
    for K in range(int(sys.argv[2]) if len(sys.argv) > 2 else 12):
        st = [([], 0)]
        tried = best = 0
        fewest = 99
        while st:
            dec, disc = st.pop()
            tried += 1
            try:
                res, order = run(R, syms, dec)
            except Need as n:
                x, y = n.args
                d = (x.dump > y.dump) - (x.dump < y.dump)
                for r in sorted((-1, 0, 1), key=lambda r: r == d):
                    c = disc + (r != d)
                    nd = dec + [(x.i, y.i, r)]
                    if c <= K and (FIBD is None or feasible(syms, nd)):
                        st.append((nd, c))
                continue
            if res == 'ok':
                if not os.environ.get('FIBALL'):
                    print('K', K)
                    show(syms, dec, order)
                    return
                # FIBALL=1: keep searching this K, print each new fewest-changes solution
                k = closest(syms, dec, feasible(syms, dec))
                ch = {b: k[s.i] for b, s in syms.items() if k[s.i] != s.dump}
                if len(ch) < fewest:
                    fewest = len(ch)
                    print('K', K, len(ch), ch, flush=True)
                continue
            best = max(best, len(order))
        print('K', K, 'no solution; tried', tried, 'best prefix', best, flush=True)


def show(syms, dec, order):
    o = Order(len(syms), dec)
    inv = {s.i: (b, s.dump) for b, s in syms.items()}
    cls = {}
    for i in inv:
        cls.setdefault(o.f(i), []).append(inv[i])
    keys = list(cls)
    keys.sort(key=lambda c: sum(1 for d in keys if d != c and o.less(d, c)))
    print('order', order)
    for c in keys:
        print('  ', sorted(cls[c]))
    print('decisions', len(dec))
    if FIBD:
        k = closest(syms, dec, feasible(syms, dec))
        print('keys', {b: k[s.i] for b, s in syms.items() if k[s.i] != s.dump})
    for a, b, r in dec:
        (ba, ka), (bb, kb) = inv[a], inv[b]
        d = (ka > kb) - (ka < kb)
        if r != d or os.environ.get('ALLDEC'):
            print('  flipped: bb %d (%d) %s bb %d (%d)' % (ba, ka, '<=>'[r + 1], bb, kb))


if __name__ == '__main__':
    main()
