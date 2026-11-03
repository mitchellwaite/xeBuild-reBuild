"""Attempt 6: python tools/wip/dehint/iw6ver.py <dumpdir> <fn> <first pass number> <version...>: per pass from that dump number on, what the SSA version
is in <fn> (first line naming it), printing only when that changes.  Also the highest version in the body per pass with -m."""
import glob, re, sys
d, fn, first = sys.argv[1], sys.argv[2], int(sys.argv[3])
vers = [v for v in sys.argv[4:] if v != '-m']
fs = sorted(glob.glob(d + '/a.c.*t.*'), key=lambda f: int(re.search(r'\.(\d+)t\.', f).group(1)))
last = {}
for f in fs:
    n = int(re.search(r'\.(\d+)t\.', f).group(1))
    if n < first:
        continue
    t = open(f, errors='replace').read()
    m = re.search(r'^;; Function %s \(.*?(?=^;; Function |\Z)' % re.escape(fn), t, re.S | re.M)
    if not m:
        continue
    b = m.group(0)
    k = b.find('\n{\n')
    b = b[k:] if k >= 0 else b
    if '-m' in sys.argv:
        print(n, f.split('.')[-1], 'max', max([int(x) for x in re.findall(r'_(\d+)\b', b)] or [0]))
    for v in vers:
        ls = [l.strip()[:90] for l in b.split('\n') if re.search(r'_%s\b' % v, l) and '=' in l]
        s = ls[0] if ls else None
        if last.get(v, 0) != s:
            print(n, f.split('.')[-1], v, s)
            last[v] = s
