"""fl6k9.py: findKey through a keyAt() predicate holding the whole test (first char, rest, non-empty value), returning 1/0; and
flag shapes for the head, to see what profile they give.  matchAt's 6 lines are iniU32Invalid's ebx/ecx level (notes)."""
import itertools, sys
import fllib as L, fl6lib as F

S = F.drop(F.S0, ['KF'])
A = S.index("/* getters' own helper (not memFindStr) */")
B = S.index("#define FIND findKey(xb.iniBuf, key)")
HEAD, TAIL = S[:A], S[B:]
V = {}
SCANP = "\tfor (j = 0; j < len; j++)\n\t\tif (p[j] != key[j])\n\t\t\tj = len + 1;\n"
SCANB = "\tfor (j = 0; j < len; j++)\n\t\tif (buf[i + j] != key[j])\n\t\t\tj = len + 1;\n"
LOOP = "for (i = 0; i < xb.iniSize - len; i++)"

FORMS = {
    # (helper, call, loop body)
    'A': ("static int keyAt(unsigned char *p, const char *key, int len)\n{\n\tint j;\n\n\tif (p[0] != key[0])\n\t\treturn 0;\n" + SCANP +
          "\tif (j != len)\n\t\treturn 0;\n\tif (p[len] == 0)\n\t\treturn 0;\n\treturn 1;\n}\n\n", "keyAt(&buf[i], key, len)"),
    'B': ("static int keyAt(unsigned char *p, const char *key, int len)\n{\n\tint j;\n\n\tif (p[0] == key[0]) {\n" + SCANP.replace('\t', '\t\t').replace('\t\t\t\t\t\t', '\t\t\t\t') +
          "\t\tif (j == len && p[len] != 0)\n\t\t\treturn 1;\n\t}\n\treturn 0;\n}\n\n", "keyAt(&buf[i], key, len)"),
    'C': ("static int keyAt(unsigned char *buf, int i, const char *key, int len)\n{\n\tint j;\n\tunsigned char *p;\n\n\tif (buf[i] == key[0]) {\n\t\tp = &buf[i];\n" + SCANP.replace('\t', '\t\t').replace('\t\t\t\t\t\t', '\t\t\t\t') +
          "\t\tif (j == len) {\n\t\t\tunsigned char *q = &buf[i + len];\n\n\t\t\tif (*q != 0)\n\t\t\t\treturn 1;\n\t\t}\n\t}\n\treturn 0;\n}\n\n", "keyAt(buf, i, key, len)"),
    'D': ("static int keyAt(unsigned char *buf, int i, const char *key, int len)\n{\n\tint j;\n\tunsigned char *p;\n\tint ok = 0;\n\n\tif (buf[i] == key[0]) {\n\t\tp = &buf[i];\n" + SCANP.replace('\t', '\t\t').replace('\t\t\t\t\t\t', '\t\t\t\t') +
          "\t\tif (j == len) {\n\t\t\tunsigned char *q = &buf[i + len];\n\n\t\t\tif (*q != 0)\n\t\t\t\tok = 1;\n\t\t}\n\t}\n\treturn ok;\n}\n\n", "keyAt(buf, i, key, len)"),
}
for k, (h, call) in FORMS.items():
    for kk, ret in (('r', "\t\tif (%s)\n\t\t\treturn i + len;\n"), ('c', "\t\tif (!%s)\n\t\t\tcontinue;\n\t\treturn i + len;\n")):
        V[k + kk] = HEAD + "/* getters' own helper (not memFindStr) */\n" + h + "static int findKey(unsigned char *buf, const char *key)\n{\n\tint i, len;\n\n\tlen = strlen(key);\n\t" + LOOP + " {\n" + ret % call + "\t}\n\treturn -1;\n}\n" + TAIL

# flags in findKey itself: head flag h (same), match flag m, value flag v
SC = "\t\t\tp = &buf[i];\n\t\t\tfor (j = 0; j < len; j++)\n\t\t\t\tif (p[j] != key[j])\n\t\t\t\t\tj = len + 1;\n"
for h, m, v in itertools.product((0, 1), (0, 1), (0, 1)):
    b = "/* getters' own helper (not memFindStr) */\nstatic int findKey(unsigned char *buf, const char *key)\n{\n\tint i, j, len, ok;\n\tunsigned char *p;\n\n\tlen = strlen(key);\n\t" + LOOP + " {\n"
    if h:
        b += "\t\tok = 0;\n\t\tif (buf[i] == key[0])\n\t\t\tok = 1;\n\t\tif (ok) {\n"
    else:
        b += "\t\tif (buf[i] == key[0]) {\n"
    b += SC
    if m:
        b += "\t\t\tok = 0;\n\t\t\tif (j == len)\n\t\t\t\tok = 1;\n\t\t\tif (ok) {\n"
    else:
        b += "\t\t\tif (j == len) {\n"
    b += "\t\t\t\tunsigned char *q = &buf[i + len];\n\n"
    if v:
        b += "\t\t\t\tok = 0;\n\t\t\t\tif (*q != 0)\n\t\t\t\t\tok = 1;\n\t\t\t\tif (ok)\n\t\t\t\t\treturn i + len;\n"
    else:
        b += "\t\t\t\tif (*q != 0)\n\t\t\t\t\treturn i + len;\n"
    b += "\t\t\t}\n\t\t}\n\t}\n\treturn -1;\n}\n"
    V['flag%d%d%d' % (h, m, v)] = HEAD + b + TAIL
print(len(V))
if __name__ == '__main__':
    if len(sys.argv) > 1:
        open(F.os.path.join(F.A6, 'k9.c'), 'w', newline='\n').write(V[sys.argv[1]])
    else:
        F.run(V, 'k9', 20)
