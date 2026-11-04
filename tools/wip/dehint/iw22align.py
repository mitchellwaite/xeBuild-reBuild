"""python tools/wip/dehint/iw22align.py <dumpdir> [fn] [size]: from -fdump-tree-all-alias dumps (a.c.*), per tree pass the size-byte memcpy dests in fn with the ALIGN of
their definition, PHIs included (iw18align's regex misses PHI defs, which print as `# name = PHI`). A pass is printed when the line changes."""
import glob, re, sys
d = sys.argv[1]; fn = sys.argv[2] if len(sys.argv) > 2 else 'finalizeImage'; size = sys.argv[3] if len(sys.argv) > 3 else '512'
fs = sorted(glob.glob(d + '/a.c.*t.*'), key=lambda f: int(re.search(r'\.(\d+)t\.', f).group(1)))
prev = None
for f in fs:
    t = open(f, errors='replace').read()
    m = re.search(r'^;; Function %s \(.*?(?=^;; Function |\Z)' % fn, t, re.S | re.M)
    if not m: continue
    b = m.group(0)
    out = []
    for x in re.findall(r'memcpy \((\w+), [^,]+, %s\)' % size, b):
        # lines just before the def: `# ALIGN`, `# PT`, then `[# ]name = ...`
        k = re.search(r'((?:^[ \t]*# (?:PT|ALIGN|USE|CLB)[^\n]*\n)*)^[ \t]*(?:# )?%s = ([^\n]*)' % re.escape(x), b, re.M)
        al = re.search(r'ALIGN = (\d+)', k.group(1)) if k else None
        out.append('%s align=%s %s' % (x, al.group(1) if al else '-', k.group(2)[:48] if k else '?'))
    s = ' | '.join(out)
    if s != prev:
        print(re.search(r'\.\d+t\.(.*)$', f).group(1), s)
    prev = s
