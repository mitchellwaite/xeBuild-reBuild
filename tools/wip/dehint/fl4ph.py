"""fl4ph.py <tag> <regex>: per dump, parseIni lines matching regex (only printed when changed)."""
import glob, os, re, sys
import fllib as L
tag, rx = sys.argv[1:3]
fs = glob.glob(os.path.join(L.BD, 'dump', tag, '-.*t.*'))
fs.sort(key=lambda f: int(re.search(r'\.(\d+)t\.', f).group(1)))
prev = None
for f in fs:
    n = os.path.basename(f)[2:]
    t = open(f, errors='replace').read()
    parts = [q for q in re.split(r'(?m)^(?=;; Function )', t) if q.startswith(';; Function parseIni ')]
    if not parts:
        continue
    out = re.findall(rx, parts[0], re.M)
    s = ' | '.join(str(x) for x in out)
    if s != prev:
        print(n, s[:400])
        prev = s
