"""fl8c.py: signatures of the local helpers, and buf/p's pointer types.
  python fl8c.py mc | ms | ptr | prot | ff   (each at the subsets of T1-T3 in DROPS)
Axes are added to fl8lib.E, so labels work with `python fl8lib.py <label>`."""
import itertools, sys
import fllib as L, fl8lib as T

DROPS = ['', 'T1,T3', 'T1,T2,T3', 'T1', 'T3']
E = T.E

MCD = "int memFindChar(unsigned char *buf, char c, int size);\n"
MCF = "int memFindChar(unsigned char *buf, char c, int size)\n{"
MSD = "int memFindStr(unsigned char *buf, int size, const char *key, int label);\n"
MSF = "int memFindStr(unsigned char *buf, int size, const char *str, int skipNul)\n{"


def mc(buf, c, size, ret):
    def f(s):
        sig = "%s memFindChar(%s buf, %s c, %s size)" % (ret, buf, c, size)
        s = L.sub(s, MCD, sig + ";\n")
        return L.sub(s, MCF, sig + "\n{")
    return f


def ms(buf, size, st, skip, ret):
    def f(s):
        s = L.sub(s, MSD, "%s memFindStr(%s buf, %s size, %s str, %s skipNul);\n" % (ret, buf, size, st, skip))
        return L.sub(s, MSF, "%s memFindStr(%s buf, %s size, %s str, %s skipNul)\n{" % (ret, buf, size, st, skip))
    return f


def key(*a):
    return '_'.join(x.replace(' ', '').replace('*', 'P') for x in a)


E['mc'] = {}
for a in itertools.product(['unsigned char *', 'const unsigned char *', 'char *', 'const char *'], ['char', 'int', 'unsigned char'], ['int', 'long'], ['int', 'long']):
    E['mc'][key(*a)] = mc(*a)
E['ms'] = {}
for a in itertools.product(['unsigned char *', 'const unsigned char *', 'char *', 'const char *'], ['int', 'long'], ['const char *', 'char *', 'const unsigned char *', 'unsigned char *'], ['int', 'long', 'char'], ['int', 'long']):
    E['ms'][key(*a)] = ms(*a)

# pointers: all of parseIni's buf and p as char *.  buf[0] == 0xff has to keep its meaning
PA, PB = "uint32_t parseIni(char *path)\n{", "/* offset of the value after `key` in buf, or -1 */"


def body(s, fn):
    i, j = s.index(PA), s.index(PB)
    return s[:i] + fn(s[i:j]) + s[j:]


def uncast(t):
    return t.replace('(char *)p', 'p').replace('(char *)&buf[', '&buf[')


def ptr(bufty, pty, ff=None, cmpf="(unsigned char)buf[0] == 0xff || (unsigned char)buf[1] == 0xff"):
    def g(t):
        t = L.sub(t, "\tunsigned char *buf, *p;\n", "\t%s*buf;\n\t%s*p;\n" % (bufty, pty))
        if bufty.startswith('char'):
            t = L.sub(t, "buf[0] == 0xff || buf[1] == 0xff", cmpf)
        return uncast(t)

    def f(s):
        s = body(s, g)
        if pty.startswith('char'):
            s = L.sub(s, "static void findField(unsigned char *p,", "static void findField(char *p,")
        return s
    return f


E['ptr'] = {
    'bc': ptr('char ', 'char '),
    'bc2': ptr('char ', 'char ', cmpf="buf[0] == (char)0xff || buf[1] == (char)0xff"),
    'bc3': ptr('char ', 'char ', cmpf="buf[0] == -1 || buf[1] == -1"),
    'pc': ptr('unsigned char ', 'char '),
    'bonly': ptr('char ', 'unsigned char '),
    'void': lambda s: body(s, lambda t: L.sub(uncast(t), "\tunsigned char *buf, *p;\n", "\tunsigned char *buf;\n\tvoid *p;\n")),
}

# prototypes as seen from this file (header copies would be needed to land these)
INC = '#include "fileutil.h"\n'


def proto(name, decl):
    def f(s):
        return L.sub(s, INC, '#define %s %s_hdr\n%s#undef %s\n%s;\n' % (name, name, INC, name, decl))
    return f


E['prot'] = {
    'gfs_int': proto('getFileSize', 'int getFileSize(FILE *f)'),
    'gfs_u': proto('getFileSize', 'uint32_t getFileSize(FILE *f)'),
    'gfs_ui': proto('getFileSize', 'unsigned getFileSize(FILE *f)'),
    'x_u': proto('myatox32', 'unsigned myatox32(const char *dat, uint32_t defValue)'),
    'x_l': proto('myatox32', 'unsigned long myatox32(const char *dat, unsigned long defValue)'),
    'x_i': proto('myatox32', 'int myatox32(const char *dat, int defValue)'),
    'u_u': proto('myatou32', 'unsigned myatou32(const char *dat, unsigned defValue)'),
    'u_i': proto('myatou32', 'int myatou32(const char *dat, int defValue)'),
    'u_l': proto('myatou32', 'long myatou32(const char *dat, long defValue)'),
}
PP = "int iniPreParse(unsigned char *buf, int size);\n"
PPF = "int iniPreParse(unsigned char *buf, int size)\n{"
FFS = "static void findField(unsigned char *p, int rem, int *comma, int *nul)"
PRS = "static int preParse(unsigned char *buf, int size)"


def rs(old, new):
    return lambda s: L.sub(s, old, new)


E['ff'] = {
    'cu': rs(FFS, "static void findField(const unsigned char *p, int rem, int *comma, int *nul)"),
    'cc': rs(FFS, "static void findField(char *p, int rem, int *comma, int *nul)"),
    'rl': rs(FFS, "static void findField(unsigned char *p, long rem, int *comma, int *nul)"),
    'ru': rs(FFS, "static void findField(unsigned char *p, unsigned rem, int *comma, int *nul)"),
    'ret': lambda s: L.sub(L.sub(s, FFS, "static int findField(unsigned char *p, int rem, int *comma, int *nul)"), "\t*nul = memFindChar(p, 0, rem);\n}", "\t*nul = memFindChar(p, 0, rem);\n\treturn *comma;\n}"),
}
E['pre'] = {
    'void': lambda s: L.sub(L.sub(s, PRS, "static int preParse(void *ptr, int size)"), "\tbuf[size] = 0xff;\n\tsize = iniPreParse(buf, size);", "\tunsigned char *buf = ptr;\n\n\tbuf[size] = 0xff;\n\tsize = iniPreParse(buf, size);"),
    'l': rs(PRS, "static long preParse(unsigned char *buf, long size)"),
    'u': rs(PRS, "static int preParse(unsigned char *buf, uint32_t size)"),
    'vr': lambda s: L.sub(L.sub(L.sub(s, PRS, "static void preParse(unsigned char *buf, int *size)"), "\tbuf[size] = 0xff;\n\tsize = iniPreParse(buf, size);\n\tbuf[size] = 0;\n\treturn size;\n", "\tbuf[*size] = 0xff;\n\t*size = iniPreParse(buf, *size);\n\tbuf[*size] = 0;\n"), "size = preParse(buf, size);", "preParse(buf, &size);"),
}


def sweep(axis):
    V = {}
    for d in DROPS:
        V[d + '|'] = T.state(d + '|')
        for v in E[axis]:
            lb = '%s|%s=%s' % (d, axis, v)
            V[lb] = T.state(lb)
    rs_ = T.run(V, 'c_' + axis, 12)
    T.floors(rs_)
    sc = {r[3]: r[0] for r in rs_}
    seen = []
    for v in E[axis]:
        seen.append((min(sc['%s|%s=%s' % (d, axis, v)] for d in DROPS), sc['|%s=%s' % (axis, v)], sc['T1,T3|%s=%s' % (axis, v)], sc['T1,T2,T3|%s=%s' % (axis, v)], v))
    seen.sort()
    print('value: none, T1,T3, T1,T2,T3')
    for x in seen[:40]:
        print(x[4], x[1], x[2], x[3])


if __name__ == '__main__':
    for a in sys.argv[1:]:
        print('=====', a)
        sweep(a)
