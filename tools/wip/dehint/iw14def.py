"""python tools/wip/dehint/iw14def.py <dumpdir> <n> [n...] [-f fn] : for SSA version n, its defining statement per tree pass (only when it
changes) in fn (default writeFsTable). <dumpdir> is a dump dir made by iw14names.py (build/iw/a14/nm_<name>)."""
import glob, re, sys
a = sys.argv[1:]
fn = 'writeFsTable'
if '-f' in a:
    i = a.index('-f'); fn = a[i + 1]; del a[i:i + 2]
d = a[0]
names = [int(x) for x in a[1:]]
fs = sorted(glob.glob(d + '/a.c.*t.*'), key=lambda f: int(re.search(r'\.(\d+)t\.', f).group(1)))
bodies = []
for f in fs:
    t = open(f, errors='replace').read()
    m = re.search(r'^;; Function %s \(.*?(?=^;; Function |\Z)' % re.escape(fn), t, re.S | re.M)
    if not m:
        continue
    s = m.group(0)
    k = s.find('\n{')
    if k >= 0:
        bodies.append((re.search(r'\.\d+t\.(.*)$', f).group(1), s[k:].split('\n')))
for n in names:
    rx = re.compile(r'^\s*(?:# )?(?:[A-Za-z_][\w.]*)?_%d(?:\(D\))? *=' % n)
    out = []
    last = None
    for p, ls in bodies:
        h = next((l.strip() for l in ls if rx.search(l)), None)
        if h != last:
            out.append('%s: %s' % (p, (h or '(none)')[:70]))
            last = h
    print(n, '|', ' || '.join(out))
