"""python tools/wip/dehint/iw14gap.py <dumpdir> [fn]: SSA versions of fn that are in no dump before ivopts ('phantoms'), and where each shows up after."""
import glob, re, sys
d = sys.argv[1]; fn = sys.argv[2] if len(sys.argv) > 2 else 'writeFsTable'
fs = sorted(glob.glob(d + '/a.c.*t.*'), key=lambda f: int(re.search(r'\.(\d+)t\.', f).group(1)))
seen = {}; order = []
for f in fs:
    t = open(f, errors='replace').read()
    m = re.search(r'^;; Function %s \(.*?(?=^;; Function |\Z)' % re.escape(fn), t, re.S | re.M)
    if not m: continue
    s = m.group(0); k = s.find('\n{')
    if k < 0: continue
    p = re.search(r'\.\d+t\.(.*)$', f).group(1); order.append(p)
    for x in re.finditer(r'(?<![\w.])(?:[A-Za-z_][\w.]*)?_(\d+)(?:\(D\))?\b', s[k:]):
        seen.setdefault(int(x.group(1)), p)
top = max(seen)
print('max', top, 'gaps', [n for n in range(1, top) if n not in seen])
hi = [n for n, p in seen.items() if order.index(p) > order.index('fixup_cfg4')]
print('first seen after fixup_cfg4:', sorted((n, seen[n]) for n in hi))
