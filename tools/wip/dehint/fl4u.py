"""fl4u.py: findKey's compares and locals with iniU32Invalid's test out (2 lines away), and getIniValue-style getter forms."""
import itertools
import fllib as L, fl4lib as F, fl4final as Z

S = Z.build()
K2 = "\t/* defensive and dead, as in findKey: sets the order of this function's\n\t   buf[i]/key[0] compare */\n\tif (key == NULL)\n\t\treturn NULL;\n"
S1 = L.sub(S, K2, '')
A = '\t\tif (key[0] == buf[i]) {\n\t\t\tp = &buf[i];\n'
B = '\t\t\t\tif (p[j] != key[j])\n'
AF = {'': A, 'swap': '\t\tif (buf[i] == key[0]) {\n\t\t\tp = &buf[i];\n', 'pfirst': '\t\tp = &buf[i];\n\t\tif (key[0] == *p) {\n',
      'pswap': '\t\tp = &buf[i];\n\t\tif (*p == key[0]) {\n', 'scope': '\t\tif (key[0] == buf[i]) {\n\t\t\tunsigned char *p = &buf[i];\n\n'}
BF = {'': B, 'swap': '\t\t\t\tif (key[j] != p[j])\n'}
G0 = '''	/* defensive and dead'''
V = {}
for a, b in itertools.product(AF, BF):
    s = S1
    if a:
        s = L.sub(s, A, AF[a])
    if a == 'scope':
        s = L.sub(s, '\tint i, j, len;\n\tunsigned char *p;\n\tlen = strlen(key);', '\tint i, j, len;\n\tlen = strlen(key);')
    if b:
        s = L.sub(s, B, BF[b])
    V['%s/%s' % (a, b)] = s
# iniU32Invalid's value logic as a helper, called once
U = S1[S1.index('\tval = (char *)&xb.iniBuf[off];\n\tif (val[0] == \'0\''):S1.index('/* load and pre-parse options.ini')]
H = U[U.index('\tif (val[0]'):]
V['u32helper'] = L.sub(S1, U, '\treturn u32Bad((char *)&xb.iniBuf[off]);\n}\n\n').replace('char *iniU32Invalid(const char *key)\n', 'static char *u32Bad(char *val)\n{\n' + H + 'char *iniU32Invalid(const char *key)\n')
F.run(V, 'u', show=14)
