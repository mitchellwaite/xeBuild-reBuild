"""fl5k2.py scan/cmp/tail/wrap/gets [fn..]: per-getter diffs of an fl5k state"""
import difflib, sys
sys.argv, av = sys.argv[:1], sys.argv[1:]
import fllib as L, fl5lib as F
src = open(__file__.replace('fl5k2', 'fl5k')).read().split("\nV = {}\n")[0]
exec(src)
c = av[0].split('/')
s = gen(*c)
o = L.compile(s, None, 'a5k2')
x, y = F.norm(L.dis(L.REF)), F.norm(L.dis(o))
for fn in av[1:] or ['_getIniBool', '_iniBoolInvalid', '_getIniU32', '_iniU32Invalid']:
    print('==', fn)
    print('\n'.join(l for l in difflib.unified_diff(x[fn], y[fn], lineterm='', n=0) if not l.startswith(('---', '+++'))))
