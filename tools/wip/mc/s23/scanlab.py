"""scanlab.py BASE.json TAG [SPECS0...]: measure every single label spec (lab.PAT x hot/cold) on top of
injections BASE plus fixed label specs SPECS0. Prints inv, order, fq deltas vs base."""
import json, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lab, table, search
base = [tuple(x) for x in json.load(open(sys.argv[1]))]; tag = sys.argv[2]; s0 = sys.argv[3:]
orig = search.make
def meas(specs, t):
    src = lab.make(base, specs)
    p = os.path.join(table.D, 'v_%s.c' % t); open(p, 'w', newline='\n').write(src)
    sd = os.path.join(table.D, 'slot_%s' % t)
    import subprocess
    r = subprocess.run([sys.executable, os.path.join(table.ROOT, 'tools/wip/mc/s19/mkslot.py'), p, sd], capture_output=True, text=True)
    if r.returncode: return None
    r = subprocess.run([sys.executable, os.path.join(table.ROOT, 'tools/wip/mc/s18/analyze.py'), sd], capture_output=True, text=True)
    try:
        import ast
        l = r.stdout.strip().splitlines(); o = [int(x) for x in l[2].split()[1:]]
        miss = [b for b in table.NEED if b not in o]
        return {'fq': ast.literal_eval(l[0])['fq'], 'inv': int(l[1].split()[1]) + 5 * len(miss), 'order': l[2], 'miss': miss}
    except Exception: return None
b = meas(s0, tag + '_b'); print('base', b['inv'], b['order'], flush=True)
jobs = [s0 + ['%s:%s' % (k, h)] for k in lab.PAT for h in ('hot', 'cold')]
def one(sp): return sp, meas(sp, tag + '_' + sp[-1].replace(':', '_'))
with ThreadPoolExecutor(8) as ex:
    for sp, r in ex.map(one, jobs):
        if r is None: print(sp[-1], 'fail'); continue
        d = {k: r['fq'].get(k, 0) - b['fq'].get(k, 0) for k in set(r['fq']) | set(b['fq'])}
        print(sp[-1], r['inv'], {k: v for k, v in sorted(d.items(), key=str) if v}, r['miss'], flush=True)
