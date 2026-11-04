"""fl9i.py [drops..]: an unsigned index on some of bl's xb.files[blOrder[i]] (no (sizetype) statement at laddress, so one pop fewer before
rawPatch's chain: b = a * 1028 takes a high number, c the low one; see notes, attempt 9).  Label axis ui=<bitmask over the occurrences in bl>."""
import os, sys
os.environ.setdefault('FLA', 'a9')
import fllib as L, fl6lib as F, fl8lib as G

X = 'xb.files[blOrder[i]]'
Y = 'xb.files[(uint32_t)blOrder[i]]'


def ui(mask):
    def f(s):
        a, b = F.SECS['bl']
        i, j = s.index(a), s.index(b)
        t = s[i:j].split(X)
        out = t[0]
        for k, part in enumerate(t[1:]):
            out += (Y if mask >> k & 1 else X) + part
        return s[:i] + out + s[j:]
    return f


a, b = F.SECS['bl']
NOCC = G.S0[G.S0.index(a):G.S0.index(b)].count(X)
G.E['ui'] = {str(m): ui(m) for m in range(1 << NOCC)}

if __name__ == '__main__':
    print('occurrences', NOCC)
    drops = sys.argv[1:] or ['T1,T2,T3', 'T1,T3']
    V = {}
    for d in drops:
        for m in range(1 << NOCC):
            lb = '%s|ui=%d' % (d, m)
            V[lb] = G.state(lb)
    rs = G.run(V, 'i', 30)
    G.floors(rs)
