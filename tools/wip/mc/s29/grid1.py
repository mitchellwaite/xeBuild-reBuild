import json, itertools, sys, os
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, '.')
import voc, ev
C = ['c1', 'c2', 'c3', 'c8', 'c9', 'c11']
jobs = []
for a in C:
    for b in C:
        for c in C + [None]:
            if len({a, b, c} - {None}) < (3 if c else 2): continue
            e = [['h4>', ['u2']], [a + '<', ['hdd4', 's4']], [b + '<', ['hdd5', 's5']]]
            if c: e.append([c + '<', ['hdd5', 's5']])
            jobs.append(e)
def run(x):
    i, e = x
    return e, ev.ev(voc.make(e), 'gr%d' % (i % 8))
res = []
with ThreadPoolExecutor(4) as ex:
    for e, r in ex.map(run, enumerate(jobs)):
        if r: res.append((r['score'], r.get('fncmp'), e, ' '.join(map(str, r['o']))))
res.sort(key=lambda x: (x[0], x[1]))
for r in res[:15]: print(r)
json.dump(res, open('grid1.json', 'w'))
