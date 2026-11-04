"""flxph2.py <tag>: per pass, the noCrc and len PHIs above [flashfs]'s `if (noCrc == 0)` (block that holds the test)."""
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
    out = []
    for bb in re.split(r'(?m)^  <bb \d+>:', q):
        m = re.search(r'if \((noCrc_\d+|noCrc\.\d+_\d+) (==|!=) 0\)', bb)
        if m:
            ph = re.findall(r'(?m)^  # ((?:noCrc|len)_\d+) = PHI <([^>]*)>', bb)
            pos = re.search(r'firmwareCrc|flashCrc|files', bb)
            out.append(' '.join(a for a, b in ph))
    s = ' | '.join(out)
    if s != prev:
        print(n, s)
        prev = s
