"""tweak.py BASE.json : all single-site replacements/additions with 1-2 targets on top of BASE
(env SITES to restrict); prints the best few by score/fncmp. 4 threads."""
import json, itertools, sys, os
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voc, ev
base = json.load(open(sys.argv[1]))
sites = os.environ.get('SITES', '').split(',') if os.environ.get('SITES') else [s for s in voc.SITES if voc.targets_for(s)]
K = int(os.environ.get('K', '2'))
jobs = []
for s in sites:
    tg = voc.targets_for(s)
    rest = [x for x in base if x[0] != s]
    if len(rest) != len(base): jobs.append(rest)          # removal
    for k in range(1, K + 1):
        for c in itertools.combinations(tg, k):
            jobs.append(rest + [[s, list(c)]])
print(len(jobs), 'jobs', flush=True)
def run(x):
    i, e = x
    return e, ev.ev(voc.make(e), 'tw%d' % (i % 8))
res = []
with ThreadPoolExecutor(4) as ex:
    for e, r in ex.map(run, enumerate(jobs)):
        if r: res.append((r['score'], r.get('fncmp'), e, ' '.join(map(str, r['o'][11:]))))
res.sort(key=lambda x: (x[0], x[1]))
for r in res[:12]: print(r[0], r[1], json.dumps(r[2]), r[3])
json.dump(res[:200], open(os.environ.get('OUT', 'tweak.json'), 'w'))
