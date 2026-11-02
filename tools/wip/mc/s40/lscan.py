"""lscan.py BASE.json OUT.jsonl [sites]: on voc design BASE (DUP=1), label every client_usage call in the
option loop (lu0..), then for each loop site x usage label add { stmt JMP(luK); }; measure + evdiff vs BASE tag."""
import sys, json, os, re
os.environ['DUP'] = '1'
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voc, ev, evdiff, loopsites as L
base = json.load(open(sys.argv[1])); bt = sys.argv[1].replace('.json', '')
def labels(t):
    p0 = t.index('int mode_client('); p1 = t.index('NO_MODE_ARG', p0)
    seg = t[p0:p1]; k = [0]
    def rep(m):
        s = 'lu%d: %s' % (k[0], m.group(0)); k[0] += 1; return s
    seg = re.sub(r'client_usage\(\d, argv\[i\]\);', rep, seg)
    return t[:p0] + seg + t[p1:], k[0]
T0 = voc.make(base)
TL, NL = labels(T0)
def mk(edits):
    t = TL
    for s, tg in edits: t = L.add(t, s, tg)
    return t
def run(x):
    i, e = x; tag = 'ls%d' % __import__('tt').tid()
    try: t = mk(e)
    except Exception as ex: return {'e': e, 'err': repr(ex)}
    r = ev.ev(t, tag, fncmp=True)
    if r is None: return {'e': e, 'err': 'build'}
    df, dP, a, b = evdiff.diff(bt, tag)
    return {'e': e, 'score': r['score'], 'fncmp': r['fncmp'], 'df': {str(k): v for k, v in df.items()}, 'nev': len(a) + len(b), 'o': ' '.join(map(str, r['o'][12:]))}
if __name__ == '__main__':
    r = ev.ev(TL, bt, fncmp=True); print('labelled base', r['score'], r['fncmp'], NL, flush=True)
    evdiff._C[bt] = evdiff.load(bt)
    sites = sys.argv[3].split(',') if len(sys.argv) > 3 else list(L.LS)
    jobs = [[[s, ['lu%d' % k]]] for s in sites for k in range(NL)]
    out = open(sys.argv[2], 'w', newline='\n')
    with ThreadPoolExecutor(4) as ex:
        for res in ex.map(run, enumerate(jobs)):
            out.write(json.dumps(res) + '\n'); out.flush()
