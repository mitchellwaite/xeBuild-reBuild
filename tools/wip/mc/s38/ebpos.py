"""ebpos.py OUT.jsonl : JMP(targets) at statement positions of the -eb / -wb / -bp / -rb arms of H5b; inv/fncmp/cm."""
import sys, os, json, re
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ev, cm
D = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\build\v\mc38'
base = open('H5b.c').read(); p0 = base.index('int mode_client('); p1 = base.index('switch', p0)
# every statement end ';' inside the option loop region
pos = [m.end() for m in re.finditer(r';\n', base[p0:p1])]
pos = [p0 + x - 1 for x in pos]
TG = os.environ.get('TG', 'p1;p0;c7;c9;c11;c9,c11').split(';')
jobs = [(q, t) for q in pos for t in TG]
def run(x):
    i, (q, t) = x; import tt; tag = 'e%d' % tt.tid()
    txt = base[:q] + ' JMP(%s);' % t + base[q:]
    # must be inside a block: wrap as statement after ';' works only if not in if-without-braces; accept compile errors
    r = ev.ev(txt, tag, fncmp=True)
    if r is None: return None
    c = cm.cm(os.path.join(D, 'v_%s.c' % tag)) if r['score'] <= 7 else None
    ln = base.count('\n', 0, q) + 1
    return {'line': ln, 't': t, 'inv': r['score'], 'fncmp': r['fncmp'], 'cm': c, 'o': ' '.join(map(str, r['o']))}
out = open(sys.argv[1], 'a')
with ThreadPoolExecutor(4) as ex:
    for res in ex.map(run, enumerate(jobs)):
        if res: print(json.dumps(res), file=out, flush=True)
