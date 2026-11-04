"""flx1.py: findKey and iniBoolInvalid's pin: declaration order (DECL_UID orders PHI insertion),
q scope, defensive q test, len type, getter decl order."""
import itertools, re
import fllib as L, flx as X

L.FLAGS[:] = ['-O3']
B = L.base()
a = B.index('static int findKey(unsigned char *buf, const char *key)')
b = B.index('#define FIND findKey')
PIN = '\t__asm__("" :: "b"(val));\n'

BODY = '''static int findKey(unsigned char *buf, const char *key)
{
%(decl)s
	len = strlen(key);
	for (i = 0; i < xb.iniSize - len; i++) {
		if (key[0] == buf[i]) {
			p = &buf[i];
			for (j = 0; j < len; j++)
				if (p[j] != key[j])
					j = len + 1;
			if (j == len) {
%(inner)s
			}
		}
	}
	return -1;
}
'''
TESTS = {
 'unr': ('q', '''				q = &buf[i + len];
				if (q == 0)
					__builtin_unreachable();
				if (*q != 0)
					return i + len;'''),
 'qq': ('q', '''				q = &buf[i + len];
				if (q && *q != 0)
					return i + len;'''),
 'qq2': ('q', '''				q = &buf[i + len];
				if (q != NULL) {
					if (*q != 0)
						return i + len;
				}'''),
 'q': ('q', '''				q = &buf[i + len];
				if (*q != 0)
					return i + len;'''),
 'noq': ('', '''				if (buf[i + len] != 0)
					return i + len;'''),
 'pq': ('', '''				if (p[len] != 0)
					return i + len;'''),
}
V = {}
for t, (qv, inner) in TESTS.items():
    names = ['i', 'j', 'len', 'p'] + ([qv] if qv else [])
    for perm in itertools.permutations(names):
        d = ''
        ints = [x for x in perm]
        d = ''.join('\t%s%s;\n' % ('int ' if x in 'i j len'.split() else 'unsigned char *', x) for x in perm)
        src = B[:a] + BODY % {'decl': d, 'inner': inner} + B[b:]
        for pin in (1, 0):
            s = src if pin else L.sub(src, PIN, '')
            V['%s_%s_%s' % (t, '.'.join(perm), 'pin' if pin else 'nopin')] = s
print(len(V))
rs = L.sweep(V, prefix='k', show=30)
X.write(rs, 'x1.txt')
