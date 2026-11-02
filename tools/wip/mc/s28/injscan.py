"""injscan.py BASE.json BASETAG OUT.jsonl : add each single bcp injection (1 target) to BASE, compile,
evdiff vs BASETAG's slot; records f/P deltas, event neutrality, score."""
import json, sys, os
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voc, ev, evdiff
base = json.load(open(sys.argv[1])); bt = sys.argv[2]
jobs = []
for s in voc.SITES:
    if not (s.startswith('!') or s in ('elt<', 'enet<', 'eneg<', 'c6<', 'c7t<', 'c12t<')): continue
    for t in voc.targets_for(s):
        jobs.append(base + [[s, [t]]])
def run(x):
    i, e = x; tag = 'ij%d' % (i % 6)
    r = ev.ev(voc.make(e), tag, fncmp=False)
    if r is None: return None
    df, dP, a, b = evdiff.diff(bt, tag)
    return {'e': e[-1], 'score': r['score'], 'df': {str(k): v for k, v in df.items()}, 'dP': {str(k): v for k, v in dP.items()},
            'nev': len(a) + len(b), 'o': ' '.join(map(str, r['o'][12:]))}
evdiff._C[bt] = evdiff.load(bt)
out = open(sys.argv[3], 'w', newline='\n')
with ThreadPoolExecutor(3) as ex:
    for res in ex.map(run, enumerate(jobs)):
        if res: out.write(json.dumps(res) + '\n'); out.flush()
