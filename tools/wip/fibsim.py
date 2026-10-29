"""Replay gcc 6's fibonacci_heap (bb-reorder STC) from a -fdump-rtl-bbro-details dump.

python tools/wip/fibsim.py dump
Checks every 'Getting bb' against the simulated extract_min; prints the extraction order.
"""
import re, sys

GMIN = -(1 << 63)


class Node:
    __slots__ = ('key', 'data', 'parent', 'child', 'left', 'right', 'degree', 'mark')

    def __init__(self, key=0, data=None):
        self.key, self.data = key, data
        self.parent = self.child = None
        self.left = self.right = self
        self.degree = 0
        self.mark = 0

    def cmp(self, o):
        return -1 if self.key < o.key else (1 if self.key > o.key else 0)

    def insert_after(self, b):
        a = self
        if a is a.right:
            a.right = b; a.left = b; b.right = a; b.left = a
        else:
            b.right = a.right; a.right.left = b; a.right = b; b.left = a

    def insert_before(self, b):
        a = self
        if a is a.left:
            a.right = b; a.left = b; b.right = a; b.left = a
        else:
            b.left = a.left; a.left.right = b; a.left = b; b.right = a

    def remove(self):
        ret = None if self is self.left else self.left
        if self.parent is not None and self.parent.child is self:
            self.parent.child = ret
        self.right.left = self.left
        self.left.right = self.right
        self.parent = None
        self.left = self.right = self
        return ret

    def link(self, parent):
        if parent.child is None:
            parent.child = self
        else:
            parent.child.insert_before(self)
        self.parent = parent
        parent.degree += 1
        self.mark = 0


class Heap:
    def __init__(self):
        self.min = self.root = None
        self.n = 0

    def insert_root(self, node):
        if self.root is None:
            self.root = node; node.left = node.right = node
        else:
            self.root.insert_after(node)

    def remove_root(self, node):
        if node.left is node:
            self.root = None
        else:
            self.root = node.remove()

    def insert(self, key, data):
        node = Node(key, data)
        self.insert_root(node)
        if self.min is None or node.key < self.min.key:
            self.min = node
        self.n += 1
        return node

    def extract_min(self):
        z = self.min
        if z is None:
            return None
        x, orig = z.child, None
        while x is not None and x is not orig:
            if orig is None:
                orig = x
            y = x.right
            x.parent = None
            self.insert_root(x)
            x = y
        self.remove_root(z)
        self.n -= 1
        if self.n == 0:
            self.min = None
        else:
            self.min = z.right
            self.consolidate()
        return z

    def consolidate(self):
        a = [None] * 65
        while self.root is not None:
            w = self.root
            x = w
            self.remove_root(w)
            d = x.degree
            while a[d] is not None:
                y = a[d]
                if x.cmp(y) > 0:
                    x, y = y, x
                y.link(x)
                a[d] = None
                d += 1
            a[d] = x
        self.min = None
        for i in range(65):
            if a[i] is not None:
                self.insert_root(a[i])
                if self.min is None or a[i].cmp(self.min) < 0:
                    self.min = a[i]

    def cut(self, x, y):
        x.remove()
        y.degree -= 1
        self.insert_root(x)
        x.parent = None
        x.mark = 0

    def cascading_cut(self, y):
        while True:
            z = y.parent
            if z is None:
                return
            if y.mark == 0:
                y.mark = 1
                return
            self.cut(y, z)
            y = z

    def replace_key(self, node, key):
        if key > node.key:
            # real increase: delete and reinsert (same node object semantics)
            data = node.data
            self.delete_node(node)
            return self.insert(key, data)
        okey = node.key
        node.key = key
        y = node.parent
        if okey == key and okey != GMIN:
            return node
        if y is not None and node.cmp(y) <= 0:
            self.cut(node, y)
            self.cascading_cut(y)
        if node.cmp(self.min) <= 0:
            self.min = node
        return node

    def delete_node(self, node):
        self.replace_key(node, GMIN)
        assert node is self.min
        self.extract_min()


def parse(dump):
    t = open(dump).read()
    t = t[t.index('Reordering with the STC algorithm.'):]
    ev = []
    for l in t.split('\n'):
        m = re.match(r'STC - round (\d+)', l)
        if m: ev.append(('round', int(m.group(1)))); continue
        m = re.match(r'Getting bb (\d+)', l)
        if m: ev.append(('get', int(m.group(1)))); continue
        m = re.match(r'Basic block (\d+) was visited', l)
        if m: ev.append(('visit', int(m.group(1)))); continue
        m = re.match(r'\s*Possible start of (this|next) round: (\d+) \(key: (-?\d+)\)', l)
        if m: ev.append(('ins', m.group(1), int(m.group(2)), int(m.group(3)))); continue
        m = re.match(r'\s*Possible start point of next round: (\d+) \(key: (-?\d+)\)', l)
        if m: ev.append(('push', int(m.group(1)), int(m.group(2)))); continue
        m = re.match(r'Changing key for bb (\d+) from (-?\d+) to (-?\d+)', l)
        if m: ev.append(('chg', int(m.group(1)), int(m.group(3)))); continue
        if l.startswith('Trace 1 ') or l.startswith('Final order'):
            break
    return ev


def run(ev, entry=2, verbose=False, strict=True):
    """Replay; with strict=False the simulated extraction is followed (events after a
    divergence are only approximately meaningful)."""
    heap = Heap()
    loc = {entry: (heap, heap.insert(0, entry))}
    new = None
    order = []
    for e in ev:
        if e[0] == 'round':
            if new is not None:
                heap = new
            new = Heap()
        elif e[0] == 'get':
            z = heap.extract_min()
            got = z.data
            loc.pop(got, None)
            order.append(got)
            if got != e[1]:
                if strict:
                    return order, 'diverged at get %d (sim %d)' % (e[1], got)
        elif e[0] == 'visit':
            if e[1] in loc:
                h, n = loc.pop(e[1])
                h.delete_node(n)
        elif e[0] == 'ins':
            h = heap if e[1] == 'this' else new
            loc[e[2]] = (h, h.insert(e[3], e[2]))
        elif e[0] == 'push':
            loc[e[1]] = (new, new.insert(e[2], e[1]))
        elif e[0] == 'chg':
            h, n = loc[e[1]]
            loc[e[1]] = (h, h.replace_key(n, e[2]))
    return order, 'ok'


if __name__ == '__main__':
    ev = parse(sys.argv[1])
    order, st = run(ev)
    print(st)
    print(' '.join(map(str, order)))
