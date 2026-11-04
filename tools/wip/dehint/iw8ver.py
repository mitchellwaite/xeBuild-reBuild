"""python tools/wip/dehint/iw8ver.py <dumpdir> <asm name, e.g. imgAdd.constprop.1> <first pass number> <version...>
Dumps from `IWNP=1 iwdump.py <file> <dir> writeFsTable -fdump-tree-all`.  Per pass, who owns an SSA version in that function (clones by asm name, which iw6ver can't address);
prints when the owner changes.  Also, with -n, the versions that are new in each pass (in order of first appearance)."""
import glob, re, sys
d, fn, first = sys.argv[1], sys.argv[2], int(sys.argv[3])
new = '-n' in sys.argv
vers = [v for v in sys.argv[4:] if v != '-n']
fs = sorted(glob.glob(d + '/a.c.*t.*'), key=lambda f: int(re.search(r'\.(\d+)t\.', f).group(1)))
last = {}
prev = set()
for f in fs:
    n = int(re.search(r'\.(\d+)t\.', f).group(1))
    if n < first:
        continue
    t = open(f, errors='replace').read()
    m = re.search(r'^;; Function \S+ \(%s, .*?(?=^;; Function |\Z)' % re.escape(fn), t, re.S | re.M)
    if not m:
        continue
    b = m.group(0)
    cur = {}
    for l in b.split('\n'):
        for mm in re.finditer(r'([A-Za-z_][\w.]*)?_(\d+)\b', l):
            cur.setdefault(mm.group(2), []).append(l.strip())
    for v in vers:
        o = cur.get(v, [None])[0]
        if o != last.get(v, '?'):
            print(f.rsplit('.', 1)[1], n, '_%s:' % v, o)
            last[v] = o
    if new:
        now = set(cur)
        print(f.rsplit('.', 1)[1], n, 'new', sorted(now - prev, key=int)[:40], 'gone', sorted(prev - now, key=int)[:40])
        prev = now
