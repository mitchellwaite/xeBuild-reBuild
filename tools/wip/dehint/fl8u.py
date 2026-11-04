"""fl8u.py: flag-free and flag-first forms of the name,crc split in bl, flashfs and security.  At T1,T3 raw's nul takes dom3's 7th pop (one low number, 361), and one PHI more or fewer
in the threaded paths before it fixes tie B: bl's len/noCrc give 5 of those.
  python fl8u.py single
Labels `drops|u=edit+edit`."""
import itertools, os, random, sys
import fllib as L, fl6lib as F, fl8lib as T

ALL = {}


def sect(name, old, new, count=1):
    a, b = F.SECS[name]

    def f(s):
        i, j = s.index(a), s.index(b)
        return s[:i] + L.sub(s[i:j], old, new, count) + s[j:]
    return f


def chain(*fs):
    def f(s):
        for g in fs:
            s = g(s)
        return s
    return f


BL = "\t\t\tlen = comma;\n\t\t\tnoCrc = 0;\n\t\t\tif (comma > nul) {\n\t\t\t\tlen = nul;\n\t\t\t\tnoCrc = 1;\n\t\t\t}\n"
BLF = "\t\t\tif (!noCrc) {\n"
BLH = {
    'q': "\t\t\tnoCrc = comma > nul;\n\t\t\tlen = noCrc ? nul : comma;\n",
    'r': "\t\t\tnoCrc = comma > nul;\n\t\t\tif (noCrc)\n\t\t\t\tlen = nul;\n\t\t\telse\n\t\t\t\tlen = comma;\n",
    's': "\t\t\tnoCrc = 0;\n\t\t\tif (comma > nul)\n\t\t\t\tnoCrc = 1;\n\t\t\tlen = comma;\n\t\t\tif (noCrc)\n\t\t\t\tlen = nul;\n",
    't': "\t\t\tlen = comma > nul ? nul : comma;\n\t\t\tnoCrc = comma > nul;\n",
    'u': "\t\t\tlen = comma < nul ? comma : nul;\n\t\t\tnoCrc = comma > nul;\n",
    'v': "\t\t\tlen = nul;\n\t\t\tnoCrc = 1;\n\t\t\tif (comma <= nul) {\n\t\t\t\tlen = comma;\n\t\t\t\tnoCrc = 0;\n\t\t\t}\n",
    'w': "\t\t\tlen = comma;\n\t\t\tif (comma > nul)\n\t\t\t\tlen = nul;\n\t\t\tnoCrc = len == nul && comma != nul;\n",
}
for k, v in BLH.items():
    ALL['bl' + k] = sect('bl', BL, v)
# no flag: test again where the flag was
NF = lambda t: sect('bl', BL, "\t\t\tlen = comma;\n\t\t\tif (comma > nul)\n\t\t\t\tlen = nul;\n")
ALL['blnf_cmp'] = chain(NF(0), sect('bl', BLF, "\t\t\tif (comma <= nul) {\n"))
ALL['blnf_cmp2'] = chain(NF(0), sect('bl', BLF, "\t\t\tif (!(comma > nul)) {\n"))
ALL['blnf_len'] = chain(NF(0), sect('bl', BLF, "\t\t\tif (len == comma) {\n"))
ALL['blnf_ne'] = chain(NF(0), sect('bl', BLF, "\t\t\tif (len != nul) {\n"))
# flag as int kept in its own type, bl only: a block local
ALL['bl_lc'] = sect('bl', "\t\t\tlen = comma;\n\t\t\tnoCrc = 0;\n", "\t\t\tint hasCrc;\n\n\t\t\tlen = comma;\n\t\t\thasCrc = 1;\n") if 0 else None
del ALL['bl_lc']


def bl_has(t):
    return t


def blhas(s):
    s = sect('bl', BL, "\t\t\thas = 1;\n\t\t\tlen = comma;\n\t\t\tif (comma > nul) {\n\t\t\t\tlen = nul;\n\t\t\t\thas = 0;\n\t\t\t}\n")(s)
    s = sect('bl', BLF, "\t\t\tif (has) {\n")(s)
    return L.sub(s, "\tuint32_t noCrc;\n", "\tuint32_t noCrc;\n\tint has;\n") if "\tuint32_t noCrc;\n" in s else s


ALL['blhas'] = blhas

# the arm test of noCrc
ALL['blpos'] = sect('bl', "\t\t\tpos = pos + len + 1;\n\t\t\tif (!noCrc) {\n", "\t\t\tpos = pos + len + 1;\n\t\t\tif (noCrc == 0) {\n")
ALL['blflip'] = sect('bl', "\t\t\t\tpos = pos + n + 1;\n\t\t\t} else\n\t\t\t\txb.files[blOrder[i]].crc = 0;\n", "\t\t\t\tpos = pos + n + 1;\n\t\t\t} else {\n\t\t\t\txb.files[blOrder[i]].crc = 0;\n\t\t\t}\n")

# flashfs and security the same
FH = "\t\t\tnoCrc = 1;\n\t\t\tlen = nul;\n\t\t\tif (comma >= 0 && comma < nul) {\n\t\t\t\tlen = comma;\n\t\t\t\tnoCrc = 0;\n\t\t\t}\n"
FF = "\t\t\t\tif (!noCrc) {\n"
ALL['fl_q'] = sect('flash', FH, "\t\t\tnoCrc = !(comma >= 0 && comma < nul);\n\t\t\tlen = noCrc ? nul : comma;\n")
ALL['fl_r'] = sect('flash', FH, "\t\t\tnoCrc = comma < 0 || comma >= nul;\n\t\t\tif (noCrc)\n\t\t\t\tlen = nul;\n\t\t\telse\n\t\t\t\tlen = comma;\n")
ALL['fl_nf'] = chain(sect('flash', FH, "\t\t\tlen = nul;\n\t\t\tif (comma >= 0 && comma < nul)\n\t\t\t\tlen = comma;\n"), sect('flash', FF, "\t\t\t\tif (comma >= 0 && comma < nul) {\n"))
ALL['fl_nfl'] = chain(sect('flash', FH, "\t\t\tlen = nul;\n\t\t\tif (comma >= 0 && comma < nul)\n\t\t\t\tlen = comma;\n"), sect('flash', FF, "\t\t\t\tif (len != nul) {\n"))
ALL['fl_nfc'] = chain(sect('flash', FH, "\t\t\tlen = nul;\n\t\t\tif (comma >= 0 && comma < nul)\n\t\t\t\tlen = comma;\n"), sect('flash', FF, "\t\t\t\tif (len == comma) {\n"))
SH = "\t\t\tif (comma > nul) {\n\t\t\t\tnoCrc = 1;\n\t\t\t\tlen = nul;\n\t\t\t} else {\n\t\t\t\tnoCrc = 0;\n\t\t\t\tlen = comma;\n\t\t\t}\n"
SF = "\t\t\t\tif (!noCrc) {\n"
ALL['sec_q'] = sect('sec', SH, "\t\t\tnoCrc = comma > nul;\n\t\t\tlen = noCrc ? nul : comma;\n")
ALL['sec_nf'] = chain(sect('sec', SH, "\t\t\tlen = comma;\n\t\t\tif (comma > nul)\n\t\t\t\tlen = nul;\n"), sect('sec', SF, "\t\t\t\tif (comma <= nul) {\n"))
ALL['sec_nfl'] = chain(sect('sec', SH, "\t\t\tlen = comma;\n\t\t\tif (comma > nul)\n\t\t\t\tlen = nul;\n"), sect('sec', SF, "\t\t\t\tif (len == comma) {\n"))
# raw with a len, as the others
ALL['raw_len'] = lambda s: s
del ALL['raw_len']
# no flag state at all: the crc arm inside the if
RAW = "\t\t\tif (comma == -1 || comma >= nul) {"
ALL['raw_f'] = lambda s: sect('raw', RAW, "\t\t\tnoCrc = comma == -1 || comma >= nul;\n\t\t\tif (noCrc) {")(s)
ALL['raw_f2'] = lambda s: sect('raw', RAW, "\t\t\tn = comma == -1 || comma >= nul;\n\t\t\tif (n) {")(s)


class D(dict):
    def __missing__(self, k):
        def f(s):
            for e in k.split('+'):
                s = ALL[e](s)
            return s
        return f


T.E['u'] = D()


def single():
    V = {}
    for d in T.SUBS:
        V[d + '|'] = T.state(d + '|')
        for e in ALL:
            lb = '%s|u=%s' % (d, e)
            V[lb] = T.state(lb)
    rs = T.run(V, 'u_single', 6)
    T.floors(rs)
    sc = {r[3]: r[0] for r in rs}
    print('edit: ' + ' '.join(d or 'none' for d in T.SUBS))
    for e in sorted(ALL, key=lambda e: min(sc['%s|u=%s' % (d, e)] for d in T.SUBS)):
        print(e, ' '.join(str(sc['%s|u=%s' % (d, e)]) for d in T.SUBS))


if __name__ == '__main__':
    single()
