"""js.py OUT.jsonl : jump-set variants around J1 (race-free)."""
import json, sys, os, copy
os.environ['DUP'] = '1'; os.environ['LU'] = '1'
from concurrent.futures import ThreadPoolExecutor
import gs2, ev, tt, loopsites as L
st = json.load(open('st_J1.json'))
LB = 'c1 c10 c11 c12 c2 c3 c7 c8 c9 cdef hdd4 hdd5 i0 i1 p0 p1 s5 u2'.split()
jobs = []
for x in LB:
    if x != 'p1':
        for tg in ([['p1', x]], [[x, 'p1']]):
            c = copy.deepcopy(st); c['j'] = [['eb', tg[0]]]; jobs.append(c)
for s in L.LS:
    if s == 'eb': continue
    for x in LB:
        c = copy.deepcopy(st); c['j'] = [['eb', ['p1']], [s, [x]]]; jobs.append(c)
out = open(sys.argv[1], 'w')
def f(c):
    try: r = ev.ev(gs2.build(c), 'J%d' % tt.tid(), fncmp=True)
    except Exception: return c, None
    return c, r
with ThreadPoolExecutor(4) as ex:
    for c, r in ex.map(f, jobs):
        if r: out.write(json.dumps({'c': c, 's': r['score'], 'f': r['fncmp'], 'o': r['o']}) + '\n'); out.flush()
