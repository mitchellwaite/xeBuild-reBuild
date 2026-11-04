"""fl7f.py: the natural guards the brief names: an empty key's early return, an end-of-buffer test on the first byte, a bounds check before the value's read,
each plain and with matchAt.  Do they fold, or do they emit code?"""
import itertools, sys
import fl7lib as K

SCAN = "\t\t\tp = &buf[i];\n\t\t\tfor (j = 0; j < len; j++)\n\t\t\t\tif (p[j] != key[j])\n\t\t\t\t\tj = len + 1;\n"
MATCHAT = "static int matchAt(unsigned char *p, const char *key, int len)\n{\n\tint j;\n\n\tfor (j = 0; j < len; j++)\n\t\tif (p[j] != key[j])\n\t\t\tj = len + 1;\n\tif (j == len)\n\t\treturn 1;\n\treturn 0;\n}\n\n"
VAL = "\t\t\t\tif (buf[i + len] != 0)\n\t\t\t\t\treturn i + len;\n"
G = {
    # (before the loop, at the head of the body, in the match arm before the value's read)
    'none': ('', '', ''),
    'len0': ('\tif (len == 0)\n\t\treturn -1;\n', '', ''),
    'lenle0': ('\tif (len <= 0)\n\t\treturn -1;\n', '', ''),
    'key0': ('\tif (key[0] == 0)\n\t\treturn -1;\n', '', ''),
    'lenlt0': ('\tif (len < 0)\n\t\treturn -1;\n', '', ''),
    'nulbrk': ('', '\t\tif (buf[i] == 0 && i + 1 >= xb.iniSize)\n\t\t\tbreak;\n', ''),
    'bound': ('', '', '\t\t\t\tif (i + len >= xb.iniSize)\n\t\t\t\t\tbreak;\n'),
    'boundr': ('', '', '\t\t\t\tif (i + len >= xb.iniSize)\n\t\t\t\t\treturn -1;\n'),
    'relim': ('', '', '\t\t\t\tif (i >= xb.iniSize - len)\n\t\t\t\t\tbreak;\n'),
    'lenarm': ('', '', '\t\t\t\tif (len == 0)\n\t\t\t\t\treturn -1;\n'),
    'lenarmb': ('', '', '\t\t\t\tif (len == 0)\n\t\t\t\t\tbreak;\n'),
}
V = {}
for (gk, (a, b, c)), hm in itertools.product(G.items(), (0, 1)):
    if hm:
        mid, cond, pre, decl = '', 'matchAt(&buf[i], key, len)', MATCHAT, '\tint i, len;\n'
    else:
        mid, cond, pre, decl = SCAN, 'j == len', '', '\tint i, j, len;\n\tunsigned char *p;\n'
    V['%s,%d' % (gk, hm)] = K.fk("/* getters' own helper (not memFindStr) */\n" + pre + "static int findKey(unsigned char *buf, const char *key)\n{\n" + decl + "\tlen = strlen(key);\n" + a +
                                  "\tfor (i = 0; i < xb.iniSize - len; i++) {\n" + b + "\t\tif (buf[i] == key[0]) {\n" + mid + "\t\t\tif (" + cond + ") {\n" + c + VAL + "\t\t\t}\n\t\t}\n\t}\n\treturn -1;\n}\n")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        K.diff(V[sys.argv[1]])
    else:
        K.run(V, 'f', 22)
