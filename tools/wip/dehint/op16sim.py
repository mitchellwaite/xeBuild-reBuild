"""Attempt 16: replay TAG's bbro heap (p1/sim3) with explicit key overrides and compare
the extraction order with REFTAG's real one.

python tools/wip/dehint/op16sim.py REFTAG TAG [-map a:b,..] [-k b=key,..] [-keys b1,b2]
  -keys: print the keys TAG's dump gives these blocks
  prints the first difference of r3/r4 (after the id map)"""
import os, sys
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(H, '..', 'aio', 'p1'))
sys.path.insert(0, os.path.join(H, '..'))
import sim3
R = os.path.join(H, '..', '..', '..', 'build', 'v', 'aio_p1')


def keys_of(pre, g3, g4):
    ks = {}
    for e in list(pre) + [e for gs in (g3, g4) for evs in gs.values() for e in evs]:
        if e[0] == 'ins':
            ks.setdefault(e[2], []).append(e[3])
        elif e[0] == 'push':
            ks.setdefault(e[1], []).append(e[2])
        elif e[0] == 'chg':
            ks.setdefault(e[1], []).append(('chg', e[2]))
    return ks


def load(tag):
    return sim3.load(os.path.join(R, tag, 'aio.bbro'))


def compare(refd, tagd, ov, MAP):
    _, _, f3r, _, f4r = refd
    pre, g3, f3, g4, f4 = tagd
    o3, o4 = sim3.sim(pre, g3, g4, ov)
    o3 = [MAP.get(x, x) for x in o3]
    o4 = [MAP.get(x, x) for x in o4]
    s3, s4 = set(o3), set(o4)
    r3 = [x for x in f3r if x in s3]
    r4 = [x for x in f4r if x in s4]
    return r3 == o3 and r4 == o4, (r3, o3, r4, o4)


def first_diff(a, b):
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return i, a[max(0, i - 2):i + 6], b[max(0, i - 2):i + 6]
    return None


if __name__ == '__main__':
    a = sys.argv[1:]
    refd, tagd = load(a[0]), load(a[1])
    MAP = dict(tuple(int(y) for y in x.split(':')) for x in a[a.index('-map') + 1].split(',')) if '-map' in a else {}
    ov = {}
    if '-k' in a:
        for x in a[a.index('-k') + 1].split(','):
            b, k = x.split('=')
            ov[int(b)] = int(k)
    if '-keys' in a:
        ks = keys_of(tagd[0], tagd[1], tagd[3])
        for b in a[a.index('-keys') + 1].split(','):
            print(b, ks.get(int(b)))
    if '-scan' in a:
        i = a.index('-scan')
        lo, hi = int(a[i + 1]), int(a[i + 2])
        ks = keys_of(tagd[0], tagd[1], tagd[3])
        n = 0
        for b in sorted(ks):
            k0 = [k for k in ks[b] if not isinstance(k, tuple)]
            if not k0 or b in ov:
                continue
            hs = [k for k in range(lo, hi + 1) if k != k0[0] and compare(refd, tagd, {**ov, b: k}, MAP)[0]]
            if hs:
                n += 1
                print('block', b, 'key', k0[0], '->', hs if len(hs) < 12 else '%d..%d (%d)' % (hs[0], hs[-1], len(hs)))
        print(n, 'single hits')
        sys.exit()
    ok, (r3, o3, r4, o4) = compare(refd, tagd, ov, MAP)
    print('match', ok, 'real r3/r4 same as ref:', [MAP.get(x, x) for x in tagd[2]] == refd[2], [MAP.get(x, x) for x in tagd[4]] == refd[4])
    print('r3', first_diff(r3, o3))
    print('r4', first_diff(r4, o4))
