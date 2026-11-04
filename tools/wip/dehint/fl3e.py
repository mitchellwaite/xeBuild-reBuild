"""fl3e.py: natural redundant checks in findKey's tail and head in place of the unreachable, pin kept.
Tests x arms x positions; the score shows which lives long enough to do what the unreachable does."""
import itertools, sys
import fllib as L

L.FLAGS[:] = ['-O3']
B = L.base()
UNR = '''				unsigned char *q = &buf[i + len];

				if (q == 0)
					__builtin_unreachable();
				if (*q != 0)
					return i + len;
'''
CONDS = ['q == NULL', 'len < 0', 'i + len < 0', 'i < 0', 'j < 0', 'j != len', 'len == -1', 'i + len == -1', 'q < buf',
         'q < p', 'q == p - 1', 'p == NULL', 'i >= xb.iniSize', 'i + len >= xb.iniSize', 'i + len > xb.iniSize', 'j > len',
         'buf == NULL', 'i == -1', 'len > xb.iniSize', 'xb.iniSize <= 0', 'xb.iniSize == 0', 'xb.iniSize < len', 'key == NULL', 'key[0] == 0 && len > 0',
         'len < j', 'len <= 0 && i < 0', 'xb.iniBuf != buf', 'xb.iniBuf == NULL', 'p != &buf[i]', 'q != &p[len]', 'q != &buf[i + j]']
ARMS = {
 'ret': 'return -1;',
 'cont': 'continue;',
 'brk': 'break;',
 'len0': 'len = 0;',
 'i': 'i = xb.iniSize;',
 'j': 'j = 0;',
 'q': 'q = buf;',
 'sz': 'xb.iniSize = 0;',
}
V = {}
for c, (an, arm) in itertools.product(CONDS, ARMS.items()):
    V['%s|%s|bef' % (c, an)] = L.sub(B, UNR, '\t\t\t\tunsigned char *q = &buf[i + len];\n\n\t\t\t\tif (%s)\n\t\t\t\t\t%s\n\t\t\t\tif (*q != 0)\n\t\t\t\t\treturn i + len;\n' % (c, arm))
    V['%s|%s|aft' % (c, an)] = L.sub(B, UNR, '\t\t\t\tunsigned char *q = &buf[i + len];\n\n\t\t\t\tif (*q != 0) {\n\t\t\t\t\tif (%s)\n\t\t\t\t\t\t%s\n\t\t\t\t\treturn i + len;\n\t\t\t\t}\n' % (c, arm))
print(len(V))
rs = L.sweep(V, prefix='e3', show=40)
with open(L.BD + '/a3/e3.txt', 'w', newline='\n') as f:
    for n, r in rs:
        f.write('%s\t%s\t%s\n' % (r[0], n, r[2]))
