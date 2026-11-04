"""fl6k6.py: the getters through memFindStr's shape: a third/fourth loop exit that is live until the constant skipNul is folded.
Direct calls of memFindStr(xb.iniBuf, xb.iniSize, key, 0), and findKey with a skipNul parameter in memFindStr's tail form, with
findKey's own compare/p forms."""
import itertools, sys
import fllib as L, fl6lib as F

S = F.drop(F.S0, ['KF'])
A = S.index("/* getters' own helper (not memFindStr) */")
B = S.index("#define FIND findKey(xb.iniBuf, key)")
C = B + len("#define FIND findKey(xb.iniBuf, key)\n")
HEAD, TAIL = S[:A], S[C:]
V = {}
for call in ('memFindStr(xb.iniBuf, xb.iniSize, key, 0)',):
    V['direct'] = HEAD + '#define FIND ' + call + '\n' + TAIL
    # findIniKey too
    a = HEAD.index('/* offset of the value after `key` in buf, or -1 */')
    b = HEAD.index('/* the value after `key` in the loaded ini, or NULL */')
    h2 = HEAD[:a] + HEAD[b:]
    h2 = L.sub(h2, 'off = findIniKey(xb.iniBuf, xb.iniSize, key);', 'off = memFindStr(xb.iniBuf, xb.iniSize, key, 0);')
    V['directall'] = h2 + '#define FIND ' + call + '\n' + TAIL

CM = {'bk': 'buf[i] == key[0]', 'kb': 'key[0] == buf[i]'}
TLS = {
    # memFindStr's tail
    'mfs': "if (skipNul) {\n\tif (buf[i + len] == 0)\n\t\treturn i + len + 1;\n\treturn i + len;\n}\nif (buf[i + len] != 0)\n\treturn i + len;\n",
    # a shorter one: skipNul's arm returns once
    'one': "if (skipNul)\n\treturn i + len;\nif (buf[i + len] != 0)\n\treturn i + len;\n",
    'oneq': "if (skipNul)\n\treturn i + len + 1;\nif (buf[i + len] != 0)\n\treturn i + len;\n",
    'q': "unsigned char *q = &buf[i + len];\n\nif (skipNul)\n\treturn i + len;\nif (*q != 0)\n\treturn i + len;\n",
    'or': "if (skipNul || buf[i + len] != 0)\n\treturn i + len;\n",
    'neg': "if (buf[i + len] != 0)\n\treturn i + len;\nif (skipNul)\n\treturn i + len + 1;\n",
}
PS = {
    'p': ("p = &buf[i];\nfor (j = 0; j < len; j++)\n\tif (p[j] != key[j])\n\t\tj = len + 1;\n", 'unsigned char *p;\n\t'),
    'b': ("for (j = 0; j < len; j++)\n\tif (buf[i + j] != key[j])\n\t\tj = len + 1;\n", ''),
}


def ind(t, n):
    return ''.join('\t' * n + l for l in t.splitlines(True))


for (tk, tl), (pk, (pb, pd)), (ck, c), sized, skipval in itertools.product(TLS.items(), PS.items(), CM.items(), (0, 1), (0,)):
    sig = 'unsigned char *buf, int size, const char *key, int skipNul' if sized else 'unsigned char *buf, const char *key, int skipNul'
    lim = 'size - len' if sized else 'xb.iniSize - len'
    t = "/* getters' own helper (not memFindStr) */\nstatic int findKey(%s)\n{\n\tint i, j, len;\n\t%slen = strlen(key);\n\tfor (i = 0; i < %s; i++) {\n\t\tif (%s) {\n" % (sig, pd, lim, c)
    t += ind(pb, 3) + "\t\t\tif (j == len) {\n" + ind(tl, 4) + "\t\t\t}\n\t\t}\n\t}\n\treturn -1;\n}\n"
    call = 'findKey(xb.iniBuf, xb.iniSize, key, 0)' if sized else 'findKey(xb.iniBuf, key, 0)'
    V['%s,%s,%s,%d' % (tk, pk, ck, sized)] = HEAD + t + '#define FIND ' + call + '\n' + TAIL
print(len(V))
if __name__ == '__main__':
    if len(sys.argv) > 1:
        open(F.os.path.join(F.A6, 'k6.c'), 'w', newline='\n').write(V[sys.argv[1]])
        F.show = None
    else:
        F.run(V, 'k6', 25)
