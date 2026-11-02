"""tab.py STATE.json BASETAG OUT.jsonl : effect table: each gs candidate on STATE, real compile, evdiff vs BASETAG."""
import json, sys, os
os.environ['DUP'] = '1'
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gs, ev, evdiff
st = json.load(open(sys.argv[1])); bt = sys.argv[2]
evdiff._C[bt] = evdiff.load(bt)
def run(x):
    i, s = x; tag = 't%d' % __import__('tt').tid()
    try: r = ev.ev(gs.build(s), tag, fncmp=True)
    except Exception: return None
    if r is None: return None
    df, dP, a, b = evdiff.diff(bt, tag)
    add = (s['v'][len(st['v']):], s['a'][len(st['a']):])
    return {'add': add, 'score': r['score'], 'fncmp': r['fncmp'], 'nev': len(a) + len(b),
            'df': {str(k): v for k, v in df.items() if k < 140}, 'dP': {str(k): v for k, v in dP.items() if k < 140}}
out = open(sys.argv[3], 'w', newline='\n')
with ThreadPoolExecutor(4) as ex:
    for res in ex.map(run, enumerate(gs.cands(st))):
        if res: out.write(json.dumps(res) + '\n'); out.flush()
