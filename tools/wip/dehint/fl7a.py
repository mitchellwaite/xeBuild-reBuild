"""fl7a.py: findKey's control shape: found flags, break + test after the loop, per-position helpers returning off or -1, loop forms.
Everything live, no dead test.  Scores whole object lines."""
import itertools, sys
import fl7lib as K

CM = {'bk': 'buf[i] == key[0]', 'kb': 'key[0] == buf[i]'}
SCANP = "\t\t\tp = &buf[i];\n\t\t\tfor (j = 0; j < len; j++)\n\t\t\t\tif (p[j] != key[j])\n\t\t\t\t\tj = len + 1;\n"
SCANB = "\t\t\tfor (j = 0; j < len; j++)\n\t\t\t\tif (buf[i + j] != key[j])\n\t\t\t\t\tj = len + 1;\n"
LOOPS = {
    'for': "for (i = 0; i < xb.iniSize - len; i++)",
    'lim': "for (i = 0; i < lim; i++)",
}
V = {}


def fn(decl, body, pre=''):
    return K.fk("/* getters' own helper (not memFindStr) */\nstatic int findKey(unsigned char *buf, const char *key)\n{\n\tint i, j, len;\n\tunsigned char *p;\n" + decl + "\tlen = strlen(key);\n" + body + "}\n", pre)


for (ck, c), (sk, sc) in itertools.product(CM.items(), (('p', SCANP), ('b', SCANB))):
    head = "\tfor (i = 0; i < xb.iniSize - len; i++) {\n\t\tif (" + c + ") {\n" + sc
    tl = "\t\t}\n\t}\n"
    lab = ',' + ck + ',' + sk
    # break + test after the loop
    V['brk_test' + lab] = fn('', head + "\t\t\tif (j == len && buf[i + len] != 0)\n\t\t\t\tbreak;\n" + tl + "\tif (i < xb.iniSize - len)\n\t\treturn i + len;\n\treturn -1;\n")
    V['brk_test2' + lab] = fn('', head + "\t\t\tif (j == len) {\n\t\t\t\tif (buf[i + len] != 0)\n\t\t\t\t\tbreak;\n\t\t\t}\n" + tl + "\tif (i >= xb.iniSize - len)\n\t\treturn -1;\n\treturn i + len;\n")
    # off set + break
    V['off_brk' + lab] = fn('\tint off = -1;\n', head + "\t\t\tif (j == len) {\n\t\t\t\tif (buf[i + len] != 0) {\n\t\t\t\t\toff = i + len;\n\t\t\t\t\tbreak;\n\t\t\t\t}\n\t\t\t}\n" + tl + "\treturn off;\n")
    # flag in the head
    h2 = "\tfor (i = 0; !found && i < xb.iniSize - len; i++) {\n\t\tif (" + c + ") {\n" + sc
    V['found_head' + lab] = fn('\tint off = -1, found = 0;\n', h2 + "\t\t\tif (j == len) {\n\t\t\t\tif (buf[i + len] != 0) {\n\t\t\t\t\toff = i + len;\n\t\t\t\t\tfound = 1;\n\t\t\t\t}\n\t\t\t}\n" + tl + "\treturn off;\n")
    h3 = "\tfor (i = 0; off == -1 && i < xb.iniSize - len; i++) {\n\t\tif (" + c + ") {\n" + sc
    V['off_head' + lab] = fn('\tint off = -1;\n', h3 + "\t\t\tif (j == len) {\n\t\t\t\tif (buf[i + len] != 0)\n\t\t\t\t\toff = i + len;\n\t\t\t}\n" + tl + "\treturn off;\n")
    # author's idiom: end the loop by assigning the bound
    V['off_iend' + lab] = fn('\tint off = -1;\n', head + "\t\t\tif (j == len) {\n\t\t\t\tif (buf[i + len] != 0) {\n\t\t\t\t\toff = i + len;\n\t\t\t\t\ti = xb.iniSize;\n\t\t\t\t}\n\t\t\t}\n" + tl + "\treturn off;\n")
    # flag after the scan, tested in the loop
    V['found_brk' + lab] = fn('\tint found = 0;\n', head + "\t\t\tif (j == len) {\n\t\t\t\tif (buf[i + len] != 0)\n\t\t\t\t\tfound = 1;\n\t\t\t}\n\t\t\tif (found)\n\t\t\t\tbreak;\n" + tl + "\tif (found)\n\t\treturn i + len;\n\treturn -1;\n")
    V['found_after' + lab] = fn('\tint found = 0;\n', head + "\t\t\tif (j == len) {\n\t\t\t\tif (buf[i + len] != 0) {\n\t\t\t\t\tfound = 1;\n\t\t\t\t\tbreak;\n\t\t\t\t}\n\t\t\t}\n" + tl + "\tif (found)\n\t\treturn i + len;\n\treturn -1;\n")
    V['found_after0' + lab] = fn('\tint found = 0;\n', head + "\t\t\tif (j == len) {\n\t\t\t\tif (buf[i + len] != 0) {\n\t\t\t\t\tfound = 1;\n\t\t\t\t\tbreak;\n\t\t\t\t}\n\t\t\t}\n" + tl + "\tif (found == 0)\n\t\treturn -1;\n\treturn i + len;\n")
    # both: a return from the arm, and a flag for end-of-loop
    V['goto_found' + lab] = fn('', head + "\t\t\tif (j == len) {\n\t\t\t\tif (buf[i + len] != 0)\n\t\t\t\t\tgoto found;\n\t\t\t}\n" + tl + "\treturn -1;\nfound:\n\treturn i + len;\n")

# helpers per position
PH = {
    # offset or -1
    'keyAt': ("static int keyAt(unsigned char *buf, int i, const char *key, int len)\n{\n\tint j;\n\tunsigned char *p = &buf[i];\n\n\tfor (j = 0; j < len; j++)\n\t\tif (p[j] != key[j])\n\t\t\tj = len + 1;\n\tif (j == len && buf[i + len] != 0)\n\t\treturn i + len;\n\treturn -1;\n}\n\n",
              "\t\t\tint off = keyAt(buf, i, key, len);\n\n\t\t\tif (off != -1)\n\t\t\t\treturn off;\n"),
    'keyAtN': ("static int keyAt(unsigned char *buf, int i, const char *key, int len)\n{\n\tint j;\n\tunsigned char *p = &buf[i];\n\n\tfor (j = 0; j < len; j++)\n\t\tif (p[j] != key[j])\n\t\t\tj = len + 1;\n\tif (j == len) {\n\t\tif (buf[i + len] != 0)\n\t\t\treturn i + len;\n\t}\n\treturn -1;\n}\n\n",
               "\t\t\tint off = keyAt(buf, i, key, len);\n\n\t\t\tif (off >= 0)\n\t\t\t\treturn off;\n"),
    # match with a value test in the helper: 1 or 0
    'hasVal': ("static int hasVal(unsigned char *p, const char *key, int len)\n{\n\tint j;\n\n\tfor (j = 0; j < len; j++)\n\t\tif (p[j] != key[j])\n\t\t\tj = len + 1;\n\tif (j == len && p[len] != 0)\n\t\treturn 1;\n\treturn 0;\n}\n\n",
               "\t\t\tif (hasVal(&buf[i], key, len))\n\t\t\t\treturn i + len;\n"),
    'hasValN': ("static int hasVal(unsigned char *p, const char *key, int len)\n{\n\tint j;\n\n\tfor (j = 0; j < len; j++)\n\t\tif (p[j] != key[j])\n\t\t\tj = len + 1;\n\tif (j == len) {\n\t\tif (p[len] != 0)\n\t\t\treturn 1;\n\t}\n\treturn 0;\n}\n\n",
                "\t\t\tif (hasVal(&buf[i], key, len))\n\t\t\t\treturn i + len;\n"),
    # matchAt, as attempt 6
    'matchAt': ("static int matchAt(unsigned char *p, const char *key, int len)\n{\n\tint j;\n\n\tfor (j = 0; j < len; j++)\n\t\tif (p[j] != key[j])\n\t\t\tj = len + 1;\n\tif (j == len)\n\t\treturn 1;\n\treturn 0;\n}\n\n",
                "\t\t\tif (matchAt(&buf[i], key, len)) {\n\t\t\t\tif (buf[i + len] != 0)\n\t\t\t\t\treturn i + len;\n\t\t\t}\n"),
    'matchq': ("static int matchAt(unsigned char *p, const char *key, int len)\n{\n\tint j;\n\n\tfor (j = 0; j < len; j++)\n\t\tif (p[j] != key[j])\n\t\t\tj = len + 1;\n\tif (j == len)\n\t\treturn 1;\n\treturn 0;\n}\n\n",
               "\t\t\tif (matchAt(&buf[i], key, len)) {\n\t\t\t\tunsigned char *q = &buf[i + len];\n\n\t\t\t\tif (*q != 0)\n\t\t\t\t\treturn i + len;\n\t\t\t}\n"),
    # match and head in the helper
    'matchfull': ("static int matchAt(unsigned char *p, const char *key, int len)\n{\n\tint j;\n\n\tif (*p != key[0])\n\t\treturn 0;\n\tfor (j = 0; j < len; j++)\n\t\tif (p[j] != key[j])\n\t\t\tj = len + 1;\n\tif (j == len)\n\t\treturn 1;\n\treturn 0;\n}\n\n", None),
}
for (ck, c), (h, (pre, b)) in itertools.product(CM.items(), PH.items()):
    decl = "\tint i, len;\n"
    if b is None:
        body = "\tfor (i = 0; i < xb.iniSize - len; i++) {\n\t\tif (matchAt(&buf[i], key, len)) {\n\t\t\tif (buf[i + len] != 0)\n\t\t\t\treturn i + len;\n\t\t}\n\t}\n\treturn -1;\n"
    else:
        body = "\tfor (i = 0; i < xb.iniSize - len; i++) {\n\t\tif (" + c + ") {\n" + b + "\t\t}\n\t}\n\treturn -1;\n"
    V['%s,%s' % (h, ck)] = K.fk("/* getters' own helper (not memFindStr) */\n" + pre + "static int findKey(unsigned char *buf, const char *key)\n{\n" + decl + "\tlen = strlen(key);\n" + body + "}\n")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        K.diff(V[sys.argv[1]])
    else:
        print(len(V))
        K.run(V, 'a')
