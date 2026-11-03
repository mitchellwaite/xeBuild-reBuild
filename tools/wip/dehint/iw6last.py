"""Attempt 6: python tools/wip/dehint/iw6last.py <dumpdir> <fn> <pass number N> <version...>: for each version, the last pass < N whose body names it
(and the line), or `never`.  Shows which pass released the names that pass N pops."""
import glob, re, sys
d, fn, N = sys.argv[1], sys.argv[2], int(sys.argv[3])
vers = sys.argv[4:]
fs = sorted(glob.glob(d + '/a.c.*t.*'), key=lambda f: int(re.search(r'\.(\d+)t\.', f).group(1)))
bodies = []
for f in fs:
    n = int(re.search(r'\.(\d+)t\.', f).group(1))
    if n >= N:
        continue
    t = open(f, errors='replace').read()
    m = re.search(r'^;; Function %s \(.*?(?=^;; Function |\Z)' % re.escape(fn), t, re.S | re.M)
    if not m:
        continue
    b = m.group(0)
    k = b.find('\n{\n')
    bodies.append((n, f.split('.')[-1], b[k:] if k >= 0 else b))
for v in vers:
    r = re.compile(r'_%s\b' % v)
    out = 'never'
    for n, name, b in reversed(bodies):
        ls = [l.strip()[:60] for l in b.split('\n') if r.search(l)]
        if ls:
            out = '%d %s: %s' % (n, name, ls[0])
            break
    print(v, out)
