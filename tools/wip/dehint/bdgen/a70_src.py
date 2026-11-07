"""Attempt 70: for the versions ch2 (or another pass) reuses in buildFlash, which earlier pass released each.
python tools/wip/dehint/bdgen/a70_src.py <dumpdir> [pass no, default 107] [fn]"""
import glob, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
d = sys.argv[1]; target = int(sys.argv[2]) if len(sys.argv) > 2 else 107
fn = sys.argv[3] if len(sys.argv) > 3 else 'buildFlash'
def body(p):
    t = open(p, errors='replace').read(); i = t.find(';; Function %s ' % fn)
    if i < 0: return None
    j = t.find('\n;; Function ', i + 10); return t[i:j if j > 0 else len(t)]
def names(b):
    s = {}
    for m in re.finditer(r'(?<![\w.])((?:[A-Za-z_.][\w.]*?)?_(\d+))(?:\(D\))?\b', b):
        s.setdefault(int(m.group(2)), m.group(1))
    return s
ps = sorted(glob.glob(os.path.join(d, 'in.c.*t.*')), key=lambda p: int(re.search(r'\.(\d+)t\.', p).group(1)))
prev = None; rel = {}
for p in ps:
    n = int(re.search(r'\.(\d+)t\.', p).group(1)); b = body(p)
    if b is None: continue
    cur = names(b)
    if prev is not None and n >= 82:
        if n == target:
            for v in sorted(set(cur) - set(prev)):
                print('%5d %-14s <- %s' % (v, cur[v], rel.get(v, '?')))
            break
        for v in set(prev) - set(cur):
            rel[v] = '%s %s' % (os.path.basename(p).split('.')[2], prev[v])
    prev = cur
