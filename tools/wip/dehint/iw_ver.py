"""python tools/wip/dehint/iw_ver.py <dumpdir> <asm name e.g. imgAdd.constprop.2 or writeFsTable> <version> [<version>...]

Dumps from iwdump.py with -fdump-tree-all (the a.c.* files).  For each pass prints which statement defines each SSA version
in that function, only when it changes: shows who owned a recycled name before."""
import glob, os, re, sys

d, fn = sys.argv[1:3]
vers = sys.argv[3:]
files = sorted(glob.glob(os.path.join(d, 'a.c.*')), key=lambda f: (int(re.search(r'\.(\d+)[tir]\.', f).group(1)) if re.search(r'\.(\d+)[tir]\.', f) else -1))
last = {}
for f in files:
    m = re.search(r'\.(\d+)t\.(.*)$', f)
    if not m:
        continue
    t = open(f, errors='replace').read()
    b = re.search(r'^;; Function [^\n]*\(%s, .*?(?=^;; Function |\Z)' % re.escape(fn), t, re.S | re.M)
    if not b:
        continue
    s = b.group(0)
    for v in vers:
        rx = re.compile(r'^\s*(#\s*)?(\w[\w.]*?)?_%s(\(D\))?\s*(=|=\s*PHI).*$' % v, re.M)
        k = rx.search(s)
        line = k.group(0).strip() if k else '-'
        if last.get(v) != line:
            print('%-16s _%s: %s' % (m.group(2), v, line[:90]))
            last[v] = line
