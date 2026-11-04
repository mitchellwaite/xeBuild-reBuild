"""fl10j.py <pass> <tag>..: full replacement table of a pass for a9/iv_<tag> (new<-old ascending old, what new is); after fl10i has dumped."""
import glob, os, re, sys
import fl9a, fl9b, fllib as L
def ver(s): return int(s.rsplit('_', 1)[1])
pas = sys.argv[1]
for tag in sys.argv[2:]:
    d = os.path.join(L.A9 if hasattr(L,'A9') else os.path.join(L.BD,'a9'), 'iv_' + tag)
    q = fl9b.fn(glob.glob(os.path.join(d, '-.*t.' + pas))[0])
    defs = fl9a.defs(q)
    rows = []
    for a, b in re.findall(r'(?m)^([\w.]*_\d+) -> \{ ([^}]*)\}', q):
        if '.MEM' in a: continue
        o = b.split()
        rows.append((min(ver(x) for x in o), a, o))
    print('#', tag, pas, len(rows))
    for m, a, o in sorted(rows):
        print('  %-12s <- %-30s %s' % (a, ' '.join(o)[:30], defs.get(ver(a), '')[:70]))
