"""Probe only (never a source shape): can the magic test or head carry the needed frequency instead?

__builtin_expect on the second magic test, --param builtin-expect-probability=N, alloc test untouched.
Prints a= against the hinted build. A bb6 of N% of 8566; the alloc edge is 1.923% of that (needs >= 5226 total).
"""
import importlib.util, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.argv = ['cbsweep']
import cbsweep as cs

spec = importlib.util.spec_from_file_location('gen_cb7', os.path.join(HERE, 'gen_cb7.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
out = os.path.join(cs.ROOT, 'build', 'cb', 'ceprob2')
os.makedirs(out, exist_ok=True)
start, end = cs.BASE.index(cs.BOUNDS['ceDecrypt'][0]), cs.BASE.index(cs.BOUNDS['ceDecrypt'][1])
src = g.SRC.replace("if (BL_MAGIC(bl, 'E')) {", "if ((bl[0] & 0x43) == 0x43 && __builtin_expect(bl[1] == 'E', 1)) {", 1)
c = os.path.join(out, 'p.c')
open(c, 'w', newline='\n').write(cs.BASE[:start] + src + '\n' + cs.BASE[end:])
ref, rrd = cs.funcs(open(os.path.join(cs.ROOT, 'build', 'cb', 'gen_cb7', 'ref.s')).read())
for n in (59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 70, 72, 75):
    asm = os.path.join(out, 'p%d.s' % n)
    r = cs.compile_to(c, asm, ['--param', 'builtin-expect-probability=%d' % n])
    if r.returncode:
        print(n, r.stderr[:300])
        continue
    f, rd = cs.funcs(open(asm).read())
    d = [l for l in cs.udiff(ref['_ceDecrypt'], f['_ceDecrypt']) if l[0] in '+-']
    print(n, 'a=%d rd=%d' % (len(d), rd == rrd), ' | '.join(x.strip() for x in d[:4])[:100])
