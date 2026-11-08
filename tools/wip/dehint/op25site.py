#!/usr/bin/env python3
"""Attempt 25: every OPT/optIniBoolG assignment of the 13 boolean sites on top of a base
variant of op25.py (default dzall), scored by optlib's line count.

python tools/wip/dehint/op25site.py [BASE] [-x extra+variants] [-s site1,site2 ..] > out.txt
  -s: only flip these sites (default all 13)"""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib
import op25

a = sys.argv[1:]
extra = ''
if '-x' in a:
    i = a.index('-x'); extra = '+' + a[i + 1]; del a[i:i + 2]
sites = list(op25.SITES)
if '-s' in a:
    i = a.index('-s'); sites = a[i + 1].split(','); del a[i:i + 2]
base = a[0] if a else 'dzall'


def one(combo):
    names = base + extra + ''.join('+f_' + s for s in combo)
    t = op25.apply(op25.SRC, names)
    r = optlib.score_text(t)
    tot = 0 if r.get('identical') else r.get('total', 99999)
    return tot, ','.join(combo) or '-'


combos = [c for n in range(len(sites) + 1) for c in itertools.combinations(sites, n)]
res = []
with ThreadPoolExecutor(6) as ex:
    for k, (tot, c) in enumerate(ex.map(one, combos)):
        res.append((tot, c))
        print(tot, c, flush=True)
res.sort()
print('# best', res[:15], file=sys.stderr)
