"""fl4n.py <tag> <name...>: per pass, the defining line of each SSA name in parseIni, printed when it changes.
Shows who owned a recycled number and when it was freed."""
import glob, os, re, sys
import fllib as L
tag = sys.argv[1]
fs = glob.glob(os.path.join(L.BD, 'dump', tag, '-.*t.*'))
fs.sort(key=lambda f: int(re.search(r'\.(\d+)t\.', f).group(1)))
for name in sys.argv[2:]:
    print('---', name)
    prev = None
    for f in fs:
        n = os.path.basename(f)[2:]
        t = open(f, errors='replace').read()
        parts = [q for q in re.split(r'(?m)^(?=;; Function )', t) if q.startswith(';; Function parseIni ')]
        if not parts:
            continue
        v = name.split('_')[-1]
        m = re.search(r'(?m)^\s*(?:# )?(\w*_%s(?:\(D\))? = .*)$' % v, parts[0])
        s = m.group(1)[:90] if m else None
        if s != prev:
            print('  ', n, s)
            prev = s
