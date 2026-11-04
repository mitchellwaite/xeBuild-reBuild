"""flfk1.py: findKey shapes without the unreachable (with and without the pin)."""
import itertools
import fllib as L

s = L.base()
a = s.index('static int findKey(')
b = s.index('#define FIND')
HEAD = s[:a]
TAIL = s[b:]
PIN = '	__asm__("" :: "b"(val));\n'


def fk(check, inner='p[j] != key[j]', decl='', pre='p = &buf[i];', loop=None, loopdecl='unsigned char *p;'):
    lp = loop or 'i < xb.iniSize - len'
    return """static int findKey(unsigned char *buf, const char *key)
{
	int i, j, len;
	%s
	len = strlen(key);
	for (i = 0; %s; i++) {
		if (key[0] == buf[i]) {
			%s
			for (j = 0; j < len; j++)
				if (%s)
					j = len + 1;
			%s
		}
	}
	return -1;
}
""" % (loopdecl, lp, pre, inner, check)


CH = {
 'and': 'if (j == len && buf[i + len] != 0) return i + len;',
 'nest': 'if (j == len) { if (buf[i + len] != 0) return i + len; }',
 'pl': 'if (j == len) { if (p[len] != 0) return i + len; }',
 'pland': 'if (j == len && p[len] != 0) return i + len;',
 'q': 'if (j == len) { unsigned char *q = &buf[i + len]; if (*q != 0) return i + len; }',
 'qp': 'if (j == len) { unsigned char *q = p + len; if (*q != 0) return i + len; }',
 'qdiff': 'if (j == len) { unsigned char *q = &buf[i + len]; if (*q != 0) return q - buf; }',
 'k': 'if (j == len) { int k = i + len; if (buf[k] != 0) return k; }',
 'kq': 'if (j == len) { int k = i + len; unsigned char *q = &buf[k]; if (*q != 0) return k; }',
 'inc': 'if (j == len) { if (buf[i + j] != 0) return i + j; }',
 'incand': 'if (j == len && buf[i + j] != 0) return i + j;',
 'pj': 'if (j == len) { if (p[j] != 0) return i + j; }',
 'pjl': 'if (j == len) { if (p[j] != 0) return i + len; }',
 'eq0': 'if (j == len) { if (buf[i + len] == 0) continue; return i + len; }',
 'nz': 'if (j == len) { if (buf[i + len]) return i + len; }',
}
V = {}
for n, c in CH.items():
    for inn, ni in (('p', 'p[j] != key[j]'), ('b', 'buf[i + j] != key[j]')):
        V[n + '_' + inn] = HEAD + fk(c, ni) + TAIL
        V[n + '_' + inn + '_nopin'] = L.sub(HEAD + fk(c, ni) + TAIL, PIN, '')

if __name__ == '__main__':
    L.sweep(V, prefix='fk1', show=20)
