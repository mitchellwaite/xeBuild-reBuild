"""flx7.py <N> <seed> <state label> [AXP env]: sample axes at one dead set and report tie vectors.
A tie vector is which of the ref's tie-sensitive lines appear: t1 (bl cmp), t2 (rawpatch lea),
t3 (flashfs mov/xor order), plus the score.  Shows whether any natural edit flips a tie alone."""
import os, random, sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
import fllib as L, flx as X, flx3 as A, flx4 as F

T1 = ('cmp    edx,ebx', 'mov    DWORD PTR [esp+0x34],0x1', 'jle')
T2 = 'lea    ebp,[ebx+ebp*1+0x1]'
T3 = ('mov    ebx,0xffffffff', 'xor    edi,edi')


def vec(o):
    d = L.dis(o)['_parseIni']
    t1 = any(d[i] == T1[0] and d[i + 1] == T1[1] and d[i + 2].startswith(T1[2]) for i in range(len(d) - 2))
    t2 = T2 in d
    t3 = any(d[i] == T3[0] and d[i + 1] == T3[1] for i in range(len(d) - 1))
    return ('1' if t1 else '-') + ('2' if t2 else '-') + ('3' if t3 else '-')


if __name__ == '__main__':
    N, seed = int(sys.argv[1]), int(sys.argv[2])
    fl, dead, ch = F.parse(sys.argv[3])
    AXP = float(os.environ.get('AXP', '0.2'))
    rng = random.Random(seed)
    V = {}
    tries = 0
    while len(V) < N and tries < N * 10:
        tries += 1
        c = dict(ch)
        c.update(A.rnd_choice(rng, AXP))
        if c.get('cn') and 'comma' not in dead:
            continue
        lb = A.label(dead, fl, c)
        if lb in V:
            continue
        try:
            V[lb] = A.apply(X.gen(dead, fl), c)
        except ValueError:
            pass

    def one(kv):
        i, (n, s) = kv
        o = L.compile(s, None, 'v%d' % (i % 8) + '_%d' % (i))
        if o is None:
            return n, None, None
        sc = L.score(o)
        v = vec(o)
        os.remove(o)
        return n, sc[0], v
    with ThreadPoolExecutor(4) as ex:
        rs = list(ex.map(one, enumerate(V.items())))
    rs = [r for r in rs if r[1] is not None]
    rs.sort(key=lambda r: r[1])
    c = Counter((r[2], r[1]) for r in rs)
    for k in sorted(c, key=lambda k: k[1])[:20]:
        print(k, c[k])
    with open(L.BD + '/x7_%d.txt' % seed, 'w', newline='\n') as f:
        for r in rs:
            f.write('%s\t%s\t%s\n' % (r[1], r[2], r[0]))
    for r in rs[:12]:
        print(r[1], r[2], r[0])
