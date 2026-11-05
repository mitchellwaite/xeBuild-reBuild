"""python tools/wip/dehint/irname2.py <gen_irN.py> <fn> <regex> [limit]: for generator variants, the line of fn's optimized dump matching regex, with the diff size; groups variants by it."""
import collections, importlib.util, itertools, os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import irlib
import irsweep

gen, fn, rx = sys.argv[1:4]
limit = int(sys.argv[4]) if len(sys.argv) > 4 else 300
m = irsweep.load(gen)
base = open(os.path.join(irlib.R, getattr(m, 'BASE', 'src/image_read.c')), newline='').read().replace('\r\n', '\n')
combos = list(itertools.product(*m.AXES))[:limit]


def one(combo):
    text = irsweep.build(base, combo)
    ok, o, d = irlib.compile_src(text, [], extra=['-fdump-tree-optimized'])
    if not ok:
        return None
    idn, tot, per, notes = irlib.report(o)
    f = [x for x in os.listdir(d) if x.endswith('optimized')]
    t = open(os.path.join(d, f[0]), errors='replace').read()
    i = t.find(';; Function %s ' % fn)
    j = t.find('\n;; Function ', i + 10)
    hits = re.findall(rx, t[i:j])
    irlib.cleanup(d)
    return '+'.join(c[0] for c in combo), per.get('_' + fn, 0), tuple(hits)


g = collections.defaultdict(list)
with ThreadPoolExecutor(8) as ex:
    for r in ex.map(one, combos):
        if r:
            g[r[2]].append((r[1], r[0]))
for k, v in sorted(g.items(), key=lambda kv: min(kv[1])):
    print(min(v)[0], len(v), k, min(v)[1])
