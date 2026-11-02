"""ebscan.py STATE.json BASETAG OUT.jsonl [FORMS] : single bcp eb-copy sources on STATE (gs.build), evdiff vs BASETAG."""
import json, sys, os
os.environ['DUP'] = '1'; os.environ['LU'] = '1'
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gs, ev, evdiff, ebl
st = json.load(open(sys.argv[1])); bt = sys.argv[2]; T0 = gs.build(st); E0 = [tuple(x) for x in st.get('e', [])]
forms = sys.argv[4].split(',') if len(sys.argv) > 4 else list(ebl.W)
evdiff._C[bt] = evdiff.load(bt)
jobs = [[(s, w, t, 90 + 10 * len(st.get('e', [])))] for s in ebl.SRCS for t in ebl.fwd(s) for w in forms]
def run(x):
    i, it = x; tag = 'e%d' % (i % 4)
    try: r = ev.ev(ebl.ebinj(T0, E0 + it), tag, fncmp=True)
    except Exception as e: return {'it': it, 'err': repr(e)[:200]}
    if r is None: return {'it': it, 'err': 1}
    df, dP, a, b = evdiff.diff(bt, tag)
    return {'it': it, 'score': r['score'], 'fncmp': r['fncmp'], 'nev': len(a) + len(b),
            'df': {str(k): v for k, v in df.items() if k < 140}, 'o': ' '.join(map(str, r['o'][12:]))}
out = open(sys.argv[3], 'w', newline='\n')
with ThreadPoolExecutor(4) as ex:
    for res in ex.map(run, enumerate(jobs)): out.write(json.dumps(res) + '\n'); out.flush()
