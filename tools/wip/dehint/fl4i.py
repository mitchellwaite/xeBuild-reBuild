"""fl4i.py <tag> : per pass from ch2 on, [security]'s comma>nul compare and PHIs below it.  Finds the block by `> 21` after it."""
import glob, os, re, sys
import fllib as L
tag = sys.argv[1]
fs = glob.glob(os.path.join(L.BD, 'dump', tag, '-.*t.*'))
fs.sort(key=lambda f: int(re.search(r'\.(\d+)t\.', f).group(1)))
prev = None
for f in fs:
    n = os.path.basename(f)[2:]
    t = open(f, errors='replace').read()
    parts = [q for q in re.split(r'(?m)^(?=;; Function )', t) if q.startswith(';; Function parseIni ')]
    if not parts:
        continue
    q = parts[0]
    k = q.find(' > 21)')
    if k < 0:
        continue
    seg = q[max(0, k - 1400):k + 6]
    ls = [l.strip() for l in seg.splitlines() if re.search(r'^\s*(# \S+ = PHI|if \(|\w+ = \w+;$)', l) and 'VUSE' not in l and '.MEM' not in l]
    s = ' ; '.join(ls[-9:])
    if s != prev:
        print(n, s)
        prev = s
