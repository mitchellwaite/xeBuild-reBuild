"""python tools/wip/dehint/iw_names.py <dumpdir> <func> [name ...]

Dumps made by iwdump.py with -fdump-tree-all: walk the tree passes in order (from the
a.c.NNNt.* file numbers) and print, per pass, the SSA versions that appear or vanish in the
function body (the body only: declarations skipped).  With names, print only the passes where
those versions (e.g. 273 366) appear or vanish.  Shows the recycling order of SSA names."""
import glob, os, re, sys

d, fn = sys.argv[1:3]
want = set(sys.argv[3:])
files = sorted(glob.glob(os.path.join(d, 'a.c.*t.*')), key=lambda f: int(re.search(r'\.(\d+)t\.', f).group(1)))
prev = None
for f in files:
    t = open(f, errors='replace').read()
    m = re.search(r'^;; Function %s \(.*?(?=^;; Function |\Z)' % re.escape(fn), t, re.S | re.M)
    if not m:
        continue
    body = m.group(0)
    k = body.find('{\n')
    body = body[k:] if k >= 0 else body
    # drop declaration lines
    body = '\n'.join(l for l in body.split('\n') if not re.match(r'^  [a-zA-Z].*;$', l) or '=' in l or 'if' in l)
    seen = []
    for v in re.findall(r'\b[A-Za-z_][\w.]*_(\d+)(?:\(\w+\))?\b|\b_(\d+)\b', body):
        n = v[0] or v[1]
        if n not in seen:
            seen.append(n)
    cur = set(seen)
    name = re.search(r'\.\d+t\.(.*)$', f).group(1)
    if prev is not None:
        new = [n for n in seen if n not in prev]
        gone = sorted(prev - cur, key=int)
        if want:
            a = [n for n in new if n in want]
            b = [n for n in gone if n in want]
            if a or b:
                print(name, 'new', a, 'gone', b)
        elif new or gone:
            print('%s: new(%d) %s\n   gone(%d) %s' % (name, len(new), ' '.join(new), len(gone), ' '.join(gone)))
    prev = cur
