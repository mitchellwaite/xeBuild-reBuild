"""fl4w.py: findKey without any test (buf[i] == key[0] base): helpers for the match and the tail, and small live forms."""
import itertools
import fllib as L, fl4lib as F, fl4final as Z

S = Z.build()
K1 = "\t\t\t\t/* defensive, and dead (key was read above): VRP removes it, and\n\t\t\t\t   until then it sets findKey's SSA numbers in the getters */\n\t\t\t\tif (key == NULL)\n\t\t\t\t\treturn -1;\n"
I = S.index('/* getters\' own helper (not memFindStr) */')
J = S.index('#define FIND findKey')
FK = S[I:J]
HEAD = '''static int findKey(unsigned char *buf, const char *key)
{
	int i, j, len;
	unsigned char *p;
	len = strlen(key);
	for (i = 0; i < xb.iniSize - len; i++) {
		if (buf[i] == key[0]) {
			p = &buf[i];
			for (j = 0; j < len; j++)
				if (p[j] != key[j])
					j = len + 1;
			if (j == len) {
'''
assert HEAD in FK, FK
MATCHH = '''static int keyAt(unsigned char *p, const char *key, int len)
{
	int j;

	for (j = 0; j < len; j++)
		if (p[j] != key[j])
			j = len + 1;
	return j == len;
}

'''
H1 = MATCHH + '''static int findKey(unsigned char *buf, const char *key)
{
	int i, len;
	len = strlen(key);
	for (i = 0; i < xb.iniSize - len; i++) {
		if (buf[i] == key[0]) {
			if (keyAt(&buf[i], key, len)) {
%s
			}
		}
	}
	return -1;
}
'''
H1B = MATCHH + '''static int findKey(unsigned char *buf, const char *key)
{
	int i, len;
	len = strlen(key);
	for (i = 0; i < xb.iniSize - len; i++) {
		if (buf[i] == key[0] && keyAt(&buf[i], key, len)) {
%s
		}
	}
	return -1;
}
'''
TAILH = '''static int findKey(unsigned char *buf, const char *key)
{
	int i, j, len;
	unsigned char *p;
	len = strlen(key);
	for (i = 0; i < xb.iniSize - len; i++) {
		if (buf[i] == key[0]) {
			p = &buf[i];
			for (j = 0; j < len; j++)
				if (p[j] != key[j])
					j = len + 1;
			if (j == len) {
%s
			}
		}
	}
	return -1;
}
'''
TAILS = {
    'q': '\t\t\t\tunsigned char *q = &buf[i + len];\n\n\t\t\t\tif (*q != 0)\n\t\t\t\t\treturn i + len;',
    'noq': '\t\t\t\tif (buf[i + len] != 0)\n\t\t\t\t\treturn i + len;',
    'off': '\t\t\t\tint off = i + len;\n\n\t\t\t\tif (buf[off] != 0)\n\t\t\t\t\treturn off;',
    'offq': '\t\t\t\tint off = i + len;\n\t\t\t\tunsigned char *q = &buf[off];\n\n\t\t\t\tif (*q != 0)\n\t\t\t\t\treturn off;',
    'ptr': '\t\t\t\tif (p[len] != 0)\n\t\t\t\t\treturn i + len;',
    'ptr2': '\t\t\t\tp += len;\n\t\t\t\tif (*p != 0)\n\t\t\t\t\treturn p - buf;',
    'valh': '\t\t\t\tif (hasValue(buf, i + len))\n\t\t\t\t\treturn i + len;',
}
VALH = 'static int hasValue(unsigned char *buf, int off)\n{\n\treturn buf[off] != 0;\n}\n\n'
V = {}
for t, x in TAILS.items():
    for nm, form in (('tail', TAILH), ('h1', H1), ('h1b', H1B)):
        fk = form % x
        if t == 'ptr' or t == 'ptr2':
            if nm != 'tail':
                continue
        if t == 'valh':
            fk = VALH + fk
        V['%s %s' % (nm, t)] = S[:I] + fk + S[J:]
# whole-loop search in a helper, as memFindStr: findKey(buf, key) wraps it with xb.iniSize
SZ = S[:I] + (TAILH % TAILS['q']).replace('static int findKey(unsigned char *buf, const char *key)', 'static int findKeyIn(unsigned char *buf, int size, const char *key)').replace('xb.iniSize - len', 'size - len') + 'static int findKey(unsigned char *buf, const char *key)\n{\n\treturn findKeyIn(buf, xb.iniSize, key);\n}\n' + S[J:]
V['sized'] = SZ
V['sized2'] = SZ.replace('#define FIND findKey(xb.iniBuf, key)', '#define FIND findKeyIn(xb.iniBuf, xb.iniSize, key)')
F.run(V, 'w', show=26)
