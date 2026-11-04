"""fl3p.py: the comma site from the lean state: conditions on defined values that might last as long as `comma < -1` (until RTL)."""
import itertools
import fllib as L, fl3g as G

base = G.st('comma=1,i=1,len=1,nul=1,off3=2,off4=1,x=2')
CONDS = ['(off | 1) == 0', '(off & 3) > 3', '(size >> 31) > 0', '&tmp[1] == tmp', 'tmp == label', 'label + 1 == label', '(unsigned)off > 0xffffffffU', 'xb.files == NULL', 'consoleNames[0] != NULL',
         'validChars[0] == 0', 'fnNone == NULL', '(char)off > 127', '(unsigned char)off > 255', 'off - off != 0', '(off ^ off) != 0', '!off && off', 'off < 0 && off > 0', 'nbl > 9', 'nbl < 6', 'nbl == 0', 'nbl != 6 && nbl != 9',
         'end < off - 1', 'end + 1 < off', 'pos < -1', 'nul < -1', 'len < -1', 'n < -1', 'p == NULL', 'e == NULL', 's == NULL', 'crc > 0xffffffffU', 'noCrc > 1']
V = {}
for c, a in itertools.product(CONDS, [1, 2, 3, 'pos = size', 'return 0', 'free(buf); return 0']):
    s = dict(base)
    s['comma'] = (c, a)
    V['%s:%s' % (c, a)] = G.gen(s)
print(len(V))
rs = L.sweep(V, prefix='p3', show=20)
print('MATCH', [n for n, r in rs if r[0] == 0])
