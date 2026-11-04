"""flxphi.py <tag>: per pass, PHI group (noCrc, len only) at the block holding '[len] + pos' after the
'file in [flashfs]' path... simply: every block with both a noCrc and a len PHI, in order, flashfs part."""
import glob, os, re, sys
import fllib as L
tag = sys.argv[1]
d = os.path.join(L.BD, 'dump', tag)
fs = glob.glob(os.path.join(d, '-.*t.*'))
fs.sort(key=lambda f: int(re.search(r'\.(\d+)t\.', f).group(1)))
prev = None
lo = int(sys.argv[2]) if len(sys.argv) > 2 else 0
for f in fs:
    n = os.path.basename(f)[2:]
    if int(re.match(r'\d+', n).group()) < lo:
        continue
    t = open(f, errors='replace').read()
    parts = [q for q in re.split(r'(?m)^(?=;; Function )', t) if q.startswith(';; Function parseIni ')]
    if not parts:
        continue
    q = parts[0]
    a = q.find('label [flashfs] found')
    b = q.find('label [security] found')
    if a < 0 or b < 0:
        continue
    q = q[a:b] if b > a else q[a:]
    out = []
    for bb in re.split(r'(?m)^  <bb \d+>:', q):
        ph = re.findall(r'(?m)^  # ((?:noCrc|len)_\d+) = PHI', bb)
        vs = [x.split('_')[0] for x in ph]
        if 'noCrc' in vs and 'len' in vs:
            out.append(''.join('N' if v == 'noCrc' else 'L' for v in vs))
    s = ' '.join(out)
    if s != prev:
        print(n, s)
        prev = s
