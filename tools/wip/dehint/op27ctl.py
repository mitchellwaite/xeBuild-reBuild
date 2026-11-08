#!/usr/bin/env python3
"""Attempt 27: positive controls for the replay maps.  A replay that can't reproduce the
reference even with the known answer injected says nothing when it reports 0 hits.

python tools/wip/dehint/op27ctl.py REFTAG TAG [-map FILE|auto] [-ov b:k,..] SPEC ..
  SPEC  HEAD@POS:KEY        a virtual entry inserted ('ins this') at position POS of round-4
                           head HEAD's event group, key KEY, left to be extracted (a dummy)
        HEAD@POS:KEY/B@Q    .. and deleted (visited) at position Q of head B's group
        r3:HEAD@POS:KEY     pushed into the round-4 heap from round-3 head HEAD's group
  -map auto: op27map.py's map and drop list (default); FILE: a:b,.. (no drops)
  -ov: key overrides of real entries (sim3's ov)
Prints the check, then the first difference of the r3 / r4 head orders."""
import os, sys
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(H, '..', 'aio', 'p1'))
sys.path.insert(0, H)
import sim3
R = os.path.join(H, '..', '..', '..', 'build', 'v', 'aio_p1')


def getmap(ref, tag, spec='auto'):
    if spec == 'auto':
        import op27map
        m, drop, coll = op27map.build(ref, tag)
        assert not coll, coll
        return m, set(drop)
    txt = open(spec).read().strip() if os.path.exists(spec) else spec
    return dict(tuple(int(y) for y in x.split(':')) for x in txt.split(',') if x), set()


class Replay:
    def __init__(self, ref, tag, mapspec='auto'):
        _, _, self.f3r, _, self.f4r = sim3.load(os.path.join(R, ref, 'aio.bbro'))
        self.pre, self.g3, self.f3, self.g4, self.f4 = sim3.load(os.path.join(R, tag, 'aio.bbro'))
        self.map, self.drop = getmap(ref, tag, mapspec)

    def orders(self, g3=None, g4=None, ov={}, ignore=()):
        o3, o4 = sim3.sim(self.pre, self.g3 if g3 is None else g3, self.g4 if g4 is None else g4, ov)
        skip = self.drop | set(ignore)
        o3 = [self.map.get(x, x) for x in o3 if x not in skip and x < 9000]
        o4 = [self.map.get(x, x) for x in o4 if x not in skip and x < 9000]
        return o3, o4

    def check(self, g3=None, g4=None, ov={}, ignore=(), refignore=(), why=False):
        o3, o4 = self.orders(g3, g4, ov, ignore)
        s3, s4 = set(o3), set(o4)
        r3 = [x for x in self.f3r if x in s3 and x not in refignore]
        r4 = [x for x in self.f4r if x in s4 and x not in refignore]
        o3 = [x for x in o3 if x not in refignore]
        o4 = [x for x in o4 if x not in refignore]
        ok = r3 == o3 and r4 == o4
        if why and not ok:
            for nm, r, o in (('r3', r3, o3), ('r4', r4, o4)):
                if r != o:
                    i = next((i for i in range(min(len(r), len(o))) if r[i] != o[i]), min(len(r), len(o)))
                    return ok, '%s differs at %d: ref %s / tag %s (lens %d %d)' % (nm, i, r[i:i + 6], o[i:i + 6], len(r), len(o))
        return ok, ''

    def inject(self, specs):
        g3 = {h: list(e) for h, e in self.g3.items()}
        g4 = {h: list(e) for h, e in self.g4.items()}
        v = 9001
        # positions refer to the original groups: apply from the back
        ops = []
        for s in specs:
            dl = None
            if '/' in s:
                s, dl = s.split('/')
            r3 = s.startswith('r3:')
            if r3:
                s = s[3:]
            hp, k = s.split(':')
            h, p = (int(x) for x in hp.split('@'))
            ops.append((3 if r3 else 4, h, p, ('ins', 'next' if r3 else 'this', v, int(k))))
            if dl:
                b, q = (int(x) for x in dl.split('@'))
                ops.append((4, b, q, ('visit', v)))
            v += 1
        for rd, h, p, e in sorted(ops, key=lambda o: (o[0], o[1], -o[2])):
            g = g3 if rd == 3 else g4
            g.setdefault(h, []).insert(p, e)
        return g3, g4


if __name__ == '__main__':
    a = sys.argv[1:]
    opt = lambda k, d: a[a.index(k) + 1] if k in a else d
    rp = Replay(a[0], a[1], opt('-map', 'auto'))
    ov = dict(tuple(int(y) for y in x.split(':')) for x in opt('-ov', '').split(',') if x)
    specs = [x for i, x in enumerate(a[2:]) if not x.startswith('-') and a[1 + i] not in ('-map', '-ov')]
    print('as is', *rp.check(ov=ov, why=True))
    if specs:
        print('with', specs, *rp.check(*rp.inject(specs), ov=ov, why=True))
