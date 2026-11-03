"""python tools/wip/dehint/nrtags.py <generator.py> <axis-count>: re-run a sweep, one fncmp per variant, then for each value of each
'|'-separated axis print the (V,C) histogram.  Finds which axis decides a result."""
import collections, importlib.util, os, subprocess, sys, json
sys.argv_saved = sys.argv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nrsweep

gen = sys.argv[1]
name = os.path.splitext(os.path.basename(gen))[0]
spec = importlib.util.spec_from_file_location(name, gen)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
out = os.path.join(nrsweep.ROOT, 'build', 'nr', name)
os.makedirs(out, exist_ok=True)
items = []
seen = set()
for v in m.variants():
    repl = tuple(v[2]) if len(v) > 2 else ()
    if (v[1], repl) in seen:
        continue
    seen.add((v[1], repl))
    items.append((v[0], v[1], os.path.join(out, 'v%d.c' % len(items)), list(repl)))
import concurrent.futures as cf
with cf.ThreadPoolExecutor(os.cpu_count() or 4) as ex:
    res = list(ex.map(nrsweep.run, items))
axes = collections.defaultdict(lambda: collections.Counter())
for r in res:
    for i, val in enumerate(r[3].split('|')):
        axes[(i, val)][(r[1] if r[1] < 10 ** 5 else 'X', r[2] if r[2] < 10 ** 5 else 'X')] += 1
for k in sorted(axes):
    print(k, sorted(axes[k].items(), key=lambda kv: str(kv[0]))[:8])
