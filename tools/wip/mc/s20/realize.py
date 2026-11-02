"""realize.py DESIGN.json STEPS [start.json] [WSET]: greedy dead-edge injections (s19 make()) toward a
design f vector (fanneal output): objective L1(measured fq - design) + 3*inv, measured by mkslot+analyze."""
import ast, json, os, subprocess, sys
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
sys.path.insert(0, os.path.join(ROOT, 'tools', 'wip', 'mc', 's19'))
import search
D = os.path.join(ROOT, 'build', 'v', 'mc20')
design = {int(k): v for k, v in json.load(open(sys.argv[1])).items()}
steps = int(sys.argv[2])
cur = [tuple(x) for x in json.load(open(sys.argv[3]))] if len(sys.argv) > 3 and sys.argv[3] != '-' else []
WSET = sys.argv[4].split(',') if len(sys.argv) > 4 else ['b', 'p', 'pp', 'ppp']
PY = sys.executable
def meas(inj, tag='r'):
    p = os.path.join(D, 'v_%s.c' % tag); sd = os.path.join(D, 'slot_%s' % tag)
    open(p, 'w', newline='\n').write(search.make(inj))
    r = subprocess.run([PY, os.path.join(ROOT, 'tools/wip/mc/s19/mkslot.py'), p, sd], capture_output=True, text=True)
    if r.returncode: return None
    r = subprocess.run([PY, os.path.join(ROOT, 'tools/wip/mc/s18/analyze.py'), sd], capture_output=True, text=True)
    try:
        lines = r.stdout.strip().splitlines()
        d = ast.literal_eval(lines[0]); inv = int(lines[1].split()[1]); order = lines[2]
    except Exception:
        return None
    fq = d['fq']
    dist = sum(abs(fq.get(b, 0) - v) for b, v in design.items())
    return dist + 3 * inv, dist, inv, order, fq
r = meas(cur); best = r[0]
print('start', cur, r[:4], flush=True)
for st in range(steps):
    cand = None
    for t in range(len(search.TGT)):
        for s in search.SRCS:
            if not search.ok(t, s): continue
            for w in WSET:
                rr = meas(cur + [(t, s, w)])
                if rr and (cand is None or rr[0] < cand[0][0]): cand = (rr, cur + [(t, s, w)])
    if cand is None or cand[0][0] >= best:
        print('no improvement', flush=True); break
    (best, dist, inv, order, fq), cur = cand
    print('step', st, cur[-1], 'obj', best, 'dist', dist, 'inv', inv, flush=True)
    print('   ', order, flush=True)
    print('   ', json.dumps(fq), flush=True)
    json.dump(cur, open(os.path.join(ROOT, 'tools/wip/mc/s20/best.json'), 'w'))
