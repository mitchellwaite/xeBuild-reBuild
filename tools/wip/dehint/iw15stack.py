"""python tools/wip/dehint/iw15stack.py <dumpdir> [fn] [firstpass] [lastpass]: per tree pass, SSA versions of fn that appear and go, .MEM
virtual operands included (marked m). The dump dir must come from -fdump-tree-all-vops (build/iw/a15/dump.py). New names are listed in
first-occurrence order in the dump, which is not creation order; gone names are sorted. For reading the free list across passes."""
import glob, re, sys
d = sys.argv[1]
fn = sys.argv[2] if len(sys.argv) > 2 else 'writeFsTable'
first = sys.argv[3] if len(sys.argv) > 3 else None
last = sys.argv[4] if len(sys.argv) > 4 else None
fs = sorted(glob.glob(d + '/a.c.*t.*'), key=lambda f: int(re.search(r'\.(\d+)t\.', f).group(1)))
rx = re.compile(r'(?<![\w])((?:\.MEM|[A-Za-z_][\w.]*)?_(\d+))(?:\(D\))?\b')
prev = None
on = first is None
for f in fs:
    p = re.search(r'\.\d+t\.(.*)$', f).group(1)
    t = open(f, errors='replace').read()
    m = re.search(r'^;; Function %s \(.*?(?=^;; Function |\Z)' % re.escape(fn), t, re.S | re.M)
    if not m:
        continue
    body = m.group(0)
    k = body.find('\n{')
    if k < 0:
        continue
    seen = {}
    for x in rx.finditer(body[k:]):
        n = int(x.group(2))
        if n not in seen:
            seen[n] = x.group(1)
    if first and p == first:
        on = True
    if prev is not None and on:
        new = [n for n in seen if n not in prev]
        gone = sorted(n for n in prev if n not in seen)
        def tag(tbl, n):
            return ('m%d' % n) if tbl[n].startswith('.MEM') else str(n)
        if new or gone:
            print('%-14s new %3d: %s' % (p, len(new), ' '.join(tag(seen, n) for n in new)))
            print('%-14s gone %2d: %s' % ('', len(gone), ' '.join(tag(prev, n) for n in gone)))
    prev = seen
    if last and p == last:
        break
