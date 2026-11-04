"""python tools/wip/dehint/iw11trace.py <dumpdir> <fn>: per tree pass, the position of the block that feeds the ECC entry (`val = PHI <0(..)` etc.):
the chain order of blocks around the mismatch join in <fn>.  For each pass prints: number of blocks, the ECC entry's index, and the block(s) that give it the constant 0 with their predecessors' count."""
import glob, os, re, sys

d, fn = sys.argv[1:3]
order = sorted(glob.glob(os.path.join(d, 'a.c.*')), key=lambda f: int(re.search(r'a\.c\.(\d+)', f).group(1)) if re.search(r'a\.c\.(\d+)', f) else 0)
for f in order:
    suf = re.sub(r'^\d+[tri]\.', '', f.split('a.c.')[1])
    p = os.path.join(d, fn + '.' + suf)
    if not os.path.exists(p):
        continue
    t = open(p, errors='replace').read()
    bl = re.split(r'^\s*<bb (\d+)>:\s*$', t, flags=re.M)
    ids = [int(x) for x in bl[1::2]]
    if not ids:
        continue
    # ECC entry: the block with a PHI whose arg is 0 from a block, and `& 31`
    hits = []
    for i in range(1, len(bl), 2):
        b = bl[i + 1]
        if re.search(r'& 31;', b):
            ph = re.findall(r'# (\w+) = PHI <([^>]*)>', b)
            hits.append((bl[i], [x[1][:50] for x in ph[:1]]))
    print('%-20s n=%3d  order=%s  ecc=%s' % (suf, len(ids), ' '.join(map(str, ids[:16])), hits[:1]))
