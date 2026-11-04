"""python tools/wip/dehint/iw25cmp.py <dumpdir> [pass suffix list]: writeFsTable's ivtmp compares (with their ivtmp and bound names) at sccp-to-optimized passes."""
import os, re, sys
d = sys.argv[1]
for suf in sys.argv[2:] or ['unswitch', 'sccp', 'vect', 'ivopts', 'optimized']:
    f = [x for x in os.listdir(d) if x.endswith('.' + suf)]
    if not f:
        print(suf, 'none'); continue
    t = open(os.path.join(d, f[0]), errors='replace').read()
    m = re.search(r'^;; Function writeFsTable \(.*?(?=^;; Function |\Z)', t, re.S | re.M).group(0)
    c = re.findall(r'if \(((?:ivtmp[._\d]+|_\d+)) != ((?:ivtmp[._\d]+|_\d+))\)', m)
    print(suf, [a + ' ' + b for a, b in c])
    if suf == 'unswitch':
        print('  prephitmp', sorted(set(re.findall(r'prephitmp_\d+', m)))[:12])
