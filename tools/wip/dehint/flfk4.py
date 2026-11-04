"""flfk4.py: findKey with key[0] held in a local, and other SSA-order shapes."""
import itertools
import fllib as L

s = L.base()
a = s.index('static int findKey(')
b = s.index('#define FIND')
HEAD = s[:a]
TAIL = s[b:]
PIN = '	__asm__("" :: "b"(val));\n'
T = """static int findKey(unsigned char *buf, const char *key)
{
	int i, j, len;
	%(decl)s
	%(pre1)s
	len = strlen(key);
	%(pre2)s
	for (i = 0; i < xb.iniSize - len; i++) {
		%(body)s
	}
	return -1;
}
"""
BODY = {
 'p': """if (%(c)s == buf[i]) {
			unsigned char *p = &buf[i];
			for (j = 0; j < len; j++)
				if (p[j] != key[j])
					j = len + 1;
			if (j == len) {
				if (buf[i + len] != 0)
					return i + len;
			}
		}""",
 'b': """if (%(c)s == buf[i]) {
			for (j = 0; j < len; j++)
				if (buf[i + j] != key[j])
					j = len + 1;
			if (j == len && buf[i + len] != 0)
				return i + len;
		}""",
 'q': """if (%(c)s == buf[i]) {
			unsigned char *p = &buf[i];
			for (j = 0; j < len; j++)
				if (p[j] != key[j])
					j = len + 1;
			if (j == len) {
				p += len;
				if (*p != 0)
					return i + len;
			}
		}""",
 'loc': """{
			unsigned char *p = &buf[i];
			if (%(c)s == *p) {
			for (j = 0; j < len; j++)
				if (p[j] != key[j])
					j = len + 1;
			if (j == len && p[len] != 0)
				return i + len;
			}
		}""",
}
V = {}
for ty in ['char', 'int', 'unsigned char']:
    for where in ['before', 'after']:
        for bn, bd in BODY.items():
            for pin in (1, 0):
                d = {'decl': ty + ' c;', 'pre1': 'c = key[0];' if where == 'before' else '',
                     'pre2': 'c = key[0];' if where == 'after' else '', 'body': bd % {'c': 'c'}}
                src = HEAD + T % d + TAIL
                if not pin:
                    src = L.sub(src, PIN, '')
                V['%s_%s_%s_%d' % (ty.replace(' ', ''), where, bn, pin)] = src
for bn, bd in BODY.items():
    d = {'decl': '', 'pre1': '', 'pre2': '', 'body': bd % {'c': 'key[0]'}}
    V['plain_' + bn] = HEAD + T % d + TAIL
L.sweep(V, prefix='fk4', show=40)
