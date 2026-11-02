"""varscan.py STATE.json OUT.jsonl : vary each existing arm/eb item's form (all W forms) or drop it; real compile."""
import json, sys, os, copy
os.environ['DUP'] = '1'; os.environ['LU'] = '1'
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gs2, ev, ebl
st = json.load(open(sys.argv[1]))
FORMS = list(ebl.W)
def jobs():
    for k in ('a', 'e', 'v'):
        for i in range(len(st.get(k, []))):
            s = copy.deepcopy(st); del s[k][i]; yield ('drop', k, i), s
            if k == 'v': continue
            for w in FORMS:
                if w == st[k][i][2 if k == 'a' else 1]: continue
                s = copy.deepcopy(st); s[k][i][2 if k == 'a' else 1] = w; yield ('form', k, i, w), s
def run(x):
    j, (key, s) = x
    try: r = ev.ev(gs2.build(s), 'vs%d' % __import__('tt').tid(), True)
    except Exception as e: return {'k': key, 'err': repr(e)[:100]}
    if r is None: return {'k': key, 'err': 1}
    return {'k': key, 'score': r['score'], 'fncmp': r['fncmp'], 'o': ' '.join(map(str, r['o'][12:])), 'st': s}
out = open(sys.argv[2], 'w', newline='\n')
with ThreadPoolExecutor(4) as ex:
    for res in ex.map(run, enumerate(jobs())): out.write(json.dumps(res) + '\n'); out.flush()
