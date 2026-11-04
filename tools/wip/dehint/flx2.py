"""flx2.py: parseIni's declaration order, random sample at a few dead/flen states."""
import random, sys
import fllib as L, flx as X

DECL = '''	int size, off, end, pos, len, nul, comma, n, i, nbl;
	uint32_t noCrc;
	struct fileent *e;
	char *s;
	uint32_t crc;
	char label[50];
	char tmp[0x400];
'''
HEAD = '	unsigned char *buf, *p;\n'
NAMES = {'size': 'int ', 'off': 'int ', 'end': 'int ', 'pos': 'int ', 'len': 'int ', 'nul': 'int ', 'comma': 'int ',
         'n': 'int ', 'i': 'int ', 'nbl': 'int ', 'noCrc': 'uint32_t ', 'e': 'struct fileent *', 's': 'char *',
         'crc': 'uint32_t ', 'label': 'char ', 'tmp': 'char ', 'buf': 'unsigned char *', 'p': 'unsigned char *'}
SUF = {'label': '[50]', 'tmp': '[0x400]'}
STATES = [(('t', 'len'), 'asm'), (('i', 'off3', 'off5', 't'), 'nest'), (('comma', 'i', 'off3', 'off4', 'off5', 't', 'len'), 'asm'),
          (X.ALLDEAD, 'nest')]
N = int(sys.argv[1]) if len(sys.argv) > 1 else 200
random.seed(int(sys.argv[2]) if len(sys.argv) > 2 else 1)


def declare(order):
    return ''.join('\t%s%s%s;\n' % (NAMES[x], x, SUF.get(x, '')) for x in order)


V = {}
names = list(NAMES)
for k in range(N):
    random.shuffle(names)
    d = declare(names)
    for si, (dd, fl) in enumerate(STATES):
        s = X.gen(dd, fl)
        s = L.sub(s, HEAD + DECL, d)
        V['%d_%s' % (si, '.'.join(names))] = s
print(len(V))
rs = L.sweep(V, prefix='d', show=20)
X.write(rs, 'x2.txt')
from collections import Counter
c = Counter((n.split('_')[0], r[0]) for n, r in rs)
for k in sorted(c):
    print(k, c[k])
