"""fl5k.py: findKey with no test: getters through value helpers (iniVal), at the current `buf[i] == key[0]`; the scan as a helper with the
xb reads in a wrapper; test-first loop forms.  Getter functions' diff only."""
import itertools, re, sys
import fllib as L, fl5lib as F

T = ('raw', 'off3', 'off4', 'x')
B = F.gen(T, kf=False)
a = B.index("/* getters' own helper (not memFindStr) */")
b = B.index('/* load and pre-parse options.ini')

SCAN = {
    'cur': ('static int findKey(unsigned char *buf, const char *key)\n{\n\tint i, j, len;\n\tunsigned char *p;\n\tlen = strlen(key);\n'
            '\tfor (i = 0; i < xb.iniSize - len; i++) {\n\t\tif (CMP) {\n\t\t\tp = &buf[i];\n\t\t\tfor (j = 0; j < len; j++)\n\t\t\t\tif (p[j] != key[j])\n\t\t\t\t\tj = len + 1;\n'
            '\t\t\tif (j == len) {\nTAIL\t\t\t}\n\t\t}\n\t}\n\treturn -1;\n}\n'),
    'first': ('static int findKey(unsigned char *buf, const char *key)\n{\n\tint i, j, len;\n\tunsigned char *p;\n\tlen = strlen(key);\n'
              '\tfor (i = 0; ; i++) {\n\t\tif (i >= xb.iniSize - len)\n\t\t\tbreak;\n\t\tif (CMP) {\n\t\t\tp = &buf[i];\n\t\t\tfor (j = 0; j < len; j++)\n\t\t\t\tif (p[j] != key[j])\n\t\t\t\t\tj = len + 1;\n'
              '\t\t\tif (j == len) {\nTAIL\t\t\t}\n\t\t}\n\t}\n\treturn -1;\n}\n'),
    'noj': ('static int findKey(unsigned char *buf, const char *key)\n{\n\tint i, len;\n\tlen = strlen(key);\n'
            '\tfor (i = 0; i < xb.iniSize - len; i++) {\n\t\tif (CMP) {\n\t\t\tunsigned char *p = &buf[i];\n\t\t\tint j;\n\n\t\t\tfor (j = 0; j < len; j++)\n\t\t\t\tif (p[j] != key[j])\n\t\t\t\t\tj = len + 1;\n'
            '\t\t\tif (j == len) {\nTAIL\t\t\t}\n\t\t}\n\t}\n\treturn -1;\n}\n'),
}
CMPS = {'bk': 'buf[i] == key[0]', 'kb': 'key[0] == buf[i]'}
TAILS = {
    'q': '\t\t\t\tunsigned char *q = &buf[i + len];\n\n\t\t\t\tif (*q != 0)\n\t\t\t\t\treturn i + len;\n',
    'b': '\t\t\t\tif (buf[i + len] != 0)\n\t\t\t\t\treturn i + len;\n',
    'p': '\t\t\t\tif (p[len] != 0)\n\t\t\t\t\treturn i + len;\n',
    'o': '\t\t\t\tint off = i + len;\n\n\t\t\t\tif (buf[off] != 0)\n\t\t\t\t\treturn off;\n',
    'c': '\t\t\t\tif (buf[i + len] == 0)\n\t\t\t\t\tcontinue;\n\t\t\t\treturn i + len;\n',
}
GETS_F = {
 'plain': '''#define FIND findKey(xb.iniBuf, key)
long getIniBool(const char *key, int def)
{
	int off;
	char *val;
	if (xb.iniSize == 0)
		return def;
	off = FIND;
	if (off == -1)
		return def;
	val = (char *)&xb.iniBuf[off];
	if (strnicmp(val, "true", 4) == 0)
		return 1;
	if (strnicmp(val, "false", 5) == 0)
		return 0;
	return def;
}

char *iniBoolInvalid(const char *key)
{
	int off;
	char *val;
	if (xb.iniSize == 0)
		return NULL;
	off = FIND;
	if (off == -1)
		return NULL;
	val = (char *)&xb.iniBuf[off];
	if (strnicmp(val, "true", 4) == 0)
		return NULL;
	if (strnicmp(val, "false", 5) != 0)
		return val;
	return NULL;
}
unsigned int getIniU32(const char *key, unsigned int def)
{
	int off;
	if (xb.iniSize == 0)
		return def;
	off = FIND;
	if (off == -1)
		return def;
	return myatou32((char *)&xb.iniBuf[off], def);
}
char *iniU32Invalid(const char *key)
{
	int off;
	char *val;
	if (xb.iniSize == 0)
		return NULL;
	off = FIND;
	if (off == -1)
		return NULL;
	val = (char *)&xb.iniBuf[off];
	if (val[0] == '0' && myatol(val[1]) == 'x') {
		if (validateString(val + 2) == 0)
			return val;
		return NULL;
	}
	if (validateString(val) != 0)
		return NULL;
	return val;
}
''',
 'val': '''static char *iniVal(const char *key)
{
	int off;

	off = findKey(xb.iniBuf, key);
	if (off == -1)
		return NULL;
	return (char *)&xb.iniBuf[off];
}
long getIniBool(const char *key, int def)
{
	char *val;
	if (xb.iniSize == 0)
		return def;
	val = iniVal(key);
	if (val == NULL)
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
	if (xb.iniSize == 0)
		return NULL;
	val = iniVal(key);
	if (val == NULL)
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
	if (xb.iniSize == 0)
		return def;
	val = iniVal(key);
	if (val == NULL)
		return def;
	return myatou32(val, def);
}
char *iniU32Invalid(const char *key)
{
	char *val;
	if (xb.iniSize == 0)
		return NULL;
	val = iniVal(key);
	if (val == NULL)
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
''',
 'val2': '''static char *iniVal(const char *key)
{
	int off;

	if (xb.iniSize == 0)
		return NULL;
	off = findKey(xb.iniBuf, key);
	if (off == -1)
		return NULL;
	return (char *)&xb.iniBuf[off];
}
long getIniBool(const char *key, int def)
{
	char *val = iniVal(key);

	if (val == NULL)
		return def;
	if (strnicmp(val, "true", 4) == 0)
		return 1;
	if (strnicmp(val, "false", 5) == 0)
		return 0;
	return def;
}

char *iniBoolInvalid(const char *key)
{
	char *val = iniVal(key);

	if (val == NULL)
		return NULL;
	if (strnicmp(val, "true", 4) == 0)
		return NULL;
	if (strnicmp(val, "false", 5) != 0)
		return val;
	return NULL;
}
unsigned int getIniU32(const char *key, unsigned int def)
{
	char *val = iniVal(key);

	if (val == NULL)
		return def;
	return myatou32(val, def);
}
char *iniU32Invalid(const char *key)
{
	char *val = iniVal(key);

	if (val == NULL)
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
''',
}
# a wrapper over a scan taking size: the xb reads are arguments
WRAP = {
    'none': lambda fk: fk,
    'size': lambda fk: fk.replace('static int findKey(unsigned char *buf, const char *key)', 'static int scanKey(unsigned char *buf, int size, const char *key)').replace('xb.iniSize - len', 'size - len')
                       + 'static int findKey(unsigned char *buf, const char *key)\n{\n\treturn scanKey(buf, xb.iniSize, key);\n}\n',
    'lenp': lambda fk: fk.replace('static int findKey(unsigned char *buf, const char *key)\n{\n\tint i, j, len;\n\tunsigned char *p;\n\tlen = strlen(key);\n', 'static int scanKey(unsigned char *buf, const char *key, int len)\n{\n\tint i, j;\n\tunsigned char *p;\n\n')
                       .replace('static int findKey(unsigned char *buf, const char *key)\n{\n\tint i, len;\n\tlen = strlen(key);\n', 'static int scanKey(unsigned char *buf, const char *key, int len)\n{\n\tint i;\n\n')
                       + 'static int findKey(unsigned char *buf, const char *key)\n{\n\treturn scanKey(buf, key, strlen(key));\n}\n',
}


def gen(scan, cmp_, tail, wrap, gets):
    fk = SCAN[scan].replace('CMP', CMPS[cmp_]).replace('TAIL', TAILS[tail])
    fk = WRAP[wrap](fk)
    return B[:a] + fk + GETS_F[gets] + '\n' + B[b:]


V = {}
for c in itertools.product(SCAN, CMPS, TAILS, WRAP, GETS_F):
    V['/'.join(c)] = gen(*c)
print(len(V))
F.run(V, 'k', show=25)
