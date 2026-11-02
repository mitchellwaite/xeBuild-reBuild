"""tab3.py STATE.json BASETAG OUT.jsonl : effect table of gs2 candidates on STATE (evdiff vs BASETAG)."""
import json, sys, os
os.environ['DUP'] = '1'; os.environ['LU'] = '1'
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gs2, ev, evdiff
st = json.load(open(sys.argv[1])); bt = sys.argv[2]; evdiff._C[bt] = evdiff.load(bt)
def run(x):
    i, s = x; tag = os.environ.get('TP', 't') + '%d' % __import__('tt').tid()
    try: r = ev.ev(gs2.build(s), tag, fncmp=True)
    except Exception: return None
    if r is None: return None
    try: df, dP, a, b = evdiff.diff(bt, tag)
    except Exception: return None
    add = (s['v'][len(st['v']):], s['a'][len(st['a']):], s['e'][len(st.get('e', [])):])
    return {'add': add, 'score': r['score'], 'fncmp': r['fncmp'], 'nev': len(a) + len(b), 'o': ' '.join(map(str, r['o'][12:])),
            'df': {str(k): v for k, v in df.items() if k < 140}, 'dP': {str(k): v for k, v in dP.items() if k < 140}}
done = set()
if os.path.exists(sys.argv[3]):
    for l in open(sys.argv[3]): done.add(json.dumps(json.loads(l)['add']))
out = open(sys.argv[3], 'a', newline='\n')
def todo():
    for s in gs2.cands(st):
        if json.dumps([s['v'][len(st['v']):], s['a'][len(st['a']):], s['e'][len(st.get('e', [])):]]) not in done: yield s
with ThreadPoolExecutor(4) as ex:
    for res in ex.map(run, enumerate(todo())):
        if res: out.write(json.dumps(res) + '\n'); out.flush()
