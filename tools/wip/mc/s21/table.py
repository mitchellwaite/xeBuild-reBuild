"""table.py OUT.json [BASE.json]: measure every single s19 injection (t,s,w) on top of BASE
(default none): fq delta per block vs base, inv, missing blocks. Parallel (8 procs)."""
import ast, json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, os.path.join(ROOT, 'tools', 'wip', 'mc', 's19'))
import search, srcx
D = os.path.join(ROOT, 'build', 'v', 'mc21'); PY = sys.executable
NEED = [129, 107, 109, 110, 113, 108, 119, 120, 121, 128, 116, 132, 49, 112, 115, 103, 55, 126, 125, 61, 33, 29, 67,
        127, 117, 130, 35, 42, 53, 77, 79]
WSET = os.environ.get('WSET', 'b,p,pp,ppp,q').split(',')
def meas(inj, tag):
    p = os.path.join(D, 'v_%s.c' % tag); sd = os.path.join(D, 'slot_%s' % tag)
    open(p, 'w', newline='\n').write(search.make(inj))
    r = subprocess.run([PY, os.path.join(ROOT, 'tools/wip/mc/s19/mkslot.py'), p, sd], capture_output=True, text=True)
    if r.returncode: return None
    r = subprocess.run([PY, os.path.join(ROOT, 'tools/wip/mc/s18/analyze.py'), sd], capture_output=True, text=True)
    try:
        l = r.stdout.strip().splitlines()
        o = [int(x) for x in l[2].split()[1:]]
        miss = [b for b in NEED if b not in o]
        return {'fq': ast.literal_eval(l[0])['fq'], 'inv': int(l[1].split()[1]) + 5 * len(miss), 'order': l[2], 'needmiss': miss}
    except Exception:
        return None
if __name__ == '__main__':
    base = [tuple(x) for x in json.load(open(sys.argv[2]))] if len(sys.argv) > 2 else []
    b = meas(base, 'base'); print('base inv', b['inv'], flush=True)
    jobs = [(t, s, w) for t in range(len(search.TGT)) for s in search.SRCS if search.ok(t, s) for w in WSET]
    def one(j):
        k = '%d_%s_%s' % j
        return j, meas(base + [j], k)
    out = {'base': base, 'basefq': b['fq'], 'baseinv': b['inv'], 'rows': []}
    with ThreadPoolExecutor(8) as ex:
        for j, r in ex.map(one, jobs):
            if r is None: continue
            d = {k: r['fq'].get(k, 0) - b['fq'].get(k, 0) for k in set(r['fq']) | set(b['fq'])}
            d = {k: v for k, v in d.items() if v}
            miss = [k for k in b['fq'] if k not in r['fq']]
            out['rows'].append({'inj': j, 'd': d, 'inv': r['inv'], 'miss': miss + r['needmiss']})
            print(j, r['inv'], d, miss, flush=True)
    json.dump(out, open(sys.argv[1], 'w'))
