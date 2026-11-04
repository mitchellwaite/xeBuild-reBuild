"""fl10d.py n ax p [fn]: diff of an fl10c probe state, plus LRA's running usage for iniU32Invalid."""
import os, sys, difflib
import fllib as L, fl10lib as F, fl10c as C, fl10a as A

n, ax, p = int(sys.argv[1]), sys.argv[2], int(sys.argv[3])
fn = sys.argv[4] if len(sys.argv) > 4 else 'iniU32Invalid'
src = F.fk(C.body(n, '' if ax == '-' else ax))
fl = ['-O3'] + (['--param', 'builtin-expect-probability=%d' % p] if ax != '-' else [])
o = L.compile(src, fl, 'd10')
a, b = F.norm(L.dis(L.REF)), F.norm(L.dis(o))
print(F.nscore(o))
print('\n'.join(l for l in difflib.unified_diff(a['_' + fn], b['_' + fn], lineterm='', n=1) if not l.startswith(('---', '+++'))))
d = F.dumps(src, 'd10', F.DEF_DUMPS + fl[1:])
A.assign(d, fn)
