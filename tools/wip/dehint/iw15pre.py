"""python tools/wip/dehint/iw15pre.py <dumpdir> <fn>: what PRE inserts in fn, from a -fdump-tree-pre-details dump (iw15dump.py): `Found partial`, `Inserted`, `Created phi`, in order, with value ids.
Expressions are handled in value-id order; compare the ids of two expressions to see which gets its name first."""
import glob, re, sys
d, fn = sys.argv[1], sys.argv[2]
f = glob.glob(d + '/a.c.*t.pre')[0]
t = open(f, errors='replace').read()
m = re.search(r'^;; Function %s \(.*?(?=^;; Function |\Z)' % re.escape(fn), t, re.S | re.M).group(0)
for l in m[:m.find('\n{')].split('\n'):
    if re.search(r'^(Inserted|Created phi|Starting insert|Found partial)', l):
        print(l[:120])
