"""mode_client attempt 4: each whole dead construct (mc4groups) plus every single mc1 edit.

python tools/wip/dehint/mc4gpair.py BASE.c G_dv,G_dz,G_kk [-j 6]"""
import os, re, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib

base = mc1lib.read_src(sys.argv[1])
want = sys.argv[2].split(',')
jobs = int(sys.argv[sys.argv.index('-j') + 1]) if '-j' in sys.argv else 6
t = mc1.build_template(base)
L = t.lists
def lists_with(lab):
    return {nm: [lab] for nm, v in L.items() if lab in v[1]}
G = {'G_dz': ({'dz': 1}, lists_with('dz')), 'G_dv': ({'dv': 1}, lists_with('dv')),
     'G_kk': ({'mc_kk': 1, 'r_memset': 1, 'r_ifkk': 1}, {}),
     'G_dy': ({'cebi_dy': 1, 'cp_dy_0': 1}, lists_with('dy'))}
SKIP = re.compile(r'^G_|^fk_all$|^rok_all$|^inline$|^-np$|cold_.*=2|fa([3-9]|1[0-9]|20)$')
es = [e for e in mc1.edits(t) if not SKIP.search(e[0])]
todo = []
for g in want:
    st, dr = G[g]
    for e in es:
        m = mc1.merge((st, dr, []), e[1:])
        if m:
            todo.append((g + ' + ' + e[0], m))
print(len(todo), flush=True)
res = []
with ThreadPoolExecutor(jobs) as ex:
    for (k, m), s in zip(todo, ex.map(lambda x: mc1.score(t, *x[1]), todo)):
        res.append((s.get('total') if not s.get('identical') else 0, k, s.get('count')))
        if s.get('identical'):
            print('HIT', k, s['count'], flush=True)
for r in sorted(res, key=lambda r: (r[0] is None, r[0]))[:25]:
    print(r)
