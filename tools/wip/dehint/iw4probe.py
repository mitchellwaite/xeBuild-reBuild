"""python tools/wip/dehint/iw4probe.py <base.c> [fn ...]: every single natural-shape change (iwanneal.SHAPES) from a base, with the lines per function.
With function names, prints only variants where each named function has fewer lines than in the base."""
import os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
args = sys.argv[1:]
sys.argv = ['x']
import iwanneal as A, iwlib

base = open(args[0], newline='').read().replace('\r\n', '\n')
fns = args[1:]
FLAGS = ['--param', 'builtin-expect-probability=50']
r0 = iwlib.score_text(base, FLAGS)
print('base', iwlib.fmt(r0))
items = []
for k, (old, news) in A.SHAPES.items():
    if old in base:
        for i, n in enumerate(news):
            items.append((k, i + 1, base.replace(old, n)))
print(len(items), 'variants')


def one(it):
    return it[0], it[1], iwlib.score_text(it[2], FLAGS)


with ThreadPoolExecutor(4) as ex:
    res = list(ex.map(one, items))
res.sort(key=lambda x: x[2].get('total', 1e9))
for k, i, r in res:
    if 'compile' in r:
        continue
    if r.get('identical'):
        print('IDENTICAL', k, i)
        continue
    if fns and not all(r['per'].get(f, 0) < r0['per'].get(f, 0) for f in fns):
        continue
    print(k, i, r['total'], {a: b for a, b in r['per'].items() if b < 9999})
