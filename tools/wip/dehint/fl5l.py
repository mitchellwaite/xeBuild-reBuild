"""fl5l.py: findKey with no test, forms in product: head (nested / continue / ), p local, loop form, tails, compare order, limit, getters plain or iniVal."""
import itertools, sys
_av = sys.argv
sys.argv = _av[:1]
import fllib as L, fl5lib as F
exec(open(__file__.replace('fl5l', 'fl5k')).read().split("\nV = {}\n")[0])

HEADS = {
    'nest': ('\t\tif (CMP) {\n', '\t\t}\n'),
    'cont': ('\t\tif (NCMP)\n\t\t\tcontinue;\n\t\t{\n', '\t\t}\n'),
}
PS = {
    'p': ('\t\t\tp = &buf[i];\n', 'p[j]', 'unsigned char *p;\n'),
    'pscope': ('\t\t\tunsigned char *p = &buf[i];\n\n', 'p[j]', ''),
    'none': ('', 'buf[i + j]', ''),
}
JL = {
    'set': '\t\t\tfor (j = 0; j < len; j++)\n\t\t\t\tif (X != key[j])\n\t\t\t\t\tj = len + 1;\n',
    'brk': '\t\t\tfor (j = 0; j < len; j++)\n\t\t\t\tif (X != key[j])\n\t\t\t\t\tbreak;\n',
}
TL = {
    'q': '\t\t\tif (j == len) {\n\t\t\t\tunsigned char *q = &buf[i + len];\n\n\t\t\t\tif (*q != 0)\n\t\t\t\t\treturn i + len;\n\t\t\t}\n',
    'b': '\t\t\tif (j == len) {\n\t\t\t\tif (buf[i + len] != 0)\n\t\t\t\t\treturn i + len;\n\t\t\t}\n',
    'and': '\t\t\tif (j == len && buf[i + len] != 0)\n\t\t\t\treturn i + len;\n',
    'c': '\t\t\tif (j == len) {\n\t\t\t\tif (buf[i + len] == 0)\n\t\t\t\t\tcontinue;\n\t\t\t\treturn i + len;\n\t\t\t}\n',
    'cq': '\t\t\tif (j == len) {\n\t\t\t\tunsigned char *q = &buf[i + len];\n\n\t\t\t\tif (*q == 0)\n\t\t\t\t\tcontinue;\n\t\t\t\treturn i + len;\n\t\t\t}\n',
    'nj': '\t\t\tif (j != len)\n\t\t\t\tcontinue;\n\t\t\tif (buf[i + len] != 0)\n\t\t\t\treturn i + len;\n',
    'nj2': '\t\t\tif (j != len)\n\t\t\t\tcontinue;\n\t\t\tif (buf[i + len] == 0)\n\t\t\t\tcontinue;\n\t\t\treturn i + len;\n',
    'or': '\t\t\tif (j != len || buf[i + len] == 0)\n\t\t\t\tcontinue;\n\t\t\treturn i + len;\n',
    'qo': '\t\t\tif (j == len) {\n\t\t\t\tchar *q = (char *)buf + i + len;\n\n\t\t\t\tif (*q)\n\t\t\t\t\treturn i + len;\n\t\t\t}\n',
    'ch': '\t\t\tif (j == len) {\n\t\t\t\tunsigned char c = buf[i + len];\n\n\t\t\t\tif (c != 0)\n\t\t\t\t\treturn i + len;\n\t\t\t}\n',
    'off': '\t\t\tif (j == len) {\n\t\t\t\tint off = i + len;\n\n\t\t\t\tif (buf[off] != 0)\n\t\t\t\t\treturn off;\n\t\t\t}\n',
    'offc': '\t\t\tif (j == len) {\n\t\t\t\tint off = i + len;\n\n\t\t\t\tif (buf[off] == 0)\n\t\t\t\t\tcontinue;\n\t\t\t\treturn off;\n\t\t\t}\n',
    'ret': '\t\t\tif (j == len) {\n\t\t\t\tif (buf[i + len] != 0) {\n\t\t\t\t\tret = i + len;\n\t\t\t\t\tbreak;\n\t\t\t\t}\n\t\t\t}\n',
}
LP = {
    'for': '\tfor (i = 0; i < xb.iniSize - len; i++) {\n',
    'first': '\tfor (i = 0; ; i++) {\n\t\tif (i >= xb.iniSize - len)\n\t\t\tbreak;\n',
}
CM = {'bk': ('buf[i] == key[0]', 'buf[i] != key[0]'), 'kb': ('key[0] == buf[i]', 'key[0] != buf[i]')}


def fk(head, ps, jl, tl, lp, cm):
    h, e = HEADS[head]
    a1, x, d = PS[ps]
    c, n = CM[cm]
    h = h.replace('NCMP', n).replace('CMP', c)
    r = ''
    ret0 = '-1'
    decl = '\tint i, j, len;\n'
    if tl == 'ret':
        decl = '\tint i, j, len, ret = -1;\n'
        ret0 = 'ret'
    s = 'static int findKey(unsigned char *buf, const char *key)\n{\n' + decl
    if d:
        s += '\t' + d
    s += '\tlen = strlen(key);\n' + LP[lp] + h + a1 + JL[jl].replace('X', x) + TL[tl] + e + '\t}\n\treturn %s;\n}\n' % ret0
    return s


if __name__ == '__main__':
    V = {}
    for c in itertools.product(HEADS, PS, JL, TL, LP, CM, GETS_F):
        if c[2] == 'brk' and c[3] not in ('q', 'b', 'c'):
            continue
        V['/'.join(c)] = B[:a] + fk(*c[:6]) + GETS_F[c[6]] + '\n' + B[b:]
    print(len(V))
    F.run(V, 'l', show=30)
