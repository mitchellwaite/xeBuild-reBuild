"""fl3l.py: no pin, findKey tail `buf != xb.iniBuf`; only iniU32Invalid's cmp order left.  (a) two checks in findKey's
tail, (b) natural tests local to iniU32Invalid (conds x arms x positions)."""
import itertools, sys
import fllib as L

L.FLAGS[:] = ['-O3']
B = L.sub(L.base(), '\t__asm__("" :: "b"(val));\n', '')
UNR = '''				unsigned char *q = &buf[i + len];

				if (q == 0)
					__builtin_unreachable();
				if (*q != 0)
					return i + len;
'''
R = '\t\t\t\tif (*q != 0)\n\t\t\t\t\treturn i + len;\n'
Q = '\t\t\t\tunsigned char *q = &buf[i + len];\n\n'
NE = Q + '\t\t\t\tif (buf != xb.iniBuf)\n\t\t\t\t\treturn -1;\n' + R
V = {}
# (a)
T = {
 'ne': 'if (buf != xb.iniBuf)\n\t\t\t\t\treturn -1;\n',
 'nu': 'if (buf == NULL)\n\t\t\t\t\treturn -1;\n',
 'or': 'if (buf == NULL || buf != xb.iniBuf)\n\t\t\t\t\treturn -1;\n',
 'or2': 'if (buf != xb.iniBuf || buf == NULL)\n\t\t\t\t\treturn -1;\n',
 'xz': 'if (xb.iniBuf == NULL)\n\t\t\t\t\treturn -1;\n',
 'sz': 'if (xb.iniSize == 0)\n\t\t\t\t\treturn -1;\n',
 'szn': 'if (xb.iniSize <= 0)\n\t\t\t\t\treturn -1;\n',
 'sl': 'if (i + len >= xb.iniSize)\n\t\t\t\t\treturn -1;\n',
 'kz': 'if (key == NULL)\n\t\t\t\t\treturn -1;\n',
}
for a, b in itertools.permutations(T, 2):
    V['two_%s_%s' % (a, b)] = L.sub(B, UNR, Q + '\t\t\t\t' + T[a] + '\t\t\t\t' + T[b] + R)
for a in T:
    V['one_%s' % a] = L.sub(B, UNR, Q + '\t\t\t\t' + T[a] + R)
# (b)
s0 = L.sub(B, UNR, NE)
g = s0.index('char *iniU32Invalid(')
HEAD = s0[:g]
BODY = s0[g:]
P = {
 'pre': ('\tif (off == -1)\n\t\treturn NULL;\n\tval = (char *)&xb.iniBuf[off];\n', '\tif (off == -1)\n\t\treturn NULL;\n%s\tval = (char *)&xb.iniBuf[off];\n'),
 'aft': ('\tval = (char *)&xb.iniBuf[off];\n', '\tval = (char *)&xb.iniBuf[off];\n%s'),
 'end': ('\tif (validateString(val) != 0)\n', '%s\tif (validateString(val) != 0)\n'),
}
CONDS = ['val == NULL', 'off < 0', 'off == -1', 'off < -1', 'xb.iniBuf == NULL', 'xb.iniSize == 0', 'key == NULL', 'val[0] == 0']
ARMS = ['return NULL;', 'off = 0;', 'val = NULL;', 'xb.iniSize = 0;', 'return val;', 'return (char *)key;']
for p, c, a in itertools.product(P, CONDS, ARMS):
    o, w = P[p]
    if p == 'pre' and 'val' in c:
        continue
    V['%s|%s|%s' % (p, c, a)] = HEAD + L.sub(BODY, o, w % ('\tif (%s)\n\t\t%s\n' % (c, a)))
print(len(V))
rs = L.sweep(V, prefix='l3', show=250, workers=2)
