"""fl6k2.py: findKey with the iniSize check moved in (live, not dead): the getters lose theirs."""
import itertools, sys
import fllib as L, fl6lib as F

S = F.drop(F.S0, ['KF'])
A = S.index("/* getters' own helper (not memFindStr) */")
B = S.index("/* load and pre-parse options.ini from the base dir")
H, G, T = S[:A], S[A:B], S[B:]
LEN = "\tlen = strlen(key);\n\tfor (i = 0; i < xb.iniSize - len; i++) {\n"
assert LEN in G
QT = "\t\t\t\tunsigned char *q = &buf[i + len];\n\n\t\t\t\tif (*q != 0)\n\t\t\t\t\treturn i + len;\n"
assert QT in G
CHK = {'def': '\tif (xb.iniSize == 0)\n\t\treturn def;\n', 'NULL': '\tif (xb.iniSize == 0)\n\t\treturn NULL;\n'}

V = {}
TL = {'q': QT, 'c': "\t\t\t\tif (buf[i + len] == 0)\n\t\t\t\t\tcontinue;\n\t\t\t\treturn i + len;\n", 'n': "\t\t\t\tif (buf[i + len] != 0)\n\t\t\t\t\treturn i + len;\n"}
CM = {'bk': 'buf[i] == key[0]', 'kb': 'key[0] == buf[i]'}
for head, tl, cm, keep in itertools.product(['before', 'after', 'none'], TL, CM, ['none', 'all', 'u32', 'bool']):
    g = G
    if head == 'before':
        g = L.sub(g, "\tlen = strlen(key);\n", "\tif (xb.iniSize == 0)\n\t\treturn -1;\n\tlen = strlen(key);\n")
    elif head == 'after':
        g = L.sub(g, "\tlen = strlen(key);\n", "\tlen = strlen(key);\n\tif (xb.iniSize == 0)\n\t\treturn -1;\n")
    g = L.sub(g, QT, TL[tl])
    g = L.sub(g, 'if (buf[i] == key[0])', 'if (%s)' % CM[cm])
    # which getters keep their own check
    parts = g.split('#define FIND findKey(xb.iniBuf, key)\n')
    q = parts[1]
    fns = {'getIniBool': 'bool', 'iniBoolInvalid': 'bool', 'getIniU32': 'u32', 'iniU32Invalid': 'u32'}
    for fn, cls in fns.items():
        if keep == 'all' or keep == cls:
            continue
        i = q.index(fn + '(')
        j = q.index('FIND', i)
        seg = q[i:j]
        for c in CHK.values():
            seg = seg.replace(c, '')
        q = q[:i] + seg + q[j:]
    if head == 'none' and keep != 'all':
        continue
    V['%s,%s,%s,%s' % (head, tl, cm, keep)] = H + parts[0] + '#define FIND findKey(xb.iniBuf, key)\n' + q + T
print(len(V))
if __name__ == '__main__':
    if len(sys.argv) > 1:
        open(F.os.path.join(F.A6, 'k2.c'), 'w', newline='\n').write(V[sys.argv[1]])
        o = L.compile(V[sys.argv[1]], None, 'a6k2')
        print(L.score(o)[:4])
    else:
        F.run(V, 'k2', 16)
