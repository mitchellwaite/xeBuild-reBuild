"""flxe.py <var> <anchor text> [<anchor2 var>...]: all 256 dead subsets x flen asm/nest with fixed extra
dead test(s) inserted before the anchor line.  Default: `if (off < -1)` before [version]'s len = ...
Anchors are source substrings located at build time."""
import itertools, os, sys
import fllib as L, flx as X, flx3 as A, flx6 as D, flx7 as T
from concurrent.futures import ThreadPoolExecutor

DEFAULT = [('off', '\t\tlen = memFindChar(&buf[off], 0, sizeof(xb.kernelStr));\n')]


def put(s, ins):
    for v, a in ins:
        p = s.index(a)
        s = D.insert(s, p, v)
    return s


def run(ins, fls=('asm', 'nest'), show=40, tag='e'):
    V = {}
    for fl in fls:
        for r in range(len(X.ALLDEAD) + 1):
            for rm in itertools.combinations(X.ALLDEAD, r):
                V[fl + '|' + '+'.join(x for x in X.ALLDEAD if x not in rm)] = put(X.gen(rm, fl), ins)

    def one(kv):
        i, (n, s) = kv
        o = L.compile(s, None, tag + str(i))
        sc = L.score(o)
        v = T.vec(o)
        os.remove(o)
        return sc[0], v, n
    with ThreadPoolExecutor(4) as ex:
        rs = sorted(ex.map(one, enumerate(V.items())), key=lambda r: r[0])
    for r in rs[:show]:
        print(r[0], r[1], r[2])
    return rs


if __name__ == '__main__':
    run(DEFAULT)
