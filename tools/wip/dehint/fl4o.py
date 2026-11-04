"""fl4o.py <tag> [pass]: names new at a pass (default dom3) in parseIni, in dump order; and names defined in the previous dump
that are gone (candidates for the free list).  Bare numbers only, to compare stacks."""
import glob, os, re, sys
import fllib as L
tag = sys.argv[1]
pas = sys.argv[2] if len(sys.argv) > 2 else 'dom3'
fs = glob.glob(os.path.join(L.BD, 'dump', tag, '-.*t.*'))
fs.sort(key=lambda f: int(re.search(r'\.(\d+)t\.', f).group(1)))
seq = []
for f in fs:
    n = os.path.basename(f)[2:]
    t = open(f, errors='replace').read()
    parts = [q for q in re.split(r'(?m)^(?=;; Function )', t) if q.startswith(';; Function parseIni ')]
    if parts:
        seq.append((n, parts[0]))


def defs(q):
    return [int(m) for m in re.findall(r'(?m)^\s*(?:# )?[\w.]*_(\d+)(?:\(D\))? = ', q)]


for i, (n, q) in enumerate(seq):
    if n.endswith('.' + pas):
        a = set(defs(seq[i - 1][1]))
        b = defs(q)
        new = [x for x in b if x not in a]
        print(seq[i - 1][0], '->', n)
        print('new', len(new), new)
        gone = sorted(a - set(b))
        print('gone', len(gone), gone[:80])
