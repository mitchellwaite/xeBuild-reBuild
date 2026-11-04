"""fl10i.py <file.c>..: fl9h without fl8lib (which needs an old src): compares and dom3's PHI table per state."""
import glob, os, re, sys
import fl9a, fl9b, fllib as L

def ver(s):
    return int(s.rsplit('_', 1)[1])

def table(d, pas='dom3'):
    q = fl9b.fn(glob.glob(os.path.join(d, '-.*t.' + pas))[0])
    r = []
    for a, b in re.findall(r'(?m)^([\w.]*_\d+) -> \{ ([^}]*)\}', q):
        if '.MEM' in a:
            continue
        r.append((a, b.split()))
    return r, fl9a.defs(q)

for src in sys.argv[2:]:
    tag = os.path.basename(src)[:-2]
    d = fl9b.dump(src, tag)
    r, defs = table(d, sys.argv[1])
    rows = sorted(((min(ver(x) for x in o), a, o) for a, o in r), key=lambda t: t[0])
    print('#', tag, sys.argv[1])
    print('  ' + ' '.join('%s<-%s' % (a, '/'.join(o)) for _, a, o in rows if 'PHI' in defs.get(ver(a), '') and defs[ver(a)].count('(') >= 2))
