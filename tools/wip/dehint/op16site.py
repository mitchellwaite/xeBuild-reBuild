"""Attempt 16: OPT/optIniBoolG site assignments on the natural parseButton split base
(op16nat.py), optionally with extra edits.

python tools/wip/dehint/op16site.py [-x e1,e2] [-k K | -all] [-only s1,..] [-out file]
  results (score, flipped sites) are written to -out (default build/op/a16/site.txt)"""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib
import op16nat

a = sys.argv[1:]
base = op16nat.natural()
if '-x' in a:
    base = op16nat.edits(base, a[a.index('-x') + 1].split(','))
pool = op16nat.SITES
if '-only' in a:
    pool = a[a.index('-only') + 1].split(',')
K = int(a[a.index('-k') + 1]) if '-k' in a else 2
if '-all' in a:
    K = len(pool)
out = a[a.index('-out') + 1] if '-out' in a else os.path.join(optlib.BUILD, 'a16', 'site.txt')
combos = [c for k in range(0, K + 1) for c in itertools.combinations(pool, k)]
print('sites', pool, len(combos), 'combinations', flush=True)


def run(c):
    return c, optlib.score_text(op16nat.flip(base, c))


res = []
with open(out, 'w', newline='\n') as f, ThreadPoolExecutor(4) as ex:
    for c, r in ex.map(run, combos):
        s = 0 if r.get('identical') else r.get('total', 99999)
        res.append((s, c, r))
        f.write('%d %s %s %s\n' % (s, ','.join(c) or '-', r.get('per'), ' '.join(r.get('notes', []))))
        f.flush()
        if r.get('identical'):
            print('IDENTICAL', c, flush=True)
res.sort(key=lambda x: x[0])
for s, c, r in res[:30]:
    print(s, ','.join(c) or '-', r.get('per'), ' '.join(r.get('notes', [])))
