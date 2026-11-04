"""flxp.py <N> <seed>: arm-size sampling around the first match (extra test x before flashfs's pos >= size).
States: `nest|comma=3,...,x=1`.  Biased to fewer tests.  Logs to xp.txt; prints best per test count."""
import os, random, sys
from concurrent.futures import ThreadPoolExecutor
import fllib as L, flx7 as T, flxk as K

XA = '\t\t\tif (pos >= size)\n'
START = dict((kv.split('=')[0], int(kv.split('=')[1])) for kv in os.environ.get('START', 'comma=3,i=1,len=1,nul=1,off3=2,off4=2,off5=3,x=1').split(','))


def build(keep, fl='nest'):
    kk = {k: v for k, v in keep.items() if k != 'x'}
    s = K.build(fl, kk, False)
    if keep.get('x'):
        s = L.sub(s, XA, '\t\t\tif (off < -1) {\n' + ''.join('\t\t\t\tbuf[%d] = 1;\n' % j for j in range(keep['x'])) + '\t\t\t}\n' + XA)
    return s


def lab(keep):
    return ','.join('%s=%d' % kv for kv in sorted(keep.items()))


if __name__ == '__main__':
    N, seed = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    names = list(START)
    print('start', L.score(L.compile(build(START), None, 'p0'))[:2])
    V = {}
    while len(V) < N:
        keep = dict(START)
        # drop 1-3 tests, re-roll some arms
        for n in rng.sample(names, rng.choice([1, 1, 1, 2, 2])):
            keep.pop(n)
        for n in list(keep):
            if rng.random() < 0.4:
                keep[n] = rng.randint(1, int(os.environ.get('KMAX', '6')))
        V[lab(keep)] = build(keep)

    def one(kv):
        i, (n, s) = kv
        o = L.compile(s, None, 'p%d_%d' % (seed, i))
        if o is None:
            return 10**7, '', n
        sc = L.score(o)
        v = T.vec(o)
        os.remove(o)
        return sc[0], v, n
    with ThreadPoolExecutor(4) as ex:
        rs = sorted(ex.map(one, enumerate(V.items())), key=lambda r: r[0])
    with open(L.BD + '/xp.txt', 'a', newline='\n') as f:
        for r in rs:
            f.write('%s\t%s\t%s\n' % r)
    for r in rs[:15]:
        print(r[0], r[1], r[2], 'tests', r[2].count('='))
    print('MATCH', sorted(((r[2].count('='), r[2]) for r in rs if r[0] == 0))[:10])
