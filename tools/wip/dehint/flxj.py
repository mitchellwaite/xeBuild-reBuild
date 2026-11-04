"""flxj.py: fewer dead tests, longer arms (each store frees names at the same point).
Kept tests get k stores in their arm; arms sized independently.  A MATCH with fewer tests counts."""
import itertools, os, random, sys
from concurrent.futures import ThreadPoolExecutor
import fllib as L, flx as X, flx7 as T

ARM = {
 'nul': ('\t\t\tif (nul < -1)\n\t\t\t\tbuf[0] = 1;\n', '\t\t\tif (nul < -1) {\n%s\t\t\t}\n', '\t\t\t\t'),
 'i': ('\tif (i < -1)\n\t\tbuf[0] = 1;\n', '\tif (i < -1) {\n%s\t}\n', '\t\t'),
 'comma': ('\t\tif (comma < -1) {\n\t\t\tbuf[0] = 1;\n\t\t\tbuf[1] = 1;\n\t\t}\n', '\t\tif (comma < -1) {\n%s\t\t}\n', '\t\t\t'),
 'off4': ('\n\t\t\t\tif (off < -1)\n\t\t\t\t\tbuf[0] = 1;\n', '\n\t\t\t\tif (off < -1) {\n%s\t\t\t\t}\n', '\t\t\t\t\t'),
 'off5': ('\t\t\t\t\tif (off < -1)\n\t\t\t\t\t\tbuf[0] = 1;\n', '\t\t\t\t\tif (off < -1) {\n%s\t\t\t\t\t}\n', '\t\t\t\t\t\t'),
 'off3': ('\t\t\tif (off < -1)\n\t\t\t\tbuf[0] = 1;\n\t\t\tif (len > 21) {', '\t\t\tif (off < -1) {\n%s\t\t\t}\n\t\t\tif (len > 21) {', '\t\t\t\t'),
 'len': ('\t\t\t\tif (len < -1)\n\t\t\t\t\tbuf[0] = 1;\n', '\t\t\t\tif (len < -1) {\n%s\t\t\t\t}\n', '\t\t\t\t\t'),
}


def build(fl, keep):
    """keep: {test: k}"""
    dead = [d for d in X.ALLDEAD if d not in keep]
    s = X.gen(dead, fl)
    for n, k in keep.items():
        o, w, ind = ARM[n]
        s = L.sub(s, o, w % ''.join('%sbuf[%d] = 1;\n' % (ind, j) for j in range(k)))
    return s


if __name__ == '__main__':
    N = int(sys.argv[1])
    rng = random.Random(int(sys.argv[2]))
    V = {}
    names = list(ARM)
    while len(V) < N:
        nk = rng.choice([1, 2, 2, 2, 3, 3])
        ks = rng.sample(names, nk)
        fl = "nest"
        keep = {k: rng.randint(1, 16) for k in ks}
        V[fl + '|' + ','.join('%s=%d' % kv for kv in sorted(keep.items()))] = build(fl, keep)

    def one(kv):
        i, (n, s) = kv
        o = L.compile(s, None, 'j' + str(i))
        if o is None:
            return 10**7, '', n
        sc = L.score(o)
        v = T.vec(o)
        os.remove(o)
        return sc[0], v, n
    with ThreadPoolExecutor(4) as ex:
        rs = sorted(ex.map(one, enumerate(V.items())), key=lambda r: r[0])
    for r in rs[:25]:
        print(r)
    with open(L.BD + '/xj.txt', 'a', newline='\n') as f:
        for r in rs:
            f.write('%s\t%s\t%s\n' % r)
