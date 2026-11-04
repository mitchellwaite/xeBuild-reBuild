"""fl5n.py <fl5f label> 'cond@site/arm cond@site/arm': diff; then the neighbourhood: each test's site, cond and arm varied in turn, arms 0-3 stores."""
import difflib, re, sys
import fllib as L, fl5lib as F, fl5f as X, fl5g as G, fl5i as I

ARMS = ['*buf = 0', '*buf = 0;\n@\tbuf[size] = 0', '*buf = 0;\n@\tbuf[size] = 0;\n@\tbuf[1] = 0', 'buf[size] = 0']
CONDS = ['off < -1', 'off < 0', 'pos < 0', 'size < 0', 'len < 0', 'n < 0']


def parse(t):
    r = []
    for x in t.split(' @@ '):
        m = re.match(r'(.*)@(\d+)/(\d+)$', x)
        r.append((m.group(1), int(m.group(2)), int(m.group(3))))
    return r


def build(base, ss, ts):
    s = base
    for c, p, a in sorted(ts, key=lambda x: -x[1]):
        s = I.ins(s, ss[p][0], ss[p][1], c, ARMS[a])
    return s


def lab(ts):
    return ' @@ '.join('%s@%d/%d' % t for t in ts)


if __name__ == '__main__':
    base = X.gen(*G.parse(sys.argv[1]))
    ss = I.sites(base)
    ts = parse(sys.argv[2])
    o = L.compile(build(base, ss, ts), None, 'a5n')
    x, y = F.norm(L.dis(L.REF))['_parseIni'], F.norm(L.dis(o))['_parseIni']
    print(F.nscore(o))
    print('\n'.join(l for l in difflib.unified_diff(x, y, lineterm='', n=0) if not l.startswith(('---', '+++'))))
    for p, c in enumerate(ss):
        pass
    V = {}
    for i in range(len(ts)):
        for p in range(len(ss)):
            t2 = list(ts)
            t2[i] = (ts[i][0], p, ts[i][2])
            V[lab(t2)] = build(base, ss, t2)
        for c in CONDS:
            for a in range(len(ARMS)):
                t2 = list(ts)
                t2[i] = (c, ts[i][1], a)
                V[lab(t2)] = build(base, ss, t2)
    print(len(V))
    F.run(V, 'n', show=12)
