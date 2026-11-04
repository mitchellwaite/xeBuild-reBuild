"""fl9f.py: value searches through a pointer used twice (`p = &buf[pos]; n = memFindChar(p, ...); ... strncpy(tmp, p, ..)`).

Why: forwprop1 folds a single-use `&buf[pos]` into `buf + (pos + i)` (3 ivopts names per search); a pointer with two uses stays `p + i` (2 names).
One name fewer anywhere above slot 56 of ivopts' stack moves raw's nul one slot down (fl9b.py).
Axis pv: subset of b r f s v (bl, raw, flash, sec, version).  Labels: drops|pv=rf
"""
import itertools, os, sys
import fllib as L, fl6lib as F, fl8lib as G

N = "n = memFindChar(&buf[pos], 0, size - pos);"
NP = "p = &buf[pos];\n%sn = memFindChar(p, 0, size - pos);"
C8 = "strncpy(tmp, (char *)&buf[pos], 8);"
CN = "strncpy(tmp, (char *)&buf[pos], n);"
CP8 = "strncpy(tmp, (char *)p, 8);"
CPN = "strncpy(tmp, (char *)p, n);"
IND = {'bl': '\t\t\t\t', 'raw': '\t\t\t\t', 'flash': '\t\t\t\t\t', 'sec': '\t\t\t\t\t'}


def pv(which):
    def f(s):
        for c, sec in (('b', 'bl'), ('r', 'raw'), ('f', 'flash'), ('s', 'sec')):
            if c in which:
                s = F.secsub(s, sec, N, NP % IND[sec])
                if sec == 'raw':
                    s = F.secsub(s, sec, CN, CPN)
                else:
                    s = F.secsub(s, sec, C8, CP8)
        if 'v' in which:
            s = L.sub(s, "len = memFindChar(&buf[off], 0, sizeof(xb.kernelStr));", "p = &buf[off];\n\t\tlen = memFindChar(p, 0, sizeof(xb.kernelStr));")
            s = L.sub(s, "strncpy(xb.kernelStr, (char *)&buf[off], len);", "strncpy(xb.kernelStr, (char *)p, len);")
        return s
    return f


AX = ['b', 'r', 'f', 's', 'v']
SUBSETS = [''.join(c) for k in range(1, 6) for c in itertools.combinations(AX, k)]
G.E['pv'] = {x: pv(x) for x in SUBSETS}

if __name__ == '__main__':
    V = {}
    for d in G.SUBS:
        V[d + '|'] = G.state(d + '|')
        for x in SUBSETS:
            V['%s|pv=%s' % (d, x)] = G.state('%s|pv=%s' % (d, x))
    rs = G.run(V, 'x', 30)
    G.floors(rs)
