"""k67.py BASE.json OUT.jsonl : label k67l before the -e test (else-if tail wrapped in else { }) on a voc
design (DUP=1); sources = bcp gotos at arm starts (W forms) and loop-site JMP(k67l). measure + evdiff."""
import sys, json, os
os.environ['DUP'] = '1'
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voc, ev, evdiff, loopsites as L, inj48
K = '} else if (E(!strnicmp(argv[i], "-e", 2))) {'
U = 'client_usage(1, argv[i]);\n\t}'
ARMS = {'top': '\t\tif (!strnicmp(argv[i], "help", 2)',
        'noent': 'promptEnter = 0;',
        'rbt': 'if (reboot == 1)',
        's': 'if (reboot == 2)',
        'keys': 'mode = 3;',
        'ip': 'ip = argv[++i];',
        'r': 'setting read filename to %s',
        'w': 'setting write filename to %s',
        'rb': 'arg = getArgs(argc, argv, &i, mode, 1, &start, &count);'}
def lab(t, name='k67l'):
    assert K in t
    return t.replace(K, '} else { %s: if (E(!strnicmp(argv[i], "-e", 2))) {' % name).replace(U, 'client_usage(1, argv[i]); }\n\t}')
def inj(t, arm, w, n=10, tgt='k67l'):
    a = ARMS[arm]; p = t.index(a, t.index('int mode_client('))
    if arm in ('r', 'w'): p = t.rindex('\t\t\tlog_printf', 0, p)    # before the log_printf statement
    elif not a.startswith('\t'): pass
    s = 'if (%s) goto %s;\n' % (inj48.W[w]('i + %d' % n), tgt)
    return t[:p] + s + t[p:]
def variants(T):
    yield ('label',), T
    for arm in ARMS:
        for w in ('b', 'p', 'q', 'pp', 'qq', 'pq'):
            yield ('inj', arm, w), inj(T, arm, w)
    for s in ['nent', 'rbs', 'rbt', 'sig', 'sset', 'keys', 'ip', 'bp', 'rb', 'wb', 'eb', 'r', 'w', 'u0']:
        try: yield ('jmp', s), L.add(T, s, ['k67l'])
        except Exception as e: pass
if __name__ == '__main__':
    base = json.load(open(sys.argv[1])); bt = os.path.basename(sys.argv[1]).replace('.json', '')
    T = lab(voc.make(base))
    evdiff._C[bt] = evdiff.load(bt)
    jobs = list(variants(T))
    def run(x):
        i, (k, t) = x; tag = 'k%d' % __import__('tt').tid()
        r = ev.ev(t, tag, fncmp=True)
        if r is None: return {'k': k, 'err': 1}
        df, dP, a, b = evdiff.diff(bt, tag)
        return {'k': k, 'score': r['score'], 'fncmp': r['fncmp'], 'nev': len(a) + len(b),
                'df': {str(q): v for q, v in df.items() if q < 140}, 'o': ' '.join(map(str, r['o'][12:]))}
    out = open(sys.argv[2], 'w', newline='\n')
    with ThreadPoolExecutor(4) as ex:
        for res in ex.map(run, enumerate(jobs)): out.write(json.dumps(res) + '\n'); out.flush()
