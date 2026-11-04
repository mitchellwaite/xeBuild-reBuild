"""fl6k5.py: findKey with branch-prediction shapes instead of a dead test: continue (PRED_CONTINUE) and goto (PRED_GOTO) on the
mismatch paths.  The dead key == NULL acted by making a third loop exit (loop exit heuristic 91%/n_exits); `j <= len` by not
being EQ (opcode heuristic 28%).  Both put the tail's freq up against the entry's."""
import itertools, sys
import fllib as L, fl6lib as F

S = F.drop(F.S0, ['KF'])
A = S.index("/* getters' own helper (not memFindStr) */")
B = S.index("#define FIND findKey(xb.iniBuf, key)")
HEAD = S[:A]
TAIL = S[B:]
CM = {'bk': ('buf[i] == key[0]', 'buf[i] != key[0]'), 'kb': ('key[0] == buf[i]', 'key[0] != buf[i]')}
INNER = "for (j = 0; j < len; j++)\n\t\t\tif (p[j] != key[j])\n\t\t\t\tj = len + 1;\n"


def gen(h, jt, qt, cm, q):
    eq, ne = CM[cm]
    out = "/* getters' own helper (not memFindStr) */\nstatic int findKey(unsigned char *buf, const char *key)\n{\n\tint i, j, len;\n\tunsigned char *p;\n\tlen = strlen(key);\n"
    out += "\tfor (i = 0; i < xb.iniSize - len; i++) {\n"
    body = "p = &buf[i];\n" + INNER
    rd = '*q' if q else 'buf[i + len]'
    qdecl = "unsigned char *q = &buf[i + len];\n\n" if q else ''
    if qt == 'nest':
        tl = qdecl + "if (%s != 0)\n\treturn i + len;\n" % rd
    elif qt == 'cont':
        tl = qdecl + "if (%s == 0)\n\tcontinue;\nreturn i + len;\n" % rd
    else:
        tl = qdecl + "if (%s == 0)\n\tgoto next;\nreturn i + len;\n" % rd
    if jt == 'nest':
        body += "if (j == len) {\n" + indent(tl) + "}\n"
    elif jt == 'cont':
        body += "if (j != len)\n\tcontinue;\n" + ('{\n' + indent(tl) + '}\n' if q else tl)
    else:
        body += "if (j != len)\n\tgoto next;\n" + ('{\n' + indent(tl) + '}\n' if q else tl)
    if h == 'nest':
        out += "\t\tif (%s) {\n" % eq + indent(body, 3) + "\t\t}\n"
    elif h == 'cont':
        out += "\t\tif (%s)\n\t\t\tcontinue;\n" % ne + indent(body, 2)
    else:
        out += "\t\tif (%s)\n\t\t\tgoto next;\n" % ne + indent(body, 2)
    if 'goto next' in out:
        out += "next:\n\t\t;\n"
    out += "\t}\n\treturn -1;\n}\n"
    return HEAD + out + TAIL


def indent(t, n=1):
    return ''.join(('\t' * n + l if l.strip() else l) for l in t.splitlines(True))


V = {}
for h, jt, qt, cm, q in itertools.product(['nest', 'cont', 'goto'], ['nest', 'cont', 'goto'], ['nest', 'cont', 'goto'], CM, [1, 0]):
    V['%s,%s,%s,%s,%d' % (h, jt, qt, cm, q)] = gen(h, jt, qt, cm, q)
print(len(V))
if __name__ == '__main__':
    if len(sys.argv) > 1:
        open(F.os.path.join(F.A6, 'k5.c'), 'w', newline='\n').write(V[sys.argv[1]])
    else:
        F.run(V, 'k5', 25)
