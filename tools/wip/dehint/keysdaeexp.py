"""keysdaeexp.py: the hint-free daeEncrypt plus one expect on n != 2, over the param."""
import keyslib as K, keysdaegrid as G
from keysfn import replace_fn
from multiprocessing.pool import ThreadPool

t = G.text('W1', 'H0', 'B1', 'L0', False, 'E0')
assert 'if (n != 2)' in t
b = K.base()
jobs = []
for pol in (0, 1):
    for p in [None, 50, 52, 54, 55, 56, 58, 60, 62, 64, 66, 70, 75, 80, 85, 90, 95, 99]:
        jobs.append((pol, p))


def one(a):
    i, (pol, p) = a
    s = replace_fn(b, 'daeEncrypt', t.replace('if (n != 2)', 'if (__builtin_expect(n != 2, %d))' % pol))
    fl = ['-O3'] + (['--param', 'builtin-expect-probability=%d' % p] if p else [])
    o = K.compile(s, fl, 'ex%d' % (i % 4))
    return pol, p, K.same(o), K.fndiff(o)


slots = [[] for _ in range(4)]
for i, j in enumerate(jobs):
    slots[i % 4].append((i, j))
with ThreadPool(4) as pool:
    for r in pool.map(lambda sl: [one(x) for x in sl], slots):
        for x in r:
            print(x)
