"""fl3m.py: no pin.  findKey tail (test choice, q local or not) x a `key == NULL` check after the off test in any subset of the getters."""
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
R2 = '\t\t\t\tif (buf[i + len] != 0)\n\t\t\t\t\treturn i + len;\n'
T = {
 'none': ('', ''),
 'kz': ('if (key == NULL)\n\t\t\t\t\treturn -1;\n', ''),
 'kzb': ('if (key == NULL)\n\t\t\t\t\tbreak;\n', ''),
 'ne': ('if (buf != xb.iniBuf)\n\t\t\t\t\treturn -1;\n', ''),
 'sz': ('if (xb.iniSize == 0)\n\t\t\t\t\treturn -1;\n', ''),
 'nu': ('if (buf == NULL)\n\t\t\t\t\treturn -1;\n', ''),
 'lz': ('if (len < 0)\n\t\t\t\t\treturn -1;\n', ''),
}
TAIL = {}
for k, (t, _) in T.items():
    TAIL[k] = Q + ('\t\t\t\t' + t if t else '') + R
    TAIL[k + '-nq'] = ('\t\t\t\t' + t if t else '') + R2
GET = {
 'B': ('long getIniBool(const char *key, int def)', 'return def;'),
 'I': ('char *iniBoolInvalid(const char *key)', 'return NULL;'),
 'U': ('unsigned int getIniU32(const char *key, unsigned int def)', 'return def;'),
 'V': ('char *iniU32Invalid(const char *key)', 'return NULL;'),
}


def addtest(s, g, cond='key == NULL'):
    sig, r = GET[g]
    a = s.index(sig)
    o = '\tif (off == -1)\n\t\t%s\n' % r
    k = s.index(o, a) + len(o)
    return s[:k] + '\tif (%s)\n\t\t%s\n' % (cond, r) + s[k:]


V = {}
for t, n in itertools.product(TAIL, range(0, 5)):
    for gs in itertools.combinations('BIUV', n):
        s = L.sub(B, UNR, TAIL[t])
        for g in gs:
            s = addtest(s, g)
        V[t + '_' + ''.join(gs)] = s
print(len(V))
L.sweep(V, prefix='m3', show=30, workers=3)
