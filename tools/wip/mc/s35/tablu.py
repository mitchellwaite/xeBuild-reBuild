import json, sys, os
os.environ['DUP'] = '1'; os.environ['LU'] = '1'
from concurrent.futures import ThreadPoolExecutor
import gs, ev, evdiff
st = json.load(open('st_S5.json')); bt = 'S5'; evdiff._C[bt] = evdiff.load(bt)
C = [c for c in gs.cands(st) if c['a'] and c['a'][-1][0].startswith('lu')]
def run(x):
    i, s = x; tag = 'u%d' % (i % 8)
    r = ev.ev(gs.build(s), tag, fncmp=True)
    if r is None: return None
    df, dP, a, b = evdiff.diff(bt, tag)
    return {'add': ([], s['a'][-1:]), 'score': r['score'], 'fncmp': r['fncmp'], 'nev': len(a) + len(b), 'df': {str(k): v for k, v in df.items() if k < 140}, 'dP': {}}
out = open('tablu_S5.jsonl', 'w', newline='\n')
with ThreadPoolExecutor(4) as ex:
    for res in ex.map(run, enumerate(C)):
        if res: out.write(json.dumps(res) + '\n'); out.flush()
