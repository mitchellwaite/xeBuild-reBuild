"""fl5e.py <label> [..]: parseIni diff for fl5c labels `a=v,b=w|t1+t2`; writes the source to build/filelist_ini/a5/e_<n>.c"""
import difflib, os, sys
import fllib as L, fl5lib as F, fl5c as C

for n, lb in enumerate(sys.argv[1:]):
    a, _, t = lb.partition('|')
    c = dict(x.split('=') for x in a.split(',') if x)
    t = tuple(x for x in t.split('+') if x)
    s = C.gen(c, t)
    open(os.path.join(F.A5, 'e_%d.c' % n), 'w', newline='\n').write(s)
    o = L.compile(s, None, 'a5e')
    print('==', lb, F.nscore(o))
    x, y = F.norm(L.dis(L.REF))['_parseIni'], F.norm(L.dis(o))['_parseIni']
    print('\n'.join(l for l in difflib.unified_diff(x, y, lineterm='', n=0) if not l.startswith(('---', '+++'))))
