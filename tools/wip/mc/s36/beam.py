"""beam.py TAB.jsonl STATE.json OUT.jsonl K : expand the K best distinct-order plateau states of TAB (relative to
STATE) with every gs candidate (real compiles, LU=1); writes all results; best printed."""
import json, sys, os
os.environ['DUP'] = '1'; os.environ['LU'] = '1'
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gs, ev
st = json.load(open(sys.argv[2])); K = int(sys.argv[4])
L = sorted((json.loads(l) for l in open(sys.argv[1])), key=lambda x: (x['score'], x['fncmp']))
seeds = []; seen = set()
for x in L:
    k = (x['score'], x['fncmp'])
    if k in seen: continue
    seen.add(k); seeds.append({'v': st['v'] + x['add'][0], 'a': st['a'] + x['add'][1]})
    if len(seeds) == K: break
jobs = [(si, c) for si, s in enumerate(seeds) for c in gs.cands(s)]
print('jobs', len(jobs), flush=True)
def run(x):
    i, (si, s) = x
    try: r = ev.ev(gs.build(s), 'b%d' % (i % 8), fncmp=True)
    except Exception: return None
    if r is None: return None
    return {'s': s, 'score': r['score'], 'fncmp': r['fncmp'], 'o': ' '.join(map(str, r['o'][12:]))}
out = open(sys.argv[3], 'w', newline='\n'); best = (99, 0)
with ThreadPoolExecutor(4) as ex:
    for res in ex.map(run, enumerate(jobs)):
        if res:
            out.write(json.dumps(res) + '\n'); out.flush()
            if (res['score'], res['fncmp']) < best: best = (res['score'], res['fncmp']); print('best', best, res['o'][:80], flush=True)
