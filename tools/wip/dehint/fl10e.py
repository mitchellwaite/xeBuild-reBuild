"""fl10e.py [label]: findKey as a copy of memFindStr keeping its skipNul parameter, on current src, no dead test: tail forms x p/no-p x compare order x sized.
The arm is live in the function and only folded because every caller passes 0.  Label argument prints a diff."""
import itertools, sys, os, re
import fllib as L, fl10lib as F, fl10a as A

H0, T0 = F.HEAD, F.TAIL
TLS = {
    'mfs': "if (skipNul) {\n\tif (buf[i + len] == 0)\n\t\treturn i + len + 1;\n\treturn i + len;\n}\nif (buf[i + len] != 0)\n\treturn i + len;\n",
    'mfsq': "unsigned char *q = &buf[i + len];\n\nif (skipNul) {\n\tif (*q == 0)\n\t\treturn i + len + 1;\n\treturn i + len;\n}\nif (*q != 0)\n\treturn i + len;\n",
    'one': "if (skipNul)\n\treturn i + len;\nif (buf[i + len] != 0)\n\treturn i + len;\n",
    'oneq': "if (skipNul)\n\treturn i + len + 1;\nif (buf[i + len] != 0)\n\treturn i + len;\n",
    'q': "unsigned char *q = &buf[i + len];\n\nif (skipNul)\n\treturn i + len;\nif (*q != 0)\n\treturn i + len;\n",
    'q1': "unsigned char *q = &buf[i + len];\n\nif (skipNul)\n\treturn i + len + 1;\nif (*q != 0)\n\treturn i + len;\n",
    'q2': "unsigned char *q = &buf[i + len];\n\nif (*q != 0)\n\treturn i + len;\nif (skipNul)\n\treturn i + len + 1;\n",
    'neg': "if (buf[i + len] != 0)\n\treturn i + len;\nif (skipNul)\n\treturn i + len + 1;\n",
}
PS = {
    'p': ("p = &buf[i];\nfor (j = 0; j < len; j++)\n\tif (p[j] != key[j])\n\t\tj = len + 1;\n", 'unsigned char *p;\n\t'),
}
CM = {'bk': 'buf[i] == key[0]', 'kb': 'key[0] == buf[i]'}


def ind(t, n):
    return ''.join('\t' * n + l for l in t.splitlines(True))


def form(tl, pk, ck, sized, argv='0'):
    pb, pd = PS[pk]
    sig = 'unsigned char *buf, int size, const char *key, int skipNul' if sized else 'unsigned char *buf, const char *key, int skipNul'
    lim = 'size - len' if sized else 'xb.iniSize - len'
    t = "/* getters' own helper (not memFindStr) */\nstatic int findKey(%s)\n{\n\tint i, j, len;\n\t%slen = strlen(key);\n\tfor (i = 0; i < %s; i++) {\n\t\tif (%s) {\n" % (sig, pd, lim, CM[ck])
    t += ind(pb, 3) + "\t\t\tif (j == len) {\n" + ind(TLS[tl], 4) + "\t\t\t}\n\t\t}\n\t}\n\treturn -1;\n}\n"
    call = 'findKey(xb.iniBuf, xb.iniSize, key, %s)' % argv if sized else 'findKey(xb.iniBuf, key, %s)' % argv
    return H0 + t + '#define FIND ' + call + '\n' + T0[T0.index('\n', 0) + 1:]


V = {}
for tk, pk, ck, sized in itertools.product(TLS, PS, CM, (0, 1)):
    V['%s,%s,%s,%d' % (tk, pk, ck, sized)] = form(tk, pk, ck, sized)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        F.diff(V[sys.argv[1]])
        d = F.dumps(V[sys.argv[1]], 'e')
        for fn in A.GETTERS:
            print(fn, [b['freq'] for b in A.blocks(F.fn_part(d, 'optimized', fn))])
    else:
        print(len(V))
        F.run(V, 'e', show=32)
