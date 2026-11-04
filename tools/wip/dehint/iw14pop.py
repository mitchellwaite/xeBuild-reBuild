"""python tools/wip/dehint/iw14pop.py <dumpdir> [fn]: every SSA name ivopts takes in fn, in cand order (ivtmp number; PHI result, increment, init, then bound), with the name's
last earlier definition, the pass that last had it, and whether a later pass re-used it. Reads where ivopts' free names came from."""
import glob, re, sys
d = sys.argv[1]; fn = sys.argv[2] if len(sys.argv) > 2 else 'writeFsTable'
fs = sorted(glob.glob(d + '/a.c.*t.*'), key=lambda f: int(re.search(r'\.(\d+)t\.', f).group(1)))
bodies = []
for f in fs:
    t = open(f, errors='replace').read()
    m = re.search(r'^;; Function %s \(.*?(?=^;; Function |\Z)' % re.escape(fn), t, re.S | re.M)
    if not m: continue
    s = m.group(0); k = s.find('\n{')
    if k >= 0:
        p = re.search(r'\.\d+t\.(.*)$', f).group(1)
        bodies.append((p, s[k:].split('\n')))
    if p == 'ivopts': break
iv = bodies[-1][1]
rows = []
cands = {}
for l in iv:
    m = re.match(r'\s*# (ivtmp\.(\d+))_(\d+) = PHI', l)
    if m: cands.setdefault(int(m.group(2)), {})['vb'] = int(m.group(3))
    m = re.match(r'\s*(ivtmp\.(\d+))_(\d+) = (.*);', l)
    if m:
        c = cands.setdefault(int(m.group(2)), {})
        c['va' if ('ivtmp.%s_' % m.group(2)) in m.group(4) else 'in'] = int(m.group(3))
    m = re.match(r'\s*_(\d+) = (ivtmp\.\d+_\d+) \+ 512;', l)
    if m: rows.append(('bound', int(m.group(1)), m.group(2)))
def hist(n):
    rx = re.compile(r'^\s*(?:# )?(?:[A-Za-z_][\w.]*)?_%d(?:\(D\))? *=' % n)
    last = None; lp = None
    for p, ls in bodies[:-1]:
        h = next((l.strip() for l in ls if rx.search(l)), None)
        if h: last, lp = h, p
    return '%-12s %s' % (lp or '-', (last or '(in no dump)')[:60])
for c in sorted(cands):
    for k in ('vb', 'va', 'in'):
        if k in cands[c]:
            print('ivtmp.%d %-3s %4d  %s' % (c, k, cands[c][k], hist(cands[c][k])))
    for r in rows:
        if r[2].startswith('ivtmp.%d_' % c):
            print('ivtmp.%d end %4d  %s' % (c, r[1], hist(r[1])))
