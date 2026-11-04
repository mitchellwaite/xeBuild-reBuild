"""fl8h.py: the authors' DashLaunch habit (tmp/dashlaunch/iniparse.c): char * buffers read as `(x[i]&0xFF)`, and `(name[0]&0xFF)`.  Masks on the unsigned side keep behaviour with buf as char *,
in memFindChar, memFindStr, findKey and parseIni, and the getters.
  python fl8h.py single      each at T subsets and KF
Labels `drops|h=edit+edit`."""
import itertools, os, random, sys
import fllib as L, fl6lib as F, fl8lib as T

ALL = {}


def fnbody(start, end):
    def w(fn):
        def f(s):
            i = s.index(start)
            j = s.index(end, i)
            return s[:i] + fn(s[i:j]) + s[j:]
        return f
    return w


MC = fnbody("int memFindChar(unsigned char *buf, char c, int size)\n{", "void checkFileCase(void)\n{")
MS = fnbody("int memFindStr(unsigned char *buf, int size, const char *str, int skipNul)\n{", "int memFindChar(unsigned char *buf, char c, int size)\n{")
FK = fnbody("static int findKey(unsigned char *buf, const char *key)\n{", "#define FIND findKey")
PI = fnbody("uint32_t parseIni(char *path)\n{", "/* offset of the value after `key`")
PP = fnbody("int iniPreParse(unsigned char *buf, int size)\n{", "int memFindStr(unsigned char *buf, int size, const char *key, int label);")
U32 = fnbody("char *iniU32Invalid(const char *key)\n{", "/* load and pre-parse options.ini")

ALL['mc_m'] = MC(lambda t: L.sub(t, "if (buf[i] == c)", "if ((buf[i]&0xFF) == c)"))
ALL['mc_cm'] = lambda s: L.sub(L.sub(L.sub(s, "int memFindChar(unsigned char *buf, char c, int size);\n", "int memFindChar(char *buf, char c, int size);\n"), "int memFindChar(unsigned char *buf, char c, int size)\n{", "int memFindChar(char *buf, char c, int size)\n{"), "if (buf[i] == c)", "if ((buf[i]&0xFF) == c)")
ALL['mc_u'] = lambda s: L.sub(s, "if (buf[i] == c)", "if ((unsigned char)buf[i] == c)")


def ms(t, a):
    t = L.sub(t, "if (str[0] == buf[i]) {", {"m": "if (str[0] == (buf[i]&0xFF)) {", "n": "if (str[0] == buf[i]) {"}[a[0]])
    t = L.sub(t, "if (buf[i + j] != str[j])", {"m": "if ((buf[i + j]&0xFF) != str[j])", "n": "if (buf[i + j] != str[j])"}[a[1]])
    t = t.replace("if (buf[i + len] == 0)", {"m": "if ((buf[i + len]&0xFF) == 0)", "n": "if (buf[i + len] == 0)"}[a[2]])
    t = t.replace("if (buf[i + len] != 0)", {"m": "if ((buf[i + len]&0xFF) != 0)", "n": "if (buf[i + len] != 0)"}[a[2]])
    return t


for a in ('mmm', 'mnn', 'nmn', 'nnm'):
    ALL['ms_' + a] = MS((lambda a: lambda t: ms(t, a))(a))


def fk(t, a):
    if a[0] == 'm':
        t = L.sub(t, "if (buf[i] == key[0])", "if ((buf[i]&0xFF) == key[0])")
    if a[1] == 'm':
        t = L.sub(t, "if (p[j] != key[j])", "if ((p[j]&0xFF) != key[j])")
    if a[2] == 'm':
        t = L.sub(t, "if (*q != 0)", "if ((*q&0xFF) != 0)")
    if a[2] == 'b':
        t = L.sub(t, "unsigned char *q = &buf[i + len];\n\n", "").replace("if (*q != 0)", "if ((buf[i + len]&0xFF) != 0)")
    return t


for a in ('mmm', 'mnn', 'nmn', 'nnm', 'nnb', 'mmb'):
    ALL['fk_' + a] = FK((lambda a: lambda t: fk(t, a))(a))
# the getters
ALL['u32_m'] = U32(lambda t: L.sub(t, "if (val[0] == '0' && myatol(val[1]) == 'x') {", "if ((val[0]&0xFF) == '0' && myatol(val[1]&0xFF) == 'x') {"))
ALL['u32_m0'] = U32(lambda t: L.sub(t, "if (val[0] == '0' && myatol(val[1]) == 'x') {", "if ((val[0]&0xFF) == '0' && myatol(val[1]) == 'x') {"))
ALL['u32_m1'] = U32(lambda t: L.sub(t, "if (val[0] == '0' && myatol(val[1]) == 'x') {", "if (val[0] == '0' && myatol(val[1]&0xFF) == 'x') {"))
ALL['u32_mx'] = U32(lambda t: L.sub(t, "if (val[0] == '0' && myatol(val[1]) == 'x') {", "if (val[0] == '0' && (myatol(val[1])&0xFF) == 'x') {"))
# parseIni, buf as char *
PI0 = "\tunsigned char *buf, *p;\n"


def picast(t):
    return t.replace('(char *)p', 'p').replace('(char *)&buf[', '&buf[')


def pi_c(t):
    t = L.sub(t, PI0, "\tchar *buf, *p;\n")
    t = L.sub(t, "buf[0] == 0xff || buf[1] == 0xff", "(buf[0]&0xFF) == 0xFF || (buf[1]&0xFF) == 0xFF")
    return picast(t)


ALL['pi_c'] = lambda s: L.sub(PI(pi_c)(s), "static void findField(unsigned char *p,", "static void findField(char *p,")
ALL['pi_m'] = PI(lambda t: L.sub(t, "buf[0] == 0xff || buf[1] == 0xff", "(buf[0]&0xFF) == 0xFF || (buf[1]&0xFF) == 0xFF"))
ALL['pi_l'] = PI(lambda t: t.replace("xb.firmware[i][len - 1] == '1' || xb.firmware[i][len - 1] == '2'", "(xb.firmware[i][len - 1]&0xFF) == '1' || (xb.firmware[i][len - 1]&0xFF) == '2'"))
ALL['pi_x'] = PI(lambda t: L.sub(t, "if (xb.blSuffix[0])\n\t\tsprintf(label,", "if ((xb.blSuffix[0]&0xFF) != 0)\n\t\tsprintf(label,"))
ALL['pp_m'] = PP(lambda t: t.replace("buf[i] == ';'", "(buf[i]&0xFF) == ';'").replace("buf[i] == ' '", "(buf[i]&0xFF) == ' '"))


class D(dict):
    def __missing__(self, k):
        def f(s):
            for e in k.split('+'):
                s = ALL[e](s)
            return s
        return f


T.E['h'] = D()
DROPS = T.SUBS + ['KF', 'T1,T3,KF', 'T1,T2,T3,KF']


def single():
    V = {}
    for d in DROPS:
        V[d + '|'] = T.state(d + '|')
        for e in ALL:
            lb = '%s|h=%s' % (d, e)
            V[lb] = T.state(lb)
    rs = T.run(V, 'h_single', 8)
    T.floors(rs)
    sc = {r[3]: r[0] for r in rs}
    print('edit: ' + ' '.join(d or 'none' for d in DROPS))
    for e in sorted(ALL, key=lambda e: min(sc['%s|h=%s' % (d, e)] for d in DROPS)):
        print(e, ' '.join(str(sc['%s|h=%s' % (d, e)]) for d in DROPS))


if __name__ == '__main__':
    if True:
        single()
