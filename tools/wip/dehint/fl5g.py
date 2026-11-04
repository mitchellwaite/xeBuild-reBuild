"""fl5g.py <label>..: parseIni diff for fl5f labels `a=v,b=w|t1+t2`."""
import difflib, os, sys
import fllib as L, fl5lib as F, fl5f as C


def parse(lb):
    a, _, t = lb.partition('|')
    c = dict(x.split('=') for x in a.split(',') if x)
    return c, tuple(x for x in t.split('+') if x)


if __name__ == '__main__':
    for n, lb in enumerate(sys.argv[1:]):
        s = C.gen(*parse(lb))
        open(os.path.join(F.A5, 'g_%d.c' % n), 'w', newline='\n').write(s)
        o = L.compile(s, None, 'a5g')
        print('==', lb, F.nscore(o))
        x, y = F.norm(L.dis(L.REF))['_parseIni'], F.norm(L.dis(o))['_parseIni']
        print('\n'.join(l for l in difflib.unified_diff(x, y, lineterm='', n=0) if not l.startswith(('---', '+++'))))
