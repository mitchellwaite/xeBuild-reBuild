"""attempt 15, probe only: python tools/wip/dehint/iw15grid.py <base.c> [kmax] [mmax]: K names freed at VRP1 by a dead arm x M partially redundant `off >> n` (PRE PHIs, live until later).
Prints every state whose writeFsTable signature (iw15sig) is the target <>><<, and a table of signatures. Neither is a candidate; they tell what stack position the compares want."""
import os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib, iw15sig
base = sys.argv[1]
kmax = int(sys.argv[2]) if len(sys.argv) > 2 else 24
mmax = int(sys.argv[3]) if len(sys.argv) > 3 else 6
s = open(base, newline='').read().replace('\r\n', '\n')
A1 = '	blk = off >> 14;\n	if (xb.bigBlock && (off & 0x1ffff)) {\n		off = (off + 0x20000) & ~0x1ffff;\n		blk = off >> 14;\n	}\n'
E = '	setBeU16(0, (uint8_t *)&xb.fsReserved);\n'
PS = '	if (!xb.bigBlock)\n		goto small;\n'
OPS = ['z += 1;', 'z ^= 3;', 'z <<= 2;', 'z -= 7;', 'z |= 9;', 'z >>= 1;', 'z *= 5;', 'z &= 0xfff;', 'z += off;', 'z ^= off;']
out = os.path.join(iwlib.BUILD, 'a15', 'grid')
os.makedirs(out, exist_ok=True)
def make(k, m):
    t = s
    if m:
        u = ['u%d' % i for i in range(m)]
        new = '	blk = off >> 14;\n' + ''.join('	%s = off >> %d;\n' % (n, 13 - i) for i, n in enumerate(u)) + '	if (xb.bigBlock && (off & 0x1ffff)) {\n		off = (off + 0x20000) & ~0x1ffff;\n		blk = off >> 14;\n' + ''.join('		%s = off >> %d;\n' % (n, 13 - i) for i, n in enumerate(u)) + '	}\n'
        t = t.replace(A1, new).replace('	uint32_t blk;\n	int i;\n', '	uint32_t blk;\n	int i;\n' + ''.join('	uint32_t %s;\n' % n for n in u))
        t = t.replace(E, ''.join('	setBeU16(off >> %d, (uint8_t *)&xb.fsReserved);\n' % (13 - i) for i in range(m)) + E)
    if k:
        b = ' '.join(OPS[j % 10] for j in range(k))
        t = t.replace(PS, '	if ((off & 0x3fff) > 0x3fff) {\n		uint32_t z = off;\n		%s\n		off = z;\n	}\n' % b + PS)
    return t
def one(a):
    k, m = a
    p = os.path.join(out, 'g_%d_%d.c' % (k, m))
    t = make(k, m)
    open(p, 'w', newline='\n').write(t)
    sg, ns = iw15sig.sig(p)
    return k, m, sg, ns
grid = [(k, m) for k in range(kmax + 1) for m in range(mmax + 1)]
with ThreadPoolExecutor(4) as ex:
    res = list(ex.map(one, grid))
for m in range(mmax + 1):
    print('m%d ' % m + ' '.join(r[2] for r in res if r[1] == m))
for k, m, sg, ns in res:
    if sg == '<>><<':
        r = iwlib.score_text(make(k, m), [])
        print('HIT k%d m%d' % (k, m), ns, iwlib.fmt(r)[:120])
