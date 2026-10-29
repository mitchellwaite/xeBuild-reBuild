"""Greedy search over mode_client edge-probability overrides (tools/wip/mcfdo.py).

python tools/wip/mcfdo_search.py <dir> <draft.c> [start overrides...]
Every two-way block of the profile_estimate dump is a knob; each round tries
setting one edge of every knob to each of VALS (and dropping its override)
and keeps the best single change.  Env: VALS (comma list, %), JOBS (4).
"""
import importlib.util, os, queue, sys
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mcfdo
spec = importlib.util.spec_from_file_location('gcda', os.path.join(ROOT, 'tools', 're', 'gcda.py'))
gcda = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gcda)

d, draft = sys.argv[1:3]
mcfdo.prep(d, draft)
est, _ = gcda.read_dump(os.path.join(d, 'm.c.042t.profile_estimate'))
fn = est['mode_client']
knobs = sorted((bb, min(v[1])) for bb, v in fn.items() if len(v[1]) == 2)
vals = [float(x) for x in os.environ.get('VALS', '2,10,25,40,50,60,75,90,98').split(',')]
jobs = int(os.environ.get('JOBS', '4'))


def parse(o):
    k, p = o.split('=')
    s, t = k.split(':')[1].split('>')
    return (int(s), int(t)), float(p)


cur = dict(parse(o) for o in sys.argv[3:])
cache = {}


def ev(ov, slot):
    key = tuple(sorted(ov.items()))
    if key not in cache:
        cache[key] = mcfdo.score(d, ['mode_client:%d>%d=%g' % (s, t, p) for (s, t), p in key], slot)[0]
    return cache[key]


slots = queue.Queue()
for k in range(1, jobs + 1):
    slots.put(k)


def run(ov):
    """ev in a free slot directory (one .gcda per concurrent compile)"""
    k = slots.get()
    try:
        return ev(ov, k)
    finally:
        slots.put(k)


def show(ov):
    return ' '.join('mode_client:%d>%d=%g' % (s, t, p) for (s, t), p in sorted(ov.items()))


best = ev(cur, 0)
print('knobs', len(knobs), 'start', best, flush=True)
with ThreadPoolExecutor(jobs) as ex:
    while True:
        cands = []
        for bb, dst in knobs:
            key = (bb, dst)
            for v in vals + [None]:
                ov = dict(cur)
                if v is None:
                    if key not in ov:
                        continue
                    del ov[key]
                else:
                    if ov.get(key) == v:
                        continue
                    ov[key] = v
                cands.append(ov)
        res = list(ex.map(run, cands))
        i = min(range(len(res)), key=lambda j: res[j])
        if res[i] >= best:
            break
        best, cur = res[i], cands[i]
        print(best, show(cur), flush=True)
print('final', best, show(cur))
