"""ins77.py BASE.c OUT.jsonl [SITES] : loop-site asm-goto JMPs to post-loop case labels (77/79 etc.); inv/fncmp/cm/evdiff vs base."""
import sys, json, os, itertools
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ev, evdiff, cm, loopsites as L
D = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\build\v\mc37'
base = open(sys.argv[1]).read(); out = open(sys.argv[2], 'a')
TG = os.environ.get('TG', 'c9;c11;c9,c11;c11,c9;c10;c8;p1;i1').split(';')
sites = sys.argv[3].split(',') if len(sys.argv) > 3 else list(L.LS)
r0 = ev.ev(base, 'base', fncmp=True); evdiff._C['base'] = evdiff.load('base')
print('base', r0['score'], r0['fncmp'], file=out, flush=True)
jobs = [(s, t) for s in sites for t in TG]
def run(x):
    i, (s, t) = x; tag = os.environ.get('TP', 'j') + str(__import__('tt').tid())
    try: txt = L.add(base, s, t.split(','))
    except Exception as e: return None
    r = ev.ev(txt, tag, fncmp=True)
    if r is None: return {'s': s, 't': t, 'err': 1}
    df, dP, oa, ob = evdiff.diff('base', tag)
    c = cm.cm(os.path.join(D, 'v_%s.c' % tag))
    return {'s': s, 't': t, 'inv': r['score'], 'fncmp': r['fncmp'], 'cm': c, 'nev': len(oa) + len(ob),
            'df': {str(k): v for k, v in df.items()}, 'ins': [str(x) for x in ob if 'ins' in str(x)][:6], 'o': ' '.join(map(str, r['o'][12:]))}
with ThreadPoolExecutor(4) as ex:
    for res in ex.map(run, enumerate(jobs)):
        if res: print(json.dumps(res), file=out, flush=True)
