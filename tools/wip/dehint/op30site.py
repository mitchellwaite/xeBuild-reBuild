#!/usr/bin/env python3
"""Attempt 30: OPT / optIniBoolG assignments of the boolean sites on the natural source
(op30's nat+intb+pbfoldi = today's src/options.c without its comments).

python tools/wip/dehint/op30site.py [-all] [-base VARIANT]
  default: every subset of today's five optIniBoolG sites flipped back to OPT (32);
  -all: every assignment of the 13 sites (8192).
  prints each assignment's optlib score (0 = applyIniOptions identical), best first"""
import itertools, sys, os
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib, op30

a = sys.argv[1:]
base = 'nat+intb+pbfoldi'
if '-base' in a:
    i = a.index('-base'); base = a[i + 1]; del a[i:i + 2]
B = op30.apply(op30.SRC, base)
names = list(op30.SITES) if '-all' in a else op30.GSITES


def one(flips):
    t = B
    for n in flips:
        for x, y in op30.V['f_' + n]:
            t = t.replace(x, y, 1)
    r = optlib.score_text(t)
    per = r.get('per', {})
    return per.get('_applyIniOptions', 0) if 'total' in r else 99999, flips


combos = [c for k in range(len(names) + 1) for c in itertools.combinations(names, k)]
res = []
with ThreadPoolExecutor(8) as ex:
    for sc, fl in ex.map(one, combos):
        res.append((sc, fl))
        if sc == 0:
            print('IDENTICAL flips', fl, flush=True)
res.sort()
for sc, fl in res[:40]:
    print(sc, 'flipped:', ','.join(fl) or '-')
