"""fl6k7.py: comparisons with 0 get no opcode prediction (tree_predict_by_opcode), so a flag or helper result for the match has
probability 50% where j == len has 28%; threading removes the flag later.  Helpers and flags for the match and for the value test."""
import itertools, sys
import fllib as L, fl6lib as F

S = F.drop(F.S0, ['KF'])
A = S.index("/* getters' own helper (not memFindStr) */")
B = S.index("#define FIND findKey(xb.iniBuf, key)")
HEAD, TAIL = S[:A], S[B:]
CM = {'bk': 'buf[i] == key[0]', 'kb': 'key[0] == buf[i]'}
SCAN = "\t\t\tp = &buf[i];\n\t\t\tfor (j = 0; j < len; j++)\n\t\t\t\tif (p[j] != key[j])\n\t\t\t\t\tj = len + 1;\n"
TL = {
    'q': "\t\t\t\tunsigned char *q = &buf[i + len];\n\n\t\t\t\tif (*q != 0)\n\t\t\t\t\treturn i + len;\n",
    'n': "\t\t\t\tif (buf[i + len] != 0)\n\t\t\t\t\treturn i + len;\n",
    'c': "\t\t\t\tif (buf[i + len] == 0)\n\t\t\t\t\tcontinue;\n\t\t\t\treturn i + len;\n",
}
V = {}


def fk(decl, pre, body, tail, c, sig='unsigned char *buf, const char *key'):
    return ("/* getters' own helper (not memFindStr) */\n" + pre + "static int findKey(" + sig + ")\n{\n\tint i, j, len;\n\tunsigned char *p;\n" + decl + "\tlen = strlen(key);\n"
            "\tfor (i = 0; i < xb.iniSize - len; i++) {\n\t\tif (" + c + ") {\n" + body + "\t\t\tif (OK) {\n" + tail + "\t\t\t}\n\t\t}\n\t}\n\treturn -1;\n}\n")


MATCHH = {
    # helper returns via two returns
    'h2': "static int matchAt(unsigned char *p, const char *key, int len)\n{\n\tint j;\n\n\tfor (j = 0; j < len; j++)\n\t\tif (p[j] != key[j])\n\t\t\tj = len + 1;\n\tif (j == len)\n\t\treturn 1;\n\treturn 0;\n}\n\n",
    'h0': "static int matchAt(unsigned char *p, const char *key, int len)\n{\n\tint j;\n\n\tfor (j = 0; j < len; j++)\n\t\tif (p[j] != key[j])\n\t\t\tj = len + 1;\n\tif (j != len)\n\t\treturn 0;\n\treturn 1;\n}\n\n",
    'hv': "static int matchAt(unsigned char *p, const char *key, int len)\n{\n\tint j;\n\tint ok = 0;\n\n\tfor (j = 0; j < len; j++)\n\t\tif (p[j] != key[j])\n\t\t\tj = len + 1;\n\tif (j == len)\n\t\tok = 1;\n\treturn ok;\n}\n\n",
    'hr': "static int matchAt(unsigned char *p, const char *key, int len)\n{\n\tint j;\n\n\tfor (j = 0; j < len; j++)\n\t\tif (p[j] != key[j])\n\t\t\tj = len + 1;\n\treturn j == len;\n}\n\n",
    'hb': "static BOOL matchAt(unsigned char *p, const char *key, int len)\n{\n\tint j;\n\n\tfor (j = 0; j < len; j++)\n\t\tif (p[j] != key[j])\n\t\t\tj = len + 1;\n\tif (j == len)\n\t\treturn TRUE;\n\treturn FALSE;\n}\n\n",
}
for (ck, c), (tk, t) in itertools.product(CM.items(), TL.items()):
    # flags in findKey
    for fk_, st, okexpr in (
        ('f1', "\t\t\tok = 0;\n\t\t\tif (j == len)\n\t\t\t\tok = 1;\n", 'ok'),
        ('f2', "\t\t\tif (j == len)\n\t\t\t\tok = 1;\n\t\t\telse\n\t\t\t\tok = 0;\n", 'ok'),
        ('f3', "\t\t\tok = 1;\n\t\t\tif (j != len)\n\t\t\t\tok = 0;\n", 'ok'),
        ('f4', "\t\t\tok = 0;\n\t\t\tif (j == len)\n\t\t\t\tok = 1;\n", 'ok != 0'),
        ('f5', "\t\t\tok = 0;\n\t\t\tif (j >= len && j <= len)\n\t\t\t\tok = 1;\n", 'ok'),
    ):
        s = fk('\tint ok;\n', '', SCAN + st, t, c).replace('OK', okexpr)
        V['%s,%s,%s' % (fk_, tk, ck)] = HEAD + s + TAIL
    for h, ht in MATCHH.items():
        body = ""
        s = fk('', ht, body, t, c).replace('OK', 'matchAt(&buf[i], key, len)').replace('\tint i, j, len;\n\tunsigned char *p;\n', '\tint i, len;\n')
        V['%s,%s,%s' % (h, tk, ck)] = HEAD + s + TAIL
print(len(V))
if __name__ == '__main__':
    if len(sys.argv) > 1:
        open(F.os.path.join(F.A6, 'k7.c'), 'w', newline='\n').write(V[sys.argv[1]])
    else:
        F.run(V, 'k7', 30)
