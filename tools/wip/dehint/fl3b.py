"""fl3b.py: getters built on a value helper (a NULL test on the pointer, which VRP can drop after
findKey's deref), or on memFindStr / findIniKey directly.  No unreachable, no pin."""
import itertools
import fllib as L

L.FLAGS[:] = ['-O3']
B = L.base()
a = B.index('/* getters\' own helper')
b = B.index('/* load and pre-parse options.ini')

FKBODY = '''static int findKey(unsigned char *buf, const char *key)
{
	int i, j, len;
	unsigned char *p;
	len = strlen(key);
	for (i = 0; i < xb.iniSize - len; i++) {
		if (key[0] == buf[i]) {
			p = &buf[i];
			for (j = 0; j < len; j++)
				if (p[j] != key[j])
					j = len + 1;
			if (j == len) {
				unsigned char *q = &buf[i + len];

				if (*q != 0)
					return i + len;
			}
		}
	}
	return -1;
}
'''
FKBODY2 = FKBODY.replace('''				unsigned char *q = &buf[i + len];

				if (*q != 0)
					return i + len;
''', '''				if (buf[i + len] != 0)
					return i + len;
''')
HELP = {
 # name: (definitions, expression giving val)
 'gv': ('', 'getIniValue(key)'),
 'stat': (FKBODY + '''static char *iniVal(const char *key)
{
	int off;

	if (xb.iniSize == 0)
		return NULL;
	off = findKey(xb.iniBuf, key);
	if (off == -1)
		return NULL;
	return (char *)&xb.iniBuf[off];
}
''', 'iniVal(key)'),
 'stat2': (FKBODY2 + '''static char *iniVal(const char *key)
{
	int off;

	if (xb.iniSize == 0)
		return NULL;
	off = findKey(xb.iniBuf, key);
	if (off == -1)
		return NULL;
	return (char *)&xb.iniBuf[off];
}
''', 'iniVal(key)'),
 'statinl': (FKBODY2 + '''static inline char *iniVal(const char *key)
{
	int off;

	if (xb.iniSize == 0)
		return NULL;
	off = findKey(xb.iniBuf, key);
	if (off == -1)
		return NULL;
	return (char *)&xb.iniBuf[off];
}
''', 'iniVal(key)'),
 'statmfs': ('''static char *iniVal(const char *key)
{
	int off;

	if (xb.iniSize == 0)
		return NULL;
	off = memFindStr(xb.iniBuf, xb.iniSize, key, 0);
	if (off == -1)
		return NULL;
	return (char *)&xb.iniBuf[off];
}
''', 'iniVal(key)'),
 'statfik': ('''static char *iniVal(const char *key)
{
	int off;

	if (xb.iniSize == 0)
		return NULL;
	off = findIniKey(xb.iniBuf, xb.iniSize, key);
	if (off == -1)
		return NULL;
	return (char *)&xb.iniBuf[off];
}
''', 'iniVal(key)'),
}
TESTS = {
 'eq': 'if (val == NULL)',
 'not': 'if (!val)',
}
def getters(expr, t):
    return '''long getIniBool(const char *key, int def)
{
	char *val;

	val = %(e)s;
	%(t)s
		return def;
	if (strnicmp(val, "true", 4) == 0)
		return 1;
	if (strnicmp(val, "false", 5) == 0)
		return 0;
	return def;
}

char *iniBoolInvalid(const char *key)
{
	char *val;

	val = %(e)s;
	%(t)s
		return NULL;
	if (strnicmp(val, "true", 4) == 0)
		return NULL;
	if (strnicmp(val, "false", 5) != 0)
		return val;
	return NULL;
}

unsigned int getIniU32(const char *key, unsigned int def)
{
	char *val;

	val = %(e)s;
	%(t)s
		return def;
	return myatou32(val, def);
}

char *iniU32Invalid(const char *key)
{
	char *val;

	val = %(e)s;
	%(t)s
		return NULL;
	if (val[0] == '0' && myatol(val[1]) == 'x') {
		if (validateString(val + 2) == 0)
			return val;
		return NULL;
	}
	if (validateString(val) != 0)
		return NULL;
	return val;
}

''' % {'e': expr, 't': t}

V = {}
for h, t in itertools.product(HELP, ['eq']):
    d, e = HELP[h]
    V[h] = B[:a] + d + getters(e, TESTS[t]) + B[b:]
rs = L.sweep(V, prefix='b3', show=40)
for n, r in rs:
    print(n, r[0], r[3])
