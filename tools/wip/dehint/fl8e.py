"""fl8e.py: conversions around the head of parseIni and the helpers' arguments.  prot=gfs_u flips tie C alone and pre=u flips tie A alone,
so a signedness conversion before the first inlining moves single ties.  All are live and behave the same for any real file size.
  python fl8e.py single       one edit at each T subset
  python fl8e.py rand N [seed] random combinations of the edits that move something, at each T subset
Labels `drops|e=edit+edit`."""
import itertools, os, random, sys
import fllib as L, fl6lib as F, fl8lib as T
import fl8c, fl8d

ALL = {}
GF = "\tsize = getFileSize(f);\n\tbuf = malloc(size + 1);\n"
FR = "\tfread(buf, size, 1, f);\n"
DC = "(char *path)\n{\n\tFILE *f;\n"


def fsize(ty, cast='', mal=True, frd=True, assign=True):
    """the file's size in its own local until preParse"""
    def f(s):
        s = L.sub(s, DC, DC + "\t%s fsize;\n" % ty)
        s = L.sub(s, GF, "\tfsize = %sgetFileSize(f);\n\tbuf = malloc(%s + 1);\n" % (cast, 'fsize' if mal else 'size'))
        s = L.sub(s, FR, "\tfread(buf, %s, 1, f);\n" % ('fsize' if frd else 'size'))
        s = L.sub(s, "\tsize = preParse(buf, size);\n", "\tsize = preParse(buf, fsize);\n")
        return s
    return f


for ty in ('uint32_t', 'unsigned', 'size_t', 'long', 'off_t'):
    ALL['fs_' + ty] = fsize(ty)
ALL['fs_ca'] = lambda s: L.sub(s, GF, "\tsize = (uint32_t)getFileSize(f);\n\tbuf = malloc(size + 1);\n")
ALL['fs_mal'] = lambda s: L.sub(s, GF, "\tsize = getFileSize(f);\n\tbuf = malloc((uint32_t)size + 1);\n")
ALL['fs_fr'] = lambda s: L.sub(s, FR, "\tfread(buf, (size_t)size, 1, f);\n")
ALL['fs_fr1'] = lambda s: L.sub(s, FR, "\tfread(buf, 1, size, f);\n")

PRS = "static int preParse(unsigned char *buf, int size)"
for n, sig in [('u', "static int preParse(unsigned char *buf, uint32_t size)"),
               ('ui', "static int preParse(unsigned char *buf, unsigned size)"),
               ('st', "static int preParse(unsigned char *buf, size_t size)"),
               ('uu', "static uint32_t preParse(unsigned char *buf, uint32_t size)"),
               ('uuu', "static unsigned preParse(unsigned char *buf, unsigned size)"),
               ('ru', "static uint32_t preParse(unsigned char *buf, int size)"),
               ('l', "static long preParse(unsigned char *buf, long size)"),
               ('ch', "static int preParse(char *buf, int size)")]:
    ALL['pre_' + n] = (lambda sig: lambda s: L.sub(s, PRS, sig))(sig)
PB = "\tbuf[size] = 0xff;\n\tsize = iniPreParse(buf, size);\n\tbuf[size] = 0;\n\treturn size;\n"
ALL['pre_n'] = lambda s: L.sub(s, PB, "\tint n;\n\n\tbuf[size] = 0xff;\n\tn = iniPreParse(buf, size);\n\tbuf[n] = 0;\n\treturn n;\n")
ALL['pre_nu'] = lambda s: L.sub(L.sub(s, PRS, "static int preParse(unsigned char *buf, uint32_t size)"), PB, "\tint n;\n\n\tbuf[size] = 0xff;\n\tn = iniPreParse(buf, size);\n\tbuf[n] = 0;\n\treturn n;\n")

# iniPreParse's size as uint32_t in the prototype and definition (its own uses cast back)
# setupFiles
SF = "static void setupFiles(void)\n{\n\tint i;\n"
ALL['sf_u'] = lambda s: L.sub(L.sub(s, SF, "static void setupFiles(void)\n{\n\tlong i;\n"), "\t\tif (i >= xb.nFiles)\n", "\t\tif (i >= xb.nFiles)\n")
ALL['sf_n'] = lambda s: L.sub(L.sub(L.sub(s, SF, "static void setupFiles(int n)\n{\n\tint i;\n"), "\t\tif (i >= xb.nFiles)\n", "\t\tif (i >= n)\n"), "\tsetupFiles();\n", "\tsetupFiles(xb.nFiles);\n")

# findField's args
FFS = "static void findField(unsigned char *p, int rem, int *comma, int *nul)"
FCALL = "\t\t\tfindField(p, size - pos, &comma, &nul);\n"
FB = "\t*comma = memFindChar(p, ',', rem);\n\t*nul = memFindChar(p, 0, rem);\n"
ALL['ff_pos'] = lambda s: L.sub(L.sub(L.sub(s, FFS, "static void findField(unsigned char *buf, int size, int pos, int *comma, int *nul)"),
                                     FB, "\t*comma = memFindChar(&buf[pos], ',', size - pos);\n\t*nul = memFindChar(&buf[pos], 0, size - pos);\n"),
                               FCALL, "\t\t\tfindField(buf, size, pos, &comma, &nul);\n")
ALL['ff_u'] = lambda s: L.sub(s, FFS, "static void findField(unsigned char *p, uint32_t rem, int *comma, int *nul)")

# version section
VL = "\t\tlen = memFindChar(&buf[off], 0, sizeof(xb.kernelStr));\n"
ALL['ver_u'] = lambda s: L.sub(s, "\t\tif (len == -1)\n\t\t\tlen = sizeof(xb.kernelStr) - 1;\n", "\t\tif (len < 0)\n\t\t\tlen = sizeof(xb.kernelStr) - 1;\n")
ALL['ver_n'] = lambda s: L.sub(s, "\t\tstrncpy(xb.kernelStr, (char *)&buf[off], len);\n", "\t\tstrncpy(xb.kernelStr, (char *)buf + off, len);\n")

# moves known to shift ties
ALL['fwp'] = fl8d.ALL['fwp']
ALL['crcp2'] = fl8d.ALL['crcp2']
ALL['str0'] = fl8d.ALL['str0']
ALL['gfs_u'] = T.E if 0 else fl8c.E['prot']['gfs_u']
ALL['gfs_i'] = fl8c.E['prot']['gfs_ui']


class D(dict):
    def __missing__(self, k):
        def f(s):
            for e in k.split('+'):
                s = ALL[e](s)
            return s
        return f


T.E['e'] = D()


def single():
    V = {}
    for d in T.SUBS:
        V[d + '|'] = T.state(d + '|')
        for e in ALL:
            lb = '%s|e=%s' % (d, e)
            V[lb] = T.state(lb)
    rs = T.run(V, 'e_single', 8)
    T.floors(rs)
    sc = {r[3]: r[0] for r in rs}
    print('edit: ' + ' '.join(d or 'none' for d in T.SUBS))
    for e in sorted(ALL, key=lambda e: min(sc['%s|e=%s' % (d, e)] for d in T.SUBS)):
        print(e, ' '.join(str(sc['%s|e=%s' % (d, e)]) for d in T.SUBS))


def rand(N, seed=1):
    random.seed(seed)
    base = {}
    data = [l.rstrip('\n').split('\t') for l in open(os.path.join(T.A8, 'e_single.txt'))]
    for c in data:
        if c[3].endswith('|'):
            base[c[3][:-1]] = float(c[0])
    keep = sorted({c[3].split('=')[1] for c in data if '=' in c[3] and float(c[0]) != base[c[3].split('|')[0]] and float(c[0]) < 60})
    print(keep)
    excl = [{x for x in keep if x.startswith(p)} for p in ('fs_', 'pre_', 'gfs_')]
    V = {}
    tries = 0
    while len(V) < N and tries < N * 5:
        tries += 1
        k = random.choice([1, 2, 2, 3, 3, 4])
        c = random.sample(keep, min(k, len(keep)))
        if any(len(ex & set(c)) > 1 for ex in excl[:2]):
            continue
        if {'gfs_u', 'gfs_i'} <= set(c):
            continue
        d = random.choice(T.SUBS[1:])
        lb = '%s|e=%s' % (d, '+'.join(c))
        if lb in V:
            continue
        try:
            V[lb] = T.state(lb)
        except ValueError:
            pass
    print(len(V))
    rs = T.run(V, 'e_rand', 15)
    T.floors(rs)


if __name__ == '__main__':
    if sys.argv[1] == 'single':
        single()
    else:
        rand(int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 1)
