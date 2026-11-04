"""fl6k.py: findKey with no dead test: out-parameter forms (`*off`, `**val`) and tails, with the getters adapted."""
import itertools, re, sys
import fllib as L, fl6lib as F

A = F.S0.index("/* getters' own helper (not memFindStr) */")
B = F.S0.index("/* load and pre-parse options.ini from the base dir")
TEMPLATE_HEAD = F.S0[:A]
TAILPART = F.S0[B:]

TAILS = {
    'qn': "\t\t\t\tunsigned char *q = &buf[i + len];\n\n\t\t\t\tif (*q != 0) {\n@RET@\t\t\t\t}\n",
    'nq': "\t\t\t\tif (buf[i + len] != 0) {\n@RET@\t\t\t\t}\n",
    'pn': "\t\t\t\tif (p[len] != 0) {\n@RET@\t\t\t\t}\n",
    'cont': "\t\t\t\tif (buf[i + len] == 0)\n\t\t\t\t\tcontinue;\n@RET@",
    'qcont': "\t\t\t\tunsigned char *q = &buf[i + len];\n\n\t\t\t\tif (*q == 0)\n\t\t\t\t\tcontinue;\n@RET@",
}
# nest: j == len tests nest; else `if (j == len && ...)`
RETS = {
    'off': ("static int findKey(unsigned char *buf, const char *key, int *off)", "\t\t\t\t\t*off = i + len;\n\t\t\t\t\treturn 1;\n", "return 0;"),
    'val': ("static int findKey(unsigned char *buf, const char *key, char **val)", "\t\t\t\t\t*val = (char *)&buf[i + len];\n\t\t\t\t\treturn 1;\n", "return 0;"),
    'offv': ("static void findKey(unsigned char *buf, const char *key, int *off)", "\t\t\t\t\t*off = i + len;\n\t\t\t\t\treturn;\n", "*off = -1;"),
    'off1': ("static int findKey(unsigned char *buf, const char *key, int *off)", "\t\t\t\t\t*off = i + len;\n\t\t\t\t\treturn i + len;\n", "return -1;"),
    'valv': ("static void findKey(unsigned char *buf, const char *key, char **val)", "\t\t\t\t\t*val = (char *)&buf[i + len];\n\t\t\t\t\treturn;\n", "*val = NULL;"),
    'rval': ("static char *findKey(unsigned char *buf, const char *key)", "\t\t\t\t\treturn (char *)&buf[i + len];\n", "return NULL;"),
    'plain': ("static int findKey(unsigned char *buf, const char *key)", "\t\t\t\t\treturn i + len;\n", "return -1;"),
}
CMP = {'bk': 'buf[i] == key[0]', 'kb': 'key[0] == buf[i]'}


def fk(ret, tail, cmp_, inner, sized):
    sig, r, end = RETS[ret]
    if sized:
        sig = sig.replace('(unsigned char *buf, ', '(unsigned char *buf, int size, ')
        lim = 'size - len'
    else:
        lim = 'xb.iniSize - len'
    t = TAILS[tail].replace('@RET@', r)
    ins = {'p': "\t\t\tp = &buf[i];\n\t\t\tfor (j = 0; j < len; j++)\n\t\t\t\tif (p[j] != key[j])\n\t\t\t\t\tj = len + 1;\n",
           'b': "\t\t\tfor (j = 0; j < len; j++)\n\t\t\t\tif (buf[i + j] != key[j])\n\t\t\t\t\tj = len + 1;\n"}[inner]
    if tail == 'pn':
        ins = ins if inner == 'p' else "\t\t\tp = &buf[i];\n" + ins
    return ("/* getters' own helper (not memFindStr) */\n" + sig + "\n{\n\tint i, j, len;\n\tunsigned char *p;\n\tlen = strlen(key);\n"
            "\tfor (i = 0; i < " + lim + "; i++) {\n\t\tif (" + CMP[cmp_] + ") {\n" + ins +
            "\t\t\tif (j == len) {\n" + t + "\t\t\t}\n\t\t}\n\t}\n\t" + end + "\n}\n"), sig


GET = F.S0[A:B]
GET = GET[GET.index('#define FIND'):]


def getters(ret, sized, cond):
    g = GET
    args = 'xb.iniBuf, xb.iniSize, key' if sized else 'xb.iniBuf, key'
    g = g.replace('#define FIND findKey(xb.iniBuf, key)\n', '')
    o = '\toff = FIND;\n\tif (off == -1)\n\t\treturn %s;\n'
    if ret in ('plain',):
        return g.replace('FIND', 'findKey(%s)' % args)
    if ret in ('off', 'off1'):
        tst = {'not': 'if (!findKey(%s, &off))', 'neg': 'if (findKey(%s, &off) == 0)' if ret == 'off' else 'if (findKey(%s, &off) == -1)'}[cond] % args
        if ret == 'off1' and cond == 'not':
            tst = 'if (findKey(%s, &off) < 0)' % args
        for d in ('def', 'NULL'):
            g = g.replace(o % d, '\t%s\n\t\treturn %s;\n' % (tst, d))
        return g
    if ret == 'offv':
        for d in ('def', 'NULL'):
            g = g.replace(o % d, '\tfindKey(%s, &off);\n\tif (off == -1)\n\t\treturn %s;\n' % (args, d))
        return g
    # val forms: val is the pointer, off goes
    g = g.replace('\tint off;\n\tchar *val;\n', '\tchar *val;\n')
    g = g.replace('\tint off;\n\tif (xb.iniSize == 0)\n\t\treturn def;\n\toff = FIND;\n\tif (off == -1)\n\t\treturn def;\n\treturn myatou32((char *)&xb.iniBuf[off], def);',
                  '\tchar *val;\n\tif (xb.iniSize == 0)\n\t\treturn def;\n\t@GET@\n\t\treturn def;\n\treturn myatou32(val, def);')
    g = g.replace('\tval = (char *)&xb.iniBuf[off];\n', '')
    if ret == 'val':
        c = 'if (!findKey(%s, &val))' % args
    elif ret == 'valv':
        c = 'findKey(%s, &val);\n\tif (val == NULL)' % args
    else:
        c = 'val = findKey(%s);\n\tif (val == NULL)' % args
    for d in ('def', 'NULL'):
        g = g.replace(o % d, '\t%s\n\t\treturn %s;\n' % (c, d))
    return g.replace('@GET@', c)


V = {}
for ret, tail, cmp_, inner, sized, cond in itertools.product(RETS, TAILS, CMP, 'pb', (0, 1), ('not', 'neg')):
    if cond == 'neg' and ret not in ('off', 'off1'):
        continue
    if tail == 'pn' and False:
        continue
    t, _ = fk(ret, tail, cmp_, inner, sized)
    s = TEMPLATE_HEAD + t + getters(ret, sized, cond) + '\n' + TAILPART
    V['%s,%s,%s,%s,%d,%s' % (ret, tail, cmp_, inner, sized, cond)] = s
print(len(V))
if __name__ == '__main__':
    if len(sys.argv) > 1:
        open(F.os.path.join(F.A6, 'k.c'), 'w', newline='\n').write(V[sys.argv[1]])
        o = L.compile(V[sys.argv[1]], None, 'a6k')
        print(L.score(o)[:4])
    else:
        F.run(V, 'k', 30)
