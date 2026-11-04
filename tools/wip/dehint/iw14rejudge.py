"""python tools/wip/dehint/iw14rejudge.py <base.c> <out.log> [cap] [first] [last]: every older generator gen_iwN.py rerun on a new base by total lines. Options whose edits don't apply
to the base are dropped axis by axis, the rest is crossed (random sample of cap, default 200), repeats across generators are skipped. Lines: total label gen; IDENTICAL lines start with `0`."""
import hashlib, importlib.util, itertools, os, random, re, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib
os.environ.setdefault('IWB', sys.argv[1])
base = open(sys.argv[1], newline='').read().replace('\r\n', '\n')
log = open(sys.argv[2], 'a', newline='\n')
cap = int(sys.argv[3]) if len(sys.argv) > 3 else 200
first = int(sys.argv[4]) if len(sys.argv) > 4 else 1
last = int(sys.argv[5]) if len(sys.argv) > 5 else 213
here = os.path.dirname(os.path.abspath(__file__))
seen = set()
random.seed(14)
ex = ThreadPoolExecutor(4)
best = 1e9
def run(a):
    n, lab, t = a
    r = iwlib.score_text(t, [])
    return n, lab, t, r
for n in range(last, first - 1, -1):
    p = os.path.join(here, 'gen_iw%d.py' % n)
    if not os.path.exists(p):
        continue
    try:
        s = importlib.util.spec_from_file_location('g', p)
        m = importlib.util.module_from_spec(s)
        s.loader.exec_module(m)
        axes = m.AXES
    except Exception as e:
        log.write('skip %d %s\n' % (n, str(e)[:80])); log.flush()
        continue
    keep = []
    for ax in axes:
        try:
            k = [o for o in ax if all(a in base for a, b in o[1])]
        except Exception:
            k = []
        if len(k) > 1:
            keep.append(k)
    if not keep:
        log.write('gen %d: nothing applies\n' % n); log.flush()
        continue
    total = 1
    for k in keep:
        total *= len(k)
    combos = []
    if total <= cap:
        combos = list(itertools.product(*keep))
    else:
        for _ in range(cap):
            combos.append(tuple(random.choice(k) for k in keep))
    jobs = []
    for c in combos:
        t = base
        for lab, ed in c:
            for a, b in ed:
                t = t.replace(a, b)
        h = hashlib.md5(t.encode()).hexdigest()
        if h in seen:
            continue
        seen.add(h)
        jobs.append((n, '+'.join(x[0] for x in c if x[0]), t))
    res = list(ex.map(run, jobs))
    res = [r for r in res if 'compile' not in r[3]]
    res.sort(key=lambda r: r[3]['total'])
    log.write('gen %d: %d of %d run, best %s\n' % (n, len(jobs), total, res[0][3]['total'] if res else '-'))
    for r in res:
        if r[3]['total'] and r[3]['per'].get('_writeFsTable', 0) == 0 and r[3]['total'] < 400:
            log.write('WF0 %d %s gen%d %s\n' % (r[3]['total'], r[1], r[0], iwlib.fmt(r[3])[:160]))
            open(os.path.join(iwlib.BUILD, 'a14', 'wf0_%d_%s.c' % (r[0], hashlib.md5(r[2].encode()).hexdigest()[:8])), 'w', newline='\n').write(r[2])
    for r in res[:6]:
        if r[3]['total'] <= 6:
            log.write('%d %s gen%d %s\n' % (r[3]['total'], r[1], r[0], iwlib.fmt(r[3])[:120]))
        if r[3]['total'] == 0 or (r[3]['total'] <= 2 and r[3]['per'].get('_writeFsTable', 0) == 0):
            out = os.path.join(iwlib.BUILD, 'a14', 'hit_%d_%s.c' % (r[0], hashlib.md5(r[2].encode()).hexdigest()[:8]))
            open(out, 'w', newline='\n').write(r[2])
            log.write('HIT %s\n' % out)
    log.flush()
log.write('done\n'); log.close()
