"""Attempt 70: per pass, which buildFlash SSA versions disappear (released) and appear (made, maybe
recycled), from a70_dump.sh's -fdump-tree-all output.
python tools/wip/dehint/bdgen/a70_names.py <dumpdir> [fn] [first pass no] [last pass no]"""
import glob, os, re, sys

def body(p, fn):
    t = open(p, errors='replace').read()
    i = t.find(';; Function %s ' % fn)
    if i < 0:
        return None
    j = t.find('\n;; Function ', i + 10)
    return t[i:j if j > 0 else len(t)]

def names(b):
    # SSA names: identifier_version or _version, ignore declarations-only lines
    s = {}
    for m in re.finditer(r'(?<![\w.])((?:[A-Za-z_.][\w.]*?)?_(\d+))(?:\(D\))?\b', b):
        v = int(m.group(2)); s.setdefault(v, m.group(1))
    return s

def main():
    d = sys.argv[1]; fn = sys.argv[2] if len(sys.argv) > 2 else 'buildFlash'
    lo = int(sys.argv[3]) if len(sys.argv) > 3 else 82; hi = int(sys.argv[4]) if len(sys.argv) > 4 else 107
    ps = sorted(glob.glob(os.path.join(d, 'in.c.*t.*')), key=lambda p: int(re.search(r'\.(\d+)t\.', p).group(1)))
    prev = None
    for p in ps:
        n = int(re.search(r'\.(\d+)t\.', p).group(1))
        b = body(p, fn)
        if b is None:
            continue
        cur = names(b)
        if prev is not None and lo <= n <= hi:
            gone = sorted(set(prev) - set(cur)); new = sorted(set(cur) - set(prev))
            ren = sorted(v for v in set(prev) & set(cur) if prev[v] != cur[v])
            print('%s  -%d +%d  max %d' % (os.path.basename(p).split('.', 2)[2], len(gone), len(new), max(cur)))
            print('   gone:', ' '.join('%s' % prev[v] for v in gone))
            print('   new: ', ' '.join('%s' % cur[v] for v in new))
            if ren: print('   reused:', ' '.join('%s>%s' % (prev[v], cur[v]) for v in ren))
        prev = cur

main()
