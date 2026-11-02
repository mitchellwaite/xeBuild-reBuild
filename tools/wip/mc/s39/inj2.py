"""inj2.py BASE.json BASETAG OUT.jsonl : injscan on voc design BASE with the B6 k67 post-transform; evdiff vs BASETAG."""
import json, sys, os
os.environ['DUP'] = '1'
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voc, ev, evdiff, k67
base = json.load(open(sys.argv[1])); bt = sys.argv[2]
post = lambda t: k67.inj(k67.lab(t), 'ip', 'pp')
jobs = []
for s in voc.SITES:
    if not (s.startswith('!') or s in ('elt<', 'enet<', 'eneg<', 'c6<', 'c7t<', 'c12t<')): continue
    for t in voc.targets_for(s): jobs.append(base + [[s, [t]]])
def run(x):
    i, e = x; tag = 'ij%d' % __import__('tt').tid()
    try: r = ev.ev(post(voc.make(e)), tag, fncmp=True)
    except Exception as ex: return {'e': e[-1], 'err': repr(ex)}
    if r is None: return None
    df, dP, a, b = evdiff.diff(bt, tag)
    return {'e': e[-1], 'score': r['score'], 'fncmp': r['fncmp'], 'df': {str(k): v for k, v in df.items() if k < 140}, 'nev': len(a) + len(b), 'o': ' '.join(map(str, r['o'][12:]))}
evdiff._C[bt] = evdiff.load(bt)
out = open(sys.argv[3], 'w', newline='\n')
with ThreadPoolExecutor(4) as ex:
    for res in ex.map(run, enumerate(jobs)):
        if res: out.write(json.dumps(res) + '\n'); out.flush()
