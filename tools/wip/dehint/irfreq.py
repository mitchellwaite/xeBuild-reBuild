"""python tools/wip/dehint/irfreq.py <dumpdir> <pattern> [-a] : for every tree dump in <dumpdir> (made with irdump.py
and -fdump-tree-all-blocks-details), one line per block whose statements match <pattern>:
pass, bb, freq, successor edges.  -a prints all blocks."""
import os, re, sys

d, pat = sys.argv[1:3]
allb = '-a' in sys.argv
for f in sorted(os.listdir(d)):
    if not re.match(r'\d+t\.', f):
        continue
    t = open(os.path.join(d, f), errors='replace').read()
    # only the final function dump (after the last blank-line delimited header)
    parts = re.split(r'(?m)^;;   basic block ', t)
    out = []
    seen = {}
    for p in parts[1:]:
        m = re.match(r'(\d+), loop depth (\d+), count \d+, freq (\d+)', p)
        if not m:
            continue
        body = p
        bb = int(m.group(1))
        succ = re.findall(r';;\s+(?:succ:)?\s+(\d+|EXIT)\s*(?:\[([\d.]+)%\])?\s*\(?([A-Z_,]*)', p[p.find('succ:'):]) if 'succ:' in p else []
        if allb or re.search(pat, body):
            s = ' '.join('%s[%s]' % (a, b or '-') for a, b, c in succ)
            seen[bb] = 'bb%d f=%s -> %s' % (bb, m.group(3), s)
    if seen:
        print(f, ' | '.join(seen[k] for k in sorted(seen)))
