"""python tools/wip/dehint/iw15src.py <dumpdir> [fn] : for every name ivopts introduces in fn, in iw14pop's order (cand number; PHI, increment, init, bound),
the last pass it was live in (.MEM included) and what it held there. Dump dir from -fdump-tree-all-vops (build/iw/a15/dump.py)."""
import glob, re, sys
d = sys.argv[1]
fn = sys.argv[2] if len(sys.argv) > 2 else 'writeFsTable'
fs = sorted(glob.glob(d + '/a.c.*t.*'), key=lambda f: int(re.search(r'\.(\d+)t\.', f).group(1)))
bodies = []
for f in fs:
    p = re.search(r'\.\d+t\.(.*)$', f).group(1)
    t = open(f, errors='replace').read()
    m = re.search(r'^;; Function %s \(.*?(?=^;; Function |\Z)' % re.escape(fn), t, re.S | re.M)
    if not m:
        continue
    k = m.group(0).find('\n{')
    if k < 0:
        continue
    bodies.append((p, m.group(0)[k:].split('\n')))
    if p == 'ivopts':
        break
iv = bodies[-1][1]
prevp = [b for b in bodies if b[0] == 'cunroll'][-1]
cands = {}
rows = []
for l in iv:
    m = re.match(r'\s*# (ivtmp\.(\d+))_(\d+) = PHI', l)
    if m:
        cands.setdefault(int(m.group(2)), {})['vb'] = int(m.group(3))
    m = re.match(r'\s*(ivtmp\.(\d+))_(\d+) = (.*);', l)
    if m:
        c = cands.setdefault(int(m.group(2)), {})
        c['va' if ('ivtmp.%s_' % m.group(2)) in m.group(4) else 'in'] = int(m.group(3))
    m = re.match(r'\s*_(\d+) = (ivtmp\.\d+)_\d+ \+ \d+;', l)
    if m:
        rows.append((m.group(2), int(m.group(1))))
def hist(n):
    rxs = re.compile(r'(?<![\w])(?:\.MEM|[A-Za-z_][\w.]*)?_%d(?:\(D\))?\b' % n)
    rxd = re.compile(r'^\s*(?:# )?(?:\.MEM|[A-Za-z_][\w.]*)?_%d(?:\(D\))? *=' % n)
    lp = None; ld = None
    stmt = None
    for p, ls in bodies[:-1]:
        for i, l in enumerate(ls):
            if rxs.search(l):
                lp = p
            if rxd.search(l):
                ld = l.strip()
                # a VDEF line: the store is the next line
                if 'VDEF' in ld and i + 1 < len(ls):
                    ld += ' // ' + ls[i + 1].strip()
    return '%-12s %s' % (lp or '-', (ld or '(never defined)')[:90])
pos = 0
for c in sorted(cands):
    for k in ('vb', 'va', 'in'):
        if k in cands[c]:
            pos += 1
            print('%2d ivtmp.%d %-3s %4d  %s' % (pos, c, k, cands[c][k], hist(cands[c][k])))
    for r in rows:
        if r[0] == 'ivtmp.%d' % c:
            pos += 1
            print('%2d ivtmp.%d end %4d  %s' % (pos, c, r[1], hist(r[1])))
