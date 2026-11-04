"""flxo.py <N> [labels...]: natural axes (flx3) on arm-size states: every single edit and N random pairs each."""
import itertools, random, sys
from collections import Counter
import fllib as L, flx3 as A, flxk as K


def parse(lb):
    a = lb.split('|')
    keep = dict((kv.split('=')[0], int(kv.split('=')[1])) for kv in a[1].split(',') if kv)
    return a[0], keep, len(a) > 2


N = int(sys.argv[1])
labels = sys.argv[2:] or ['nest|comma=1,i=1,len=3,off3=3,off4=1,off5=4', 'nest|len=3,off3=5,off4=1,off5=4',
                          'nest|comma=3,i=1,len=1,nul=1,off3=2,off4=2,off5=3']
rng = random.Random(9)
items = [(a, v) for a in A.AXES for v in A.AXES[a]]
pairs = [c for c in itertools.combinations(items, 2) if c[0][0] != c[1][0]]
V = {}
for si, lb in enumerate(labels):
    base = K.build(*parse(lb))
    for c in [(x,) for x in items] + rng.sample(pairs, N):
        ch = dict(c)
        if 'cn' in ch and 'comma=' in lb:
            continue
        try:
            V['%d:%s' % (si, ','.join('%s=%s' % kv for kv in sorted(ch.items())))] = A.apply(base, ch)
        except ValueError:
            pass
print(len(V))
rs = L.sweep(V, prefix='o', show=20)
print(sorted(Counter((n[0], r[0]) for n, r in rs).items(), key=lambda x: x[0][1])[:12])
