"""Probe only (never a source shape): which alloc-test probability does the original need?

Base shape with __builtin_expect on `if (buf)` and --param builtin-expect-probability=N, N = P(buf != 0).
Prints differing .s lines of ceDecrypt against the hinted build for each N, and which lines.
"""
import difflib, importlib.util, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.argv = ['cbsweep']
import cbsweep as cs

spec = importlib.util.spec_from_file_location('gen_cb7', os.path.join(HERE, 'gen_cb7.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
out = os.path.join(cs.ROOT, 'build', 'cb', 'ceprob')
os.makedirs(out, exist_ok=True)
start, end = cs.BASE.index(cs.BOUNDS['ceDecrypt'][0]), cs.BASE.index(cs.BOUNDS['ceDecrypt'][1])
src = g.SRC.replace('if (buf) {', 'if (__builtin_expect(buf != 0, 1)) {', 1)
c = os.path.join(out, 'p.c')
open(c, 'w', newline='\n').write(cs.BASE[:start] + src + '\n' + cs.BASE[end:])
ref, rrd = cs.funcs(open(os.path.join(cs.ROOT, 'build', 'cb', 'gen_cb7', 'ref.s')).read())
for n in (99, 98, 97, 96, 95, 94, 93, 92, 91, 90, 88, 86, 85, 80, 75, 70):
    asm = os.path.join(out, 'p%d.s' % n)
    r = cs.compile_to(c, asm, ['--param', 'builtin-expect-probability=%d' % n])
    if r.returncode:
        print(n, r.stderr[:300])
        continue
    f, rd = cs.funcs(open(asm).read())
    d = [l for l in cs.udiff(ref['_ceDecrypt'], f['_ceDecrypt']) if l[0] in '+-']
    print(n, 'a=%d rd=%d' % (len(d), rd == rrd), ' | '.join(x.strip() for x in d[:4])[:100])
