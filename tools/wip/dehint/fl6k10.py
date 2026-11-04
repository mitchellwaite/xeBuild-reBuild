"""fl6k10.py: matchAt's return encoding and test: each gives the tail a different probability (0-compare none, EQ 28, NE 72, >0 64, pointer 70)."""
import itertools, sys
import fllib as L, fl6lib as F

S = F.drop(F.S0, ['KF'])
A = S.index("/* getters' own helper (not memFindStr) */")
B = S.index("#define FIND findKey(xb.iniBuf, key)")
HEAD, TAIL = S[:A], S[B:]
SCAN = "\tfor (j = 0; j < len; j++)\n\t\tif (p[j] != key[j])\n\t\t\tj = len + 1;\n"
ENC = {
    '10': ('int', 'if (j == len)\n\t\treturn 1;\n\treturn 0;\n', {'t': 'x', 'ne0': 'x != 0', 'eq1': 'x == 1', 'gt0': 'x > 0', 'ge1': 'x >= 1', 'ne2': 'x != 2'}),
    '01': ('int', 'if (j == len)\n\t\treturn 0;\n\treturn 1;\n', {'not': '!x', 'eq0': 'x == 0', 'lt1': 'x < 1', 'le0': 'x <= 0', 'ne1': 'x != 1'}),
    '0m': ('int', 'if (j == len)\n\t\treturn 0;\n\treturn -1;\n', {'not': '!x', 'ge0': 'x >= 0', 'nem': 'x != -1', 'gtm': 'x > -1'}),
    'lm': ('int', 'if (j == len)\n\t\treturn len;\n\treturn -1;\n', {'ge0': 'x >= 0', 'nem': 'x != -1', 'gtm': 'x > -1'}),
    'p0': ('unsigned char *', 'if (j == len)\n\t\treturn &p[len];\n\treturn NULL;\n', {'t': 'x', 'nen': 'x != NULL'}),
    'p0b': ('unsigned char *', 'if (j != len)\n\t\treturn NULL;\n\treturn &p[len];\n', {'t': 'x', 'nen': 'x != NULL'}),
}
TL = {
    'q': "\t\t\t\tunsigned char *q = &buf[i + len];\n\n\t\t\t\tif (*q != 0)\n\t\t\t\t\treturn i + len;\n",
    'n': "\t\t\t\tif (buf[i + len] != 0)\n\t\t\t\t\treturn i + len;\n",
}
V = {}
for ek, (rt, ret, tests) in ENC.items():
    h = "static " + rt + (' ' if not rt.endswith('*') else '') + "matchAt(unsigned char *p, const char *key, int len)\n{\n\tint j;\n\n" + SCAN + "\t" + ret + "}\n\n"
    for tk, t in tests.items():
        for lk, tl in TL.items():
            for cm in ('buf[i] == key[0]', 'key[0] == buf[i]'):
                call = t.replace('x', 'matchAt(&buf[i], key, len)')
                b = ("/* getters' own helper (not memFindStr) */\n" + h + "static int findKey(unsigned char *buf, const char *key)\n{\n\tint i, len;\n\n\tlen = strlen(key);\n"
                     "\tfor (i = 0; i < xb.iniSize - len; i++) {\n\t\tif (" + cm + ") {\n\t\t\tif (" + call + ") {\n" + tl + "\t\t\t}\n\t\t}\n\t}\n\treturn -1;\n}\n")
                V['%s,%s,%s,%s' % (ek, tk, lk, cm[:3])] = HEAD + b + TAIL
print(len(V))
if __name__ == '__main__':
    if len(sys.argv) > 1:
        open(F.os.path.join(F.A6, 'k10.c'), 'w', newline='\n').write(V[sys.argv[1]])
    else:
        F.run(V, 'k10', 24)
