"""python tools/wip/dehint/irname.py <gen_irN.py> [limit] : for generator variants, parseDump's site 2 compare in the optimized dump (the `if` right after
the log of `dst == -4`'s remap loop) and the diff size; groups variants by that compare.  Shows how far SSA names can be pushed by spelling alone."""
import collections, importlib.util, itertools, os, random, re, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import irlib

gen = sys.argv[1]
limit = int(sys.argv[2]) if len(sys.argv) > 2 else 200
s = importlib.util.spec_from_file_location('gen', gen)
m = importlib.util.module_from_spec(s)
s.loader.exec_module(m)
base = open(os.path.join(irlib.R, getattr(m, 'BASE', 'src/image_read.c')), newline='').read().replace('\r\n', '\n')
combos = list(itertools.product(*m.AXES))
random.seed(1)
if len(combos) > limit:
    combos = random.sample(combos, limit)


def one(c):
    t = base
    for lab, ed in c:
        for a, b in ed:
            if a not in t:
                return None
            t = t.replace(a, b)
    ok, o, d = irlib.compile_src(t, [], extra=['-fdump-tree-optimized'])
    if not ok:
        irlib.cleanup(d)
        return None
    idn, tot, per, notes = irlib.report(o)
    f = [x for x in os.listdir(d) if x.endswith('optimized')]
    txt = open(os.path.join(d, f[0]), errors='replace').read() if f else ''
    irlib.cleanup(d)
    i = txt.find(';; Function parseDump')
    txt = txt[i:]
    j = txt.find('== -4)')
    mm = None
    for mm in re.finditer(r'if \(([\w.]+ == [\w.]+)\)', txt[j:]):
        if not re.search(r'== -?\d+$', mm.group(1)):
            break
    return ('+'.join(x[0] for x in c if x[0]), re.sub(r'_(\d+)', r'_\1', mm.group(1)) if mm else '?', per.get('_parseDump', 0))


with ThreadPoolExecutor(4) as ex:
    res = [r for r in ex.map(one, combos) if r]
g = collections.defaultdict(list)
for lab, cmp_, n in res:
    g[cmp_].append((n, lab))
for k in sorted(g):
    v = sorted(g[k])
    print(k, len(v), 'best', v[0])
    if os.environ.get('IRNAMEALL'):
        for n, lab in v:
            if lab.count('+') <= int(os.environ['IRNAMEALL']):
                print('    ', n, lab)
