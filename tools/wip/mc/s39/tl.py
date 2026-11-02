"""tl.py START.json PREFIX ITERS TARGET : tracking loop (table -> track x2 -> best) ; logs to tl_PREFIX.log"""
import sys, os, json, subprocess
os.environ['DUP'] = '1'; os.environ['LU'] = '1'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gs2, ev
cur = sys.argv[1]; P = sys.argv[2]; TG = sys.argv[4]; log = open('tl_%s.log' % P, 'a')
for k in range(int(sys.argv[3])):
    nm = '%s%d' % (P, k); st = json.load(open(cur)); json.dump(st, open('st_%s.json' % nm, 'w'))
    r = ev.ev(gs2.build(st), nm, True); print(nm, 'inv', r['score'], r['fncmp'], ' '.join(map(str, r['o'][12:])), file=log, flush=True)
    subprocess.run([sys.executable, 'tab3.py', 'st_%s.json' % nm, nm, 'tab_%s.jsonl' % nm], env=dict(os.environ, XT='1'))
    ps = [subprocess.Popen([sys.executable, 'track.py', 'tab_%s.jsonl' % nm, nm, 'st_%s.json' % nm, TG, str(s), '20000', 'tr_%s_%d.json' % (nm, s)],
                           stdout=open('tr_%s_%d.log' % (nm, s), 'w'), stderr=subprocess.STDOUT) for s in (1, 2)]
    for p in ps: p.wait()
    best = None
    for s in (1, 2):
        for l in open('tr_%s_%d.log' % (nm, s)):
            if l.startswith('BEST'):
                v = eval(l[5:]); print('  seed', s, v, file=log, flush=True)
                if best is None or v < best[0]: best = (v, 'tr_%s_%d.json' % (nm, s))
    if not best: break
    cur = best[1]
