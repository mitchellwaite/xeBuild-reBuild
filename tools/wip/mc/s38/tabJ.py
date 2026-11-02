"""tabJ.py STATE.json OUT.jsonl: one-step effect table (race-free tags), full order per candidate."""
import json, sys, os
os.environ['DUP'] = '1'; os.environ['LU'] = '1'; os.environ['XT'] = '1'
from concurrent.futures import ThreadPoolExecutor
import gs2, ev, tt
st0 = json.load(open(sys.argv[1])); out = open(sys.argv[2], 'w')
jobs = list(gs2.cands(st0))
def f(c):
    tag = 'T%d' % tt.tid()
    try: r = ev.ev(gs2.build(c), tag, fncmp=True)
    except Exception as e: return c, None
    return c, r
print(len(jobs), flush=True)
with ThreadPoolExecutor(int(os.environ.get('NT', '6'))) as ex:
    for c, r in ex.map(f, jobs):
        if r: out.write(json.dumps({'c': c, 's': r['score'], 'f': r['fncmp'], 'o': r['o']}) + '\n'); out.flush()
