"""fl3c.py: findKey forms x where the getter's iniSize, off and NULL tests sit.  Scores per getter:
each is independent, so the best form per getter shows up in the table."""
import itertools, re
import fllib as L

L.FLAGS[:] = ['-O3']
B = L.base()
a = B.index('/* getters\' own helper')
b = B.index('/* load and pre-parse options.ini')

FK = '''static int findKey(unsigned char *buf, const char *key)
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
				TAIL
			}
		}
	}
	return -1;
}
'''
TAILS = {
 'q': 'unsigned char *q = &buf[i + len];\n\n\t\t\t\tif (*q != 0)\n\t\t\t\t\treturn i + len;',
 'b': 'if (buf[i + len] != 0)\n\t\t\t\t\treturn i + len;',
 'pl': 'if (p[len] != 0)\n\t\t\t\t\treturn i + len;',
 'cont': 'if (buf[i + len] == 0)\n\t\t\t\t\tcontinue;\n\t\t\t\treturn i + len;',
}
# helpers: H0 none, H1 off test only, H2 size and off test
H1 = '''static char *iniVal(const char *key)
{
	int off;

	off = findKey(xb.iniBuf, key);
	if (off == -1)
		return NULL;
	return (char *)&xb.iniBuf[off];
}
'''
H2 = '''static char *iniVal(const char *key)
{
	int off;

	if (xb.iniSize == 0)
		return NULL;
	off = findKey(xb.iniBuf, key);
	if (off == -1)
		return NULL;
	return (char *)&xb.iniBuf[off];
}
'''
H3 = '''static char *iniVal(const char *key)
{
	int off;

	if (xb.iniSize != 0) {
		off = findKey(xb.iniBuf, key);
		if (off != -1)
			return (char *)&xb.iniBuf[off];
	}
	return NULL;
}
'''
HEAD = {
 # form: (helper, prologue with %(r)s the failure value)
 'plain': ('', '\tint off;\n\tchar *val;\n\tif (xb.iniSize == 0)\n\t\treturn %(r)s;\n\toff = findKey(xb.iniBuf, key);\n\tif (off == -1)\n\t\treturn %(r)s;\n\tval = (char *)&xb.iniBuf[off];\n'),
 'nullafter': ('', '\tint off;\n\tchar *val;\n\tif (xb.iniSize == 0)\n\t\treturn %(r)s;\n\toff = findKey(xb.iniBuf, key);\n\tif (off == -1)\n\t\treturn %(r)s;\n\tval = (char *)&xb.iniBuf[off];\n\tif (val == NULL)\n\t\treturn %(r)s;\n'),
 'h1': (H1, '\tchar *val;\n\tif (xb.iniSize == 0)\n\t\treturn %(r)s;\n\tval = iniVal(key);\n\tif (val == NULL)\n\t\treturn %(r)s;\n'),
 'h2': (H2, '\tchar *val;\n\tval = iniVal(key);\n\tif (val == NULL)\n\t\treturn %(r)s;\n'),
 'h2z': (H2, '\tchar *val;\n\tif (xb.iniSize == 0)\n\t\treturn %(r)s;\n\tval = iniVal(key);\n\tif (val == NULL)\n\t\treturn %(r)s;\n'),
 'h3': (H3, '\tchar *val;\n\tval = iniVal(key);\n\tif (val == NULL)\n\t\treturn %(r)s;\n'),
 'h3nz': (H3, '\tchar *val;\n\tif ((val = iniVal(key)) == NULL)\n\t\treturn %(r)s;\n'),
}


def getters(h):
    d, pro = HEAD[h]
    return d + '''long getIniBool(const char *key, int def)
{
''' + pro % {'r': 'def'} + '''	if (strnicmp(val, "true", 4) == 0)
		return 1;
	if (strnicmp(val, "false", 5) == 0)
		return 0;
	return def;
}

char *iniBoolInvalid(const char *key)
{
''' + pro % {'r': 'NULL'} + '''	if (strnicmp(val, "true", 4) == 0)
		return NULL;
	if (strnicmp(val, "false", 5) != 0)
		return val;
	return NULL;
}

unsigned int getIniU32(const char *key, unsigned int def)
{
''' + pro % {'r': 'def'} + '''	return myatou32(val, def);
}

char *iniU32Invalid(const char *key)
{
''' + pro % {'r': 'NULL'} + '''	if (val[0] == '0' && myatol(val[1]) == 'x') {
		if (validateString(val + 2) == 0)
			return val;
		return NULL;
	}
	if (validateString(val) != 0)
		return NULL;
	return val;
}

'''


V = {}
for t, h in itertools.product(TAILS, HEAD):
    V[t + '_' + h] = B[:a] + FK.replace('TAIL', TAILS[t]) + getters(h) + B[b:]
L.sweep(V, prefix='c3', show=60)
