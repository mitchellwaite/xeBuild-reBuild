"""fl9h.py <label|file.c> ..: for each state, the four comma/nul compares as dom3 leaves them, and dom3's update_ssa PHI order.
Ref's forms: bl nul < comma, raw nul > comma, flash nul > comma, sec nul < comma (operands are ordered by version).
Line: A B D E verdicts, then the PHI list `new<-old` in ascending old order from len_10 on."""
import glob, os, re, sys
os.environ.setdefault('FLA', 'a9')
import fllib as L, fl8lib as G
try:
    import fl9f
except Exception:
    pass
import fl9a, fl9b

CMP = re.compile(r'if \((?:(i_\d+) ([<>=]+) (_\d+)|(_\d+) ([<>=]+) (i_\d+))\)')
WANT = {'A': 'low', 'B': 'high', 'D': 'high', 'E': 'low'}


def ver(s):
    return int(s.rsplit('_', 1)[1])


def analyse(d):
    q = fl9b.fn(glob.glob(os.path.join(d, '-.*t.optimized'))[0])
    cmps = []
    for m in CMP.finditer(q):
        i, nul = (m.group(1), m.group(3)) if m.group(1) else (m.group(6), m.group(4))
        cmps.append((ver(nul), ver(i)))
    # the four are the ones among parseIni's compares at i of memFindChar; n_ ones are excluded by the pattern, first is bl's strncmp-like
    cmps = cmps[-7:] if len(cmps) >= 7 else cmps
    return cmps


def table(d):
    q = fl9b.fn(glob.glob(os.path.join(d, '-.*t.dom3'))[0])
    r = []
    for a, b in re.findall(r'(?m)^([\w.]*_\d+) -> \{ ([^}]*)\}', q):
        if '.MEM' in a:
            continue
        r.append((a, b.split()))
    defs = fl9a.defs(q)
    return r, defs


def main(lb, i):
    if lb.endswith('.c'):
        src = lb
        tag = os.path.basename(lb)[:-2]
    else:
        tag = 'h%d' % i
        src = os.path.join(L.BD, 'a9', tag + '.c')
        open(src, 'w', newline='\n').write(G.state(lb))
    d = fl9b.dump(src, tag)
    print('#', lb)
    print('  compares (nul, comma):', analyse(d))
    r, defs = table(d)
    rows = sorted(((min(ver(x) for x in o), a, o) for a, o in r), key=lambda t: t[0])
    print('  ' + ' '.join('%s<-%s' % (a, '/'.join(o)) for _, a, o in rows if 'PHI' in defs.get(ver(a), '') and defs[ver(a)].count('(') >= 2))


for i, lb in enumerate(sys.argv[1:]):
    main(lb, i)
