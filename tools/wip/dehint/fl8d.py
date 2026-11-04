"""fl8d.py: [flashfs] gaps from attempt 7 (crc2, continue, end test) and access spelling of xb.firmware / xb.firmwareCrc,
plus the same spelling in the other sections.  Each edit at all T1-T3 subsets.
  python fl8d.py single
  python fl8d.py pair [thresh]     pairs of the edits with a state within thresh (default 12) of the floor
Labels `drops|d=edit` or `drops|d=edit+edit`."""
import itertools, re, sys
import fllib as L, fl6lib as F, fl8lib as T

A, B = F.SECS['flash']
ALL = {}


def fl(fn):
    def f(s):
        i, j = s.index(A), s.index(B)
        return s[:i] + fn(s[i:j]) + s[j:]
    return f


def reg(name, fn):
    ALL[name] = fn


LOGL = "\t\t\t\tlog_printf(1, \"found (%d) '%s' crc: 0x%08x\\n\", ++xb.nFirmware, xb.firmware[i], crc);\n"
Z = "crc = xb.firmwareCrc[i] = 0;"
V = "crc = xb.firmwareCrc[i] = myatox32(tmp, 0);"


def crc2a(t):
    t = L.sub(t, "\t\t\t\t\tif (n == 0)\n\t\t\t\t\t\t" + Z, "\t\t\t\t\tif (n == 0) {\n\t\t\t\t\t\tcrc = 0;\n\t\t\t\t\t\txb.firmwareCrc[i] = 0;\n\t\t\t\t\t}")
    t = t.replace("\t\t\t\t\t} else if (n != 8)", "\t\t\t\t\t} else if (n != 8)")
    t = L.sub(t, "\t\t\t\t} else\n\t\t\t\t\t" + Z, "\t\t\t\t} else {\n\t\t\t\t\tcrc = 0;\n\t\t\t\t\txb.firmwareCrc[i] = 0;\n\t\t\t\t}")
    return t


def crc2b(t):
    return crc2a(t).replace("xb.firmwareCrc[i] = 0;", "xb.firmwareCrc[i] = crc;")


def crc2r(t):
    """store first, crc from it"""
    t = crc2a(t)
    return t.replace("crc = 0;\n\t\t\t\t\t\txb.firmwareCrc[i] = 0;", "xb.firmwareCrc[i] = 0;\n\t\t\t\t\t\tcrc = 0;").replace("crc = 0;\n\t\t\t\t\txb.firmwareCrc[i] = 0;", "xb.firmwareCrc[i] = 0;\n\t\t\t\t\tcrc = 0;")


def crc2v(t):
    return L.sub(crc2a(t), V, "crc = myatox32(tmp, 0);\n\t\t\t\t\t\txb.firmwareCrc[i] = crc;")


def crcend(t):
    """one store, before the log"""
    t = t.replace(Z, "crc = 0;")
    t = L.sub(t, V, "crc = myatox32(tmp, 0);")
    return L.sub(t, LOGL, "\t\t\t\txb.firmwareCrc[i] = crc;\n" + LOGL)


def crcinit(t):
    """crc = 0 before the if; arms only set it when there is one"""
    t = crcend(t)
    t = L.sub(t, "\t\t\t\tif (!noCrc) {\n", "\t\t\t\tcrc = 0;\n\t\t\t\tif (!noCrc) {\n")
    t = L.sub(t, "\t\t\t\t\tif (n == 0)\n\t\t\t\t\t\tcrc = 0;\n\t\t\t\t\telse if (n != 8) {", "\t\t\t\t\tif (n != 0 && n != 8) {")
    t = L.sub(t, "\t\t\t\t\t} else {\n\t\t\t\t\t\tstrncpy(tmp, (char *)&buf[pos], 8);", "\t\t\t\t\t}\n\t\t\t\t\tif (n == 8) {\n\t\t\t\t\t\tstrncpy(tmp, (char *)&buf[pos], 8);")
    t = L.sub(t, "\t\t\t\t} else\n\t\t\t\t\tcrc = 0;\n", "\t\t\t\t}\n")
    return t


def crcinit2(t):
    t = crcend(t)
    t = L.sub(t, "\t\t\t\tif (!noCrc) {\n", "\t\t\t\tcrc = 0;\n\t\t\t\tif (!noCrc) {\n")
    t = L.sub(t, "\t\t\t\t\tif (n == 0)\n\t\t\t\t\t\tcrc = 0;\n\t\t\t\t\telse if (n != 8) {", "\t\t\t\t\tif (n == 0)\n\t\t\t\t\t\t;\n\t\t\t\t\telse if (n != 8) {")
    t = L.sub(t, "\t\t\t\t} else\n\t\t\t\t\tcrc = 0;\n", "\t\t\t\t}\n")
    return t


def crcrr(t):
    """re-read at the log, no crc variable (as [security])"""
    t = t.replace(Z, "xb.firmwareCrc[i] = 0;")
    t = L.sub(t, V, "xb.firmwareCrc[i] = myatox32(tmp, 0);")
    return L.sub(t, "xb.firmware[i], crc);", "xb.firmware[i], xb.firmwareCrc[i]);")


reg('crc2a', fl(crc2a))
reg('crc2b', fl(crc2b))
reg('crc2r', fl(crc2r))
reg('crc2v', fl(crc2v))
reg('crcend', fl(crcend))
reg('crcinit', fl(crcinit))
reg('crcinit2', fl(crcinit2))
reg('crcrrall', fl(crcrr))

# end of the loop
ENDT = "\t\t\tif (pos >= size)\n\t\t\t\ti = 256;\n"
reg('endrev', fl(lambda t: L.sub(t, ENDT, "\t\t\tif (pos < size)\n\t\t\t\tcontinue;\n\t\t\ti = 256;\n")))
reg('endbrk', fl(lambda t: L.sub(t, ENDT, "\t\t\tif (pos < size)\n\t\t\t\tcontinue;\n\t\t\tbreak;\n")))
reg('endelse', fl(lambda t: L.sub(t, ENDT, "\t\t\tif (pos < size)\n\t\t\t\t;\n\t\t\telse\n\t\t\t\ti = 256;\n")))
reg('endgt', fl(lambda t: L.sub(t, ENDT, "\t\t\tif (size <= pos)\n\t\t\t\ti = 256;\n")))
reg('forend', fl(lambda t: L.sub(L.sub(t, ENDT, ""), "for (i = 0; i < 256; i++) {", "for (i = 0; i < 256 && pos < size; i++) {")))
reg('while', fl(lambda t: L.sub(L.sub(t, ENDT, "\t\t\tif (pos >= size)\n\t\t\t\ti = 256;\n\t\t\ti++;\n"), "for (i = 0; i < 256; i++) {", "i = 0;\n\t\twhile (i < 256) {")))
# `continue` for the no-crc path
reg('contnc', fl(lambda t: t))  # placeholder for scoring identity


def good_cont(t):
    """the path check's else first, then continue style: if (len > 1023) with error, then the body (literal order goes wrong; for scoring)"""
    return t


# names
def name_all(t):
    t = L.sub(t, "\t\t\tp = &buf[pos];\n", "\t\t\tchar *name = xb.firmware[i];\n\n\t\t\tp = &buf[pos];\n")
    h, _, r = t.partition("char *name = xb.firmware[i];")
    return h + "char *name = xb.firmware[i];" + r.replace("xb.firmware[i]", "name")


def name_late(t):
    """set where the path check passes"""
    t = L.sub(t, "\t\t\tif (len <= 1023) {\n", "\t\t\tif (len <= 1023) {\n\t\t\t\tchar *name = xb.firmware[i];\n\n")
    h, _, r = t.partition("char *name = xb.firmware[i];")
    return h + "char *name = xb.firmware[i];" + r.replace("xb.firmware[i]", "name")


def name_fn(t):
    """a function level pointer, set in the loop"""
    t = L.sub(t, "\t\t\tp = &buf[pos];\n", "\t\t\tchar *name;\n\n\t\t\tname = xb.firmware[i];\n\t\t\tp = &buf[pos];\n")
    h, _, r = t.partition("name = xb.firmware[i];")
    return h + "name = xb.firmware[i];" + r.replace("xb.firmware[i]", "name")


def name_block(t):
    """only the base name check"""
    a = t.index("\t\t\t\tif (len > 21) {\n")
    b = t.index("\t\t\t\tpos = pos + len + 1;\n")
    x = t[a:b].replace("xb.firmware[i]", "name")
    x = x.replace("if (len > 21) {\n", "if (len > 21) {\n\t\t\t\t\tchar *name = xb.firmware[i];\n\n", 1)
    return t[:a] + x + t[b:]


def name_inc(t):
    """walk the table with a pointer"""
    t = L.sub(t, "\t\tfor (i = 0; i < 256; i++) {\n", "\t\tname = xb.firmware[0];\n\t\tfor (i = 0; i < 256; i++, name += sizeof(xb.firmware[0])) {\n")
    t = L.sub(t, "\t\tpos = off;\n", "\t\tchar *name;\n\n\t\tpos = off;\n")
    return t.replace("xb.firmware[i]", "name")


def name_inc2(t):
    """as name_inc, firmware pointer"""
    t = L.sub(t, "\t\tfor (i = 0; i < 256; i++) {\n", "\t\tfor (i = 0; i < 256; i++) {\n\t\t\tchar *name = fw[i];\n\n")
    t = L.sub(t, "\t\tpos = off;\n", "\t\tchar (*fw)[0x400] = xb.firmware;\n\n\t\tpos = off;\n")
    h, _, r = t.partition("char *name = fw[i];")
    return h + "char *name = fw[i];" + r.replace("xb.firmware[i]", "name")


def tab(t):
    t = L.sub(t, "\t\tpos = off;\n", "\t\tchar (*fw)[0x400] = xb.firmware;\n\n\t\tpos = off;\n")
    return t.replace("xb.firmware[i]", "fw[i]")


def fwp(t):
    """pointer to the row: (*fw)[len]"""
    t = L.sub(t, "\t\t\tp = &buf[pos];\n", "\t\t\tchar (*fw)[0x400] = &xb.firmware[i];\n\n\t\t\tp = &buf[pos];\n")
    h, _, r = t.partition("char (*fw)[0x400] = &xb.firmware[i];")
    r = r.replace("xb.firmware[i][len - 1]", "(*fw)[len - 1]").replace("xb.firmware[i][len]", "(*fw)[len]").replace("xb.firmware[i]", "*fw")
    return h + "char (*fw)[0x400] = &xb.firmware[i];" + r


def plus(t):
    return t.replace("xb.firmware[i]", "*(xb.firmware + i)")


def plusc(t):
    return t.replace("xb.firmwareCrc[i]", "*(xb.firmwareCrc + i)")


def crcp(t):
    """pointer to the crc's slot"""
    t = L.sub(t, "\t\t\tp = &buf[pos];\n", "\t\t\tuint32_t *c = &xb.firmwareCrc[i];\n\n\t\t\tp = &buf[pos];\n")
    return t.replace("xb.firmwareCrc[i] =", "*c =")


def crcp2(t):
    t = L.sub(t, "\t\t\t\tif (!noCrc) {\n", "\t\t\t\tc = xb.firmwareCrc + i;\n\t\t\t\tif (!noCrc) {\n")
    t = L.sub(t, "\t\t\tp = &buf[pos];\n", "\t\t\tuint32_t *c;\n\n\t\t\tp = &buf[pos];\n")
    return t.replace("xb.firmwareCrc[i] =", "*c =")


def lastp2(t):
    """a pointer to the name's end, set before the name check"""
    t = L.sub(t, "\t\t\t\tpos = pos + len + 1;\n\t\t\t\tif (xb.firmware[i][len - 1] == '1' || xb.firmware[i][len - 1] == '2')\n\t\t\t\t\txb.firmware[i][len - 1] = 0;\n",
              "\t\t\t\tpos = pos + len + 1;\n\t\t\t\tc = xb.firmware[i][len - 1];\n\t\t\t\tif (c == '1' || c == '2')\n\t\t\t\t\txb.firmware[i][len - 1] = 0;\n")
    return L.sub(t, "\t\t\tp = &buf[pos];\n", "\t\t\tchar c;\n\n\t\t\tp = &buf[pos];\n")


def str0(t):
    """the terminator through a pointer"""
    return L.sub(t, "xb.firmware[i][len] = 0;", "*(xb.firmware[i] + len) = 0;")


def endp(t):
    t = L.sub(t, "\t\t\t\txb.firmware[i][len] = 0;\n", "\t\t\t\tname = xb.firmware[i] + len;\n\t\t\t\t*name = 0;\n")
    t = L.sub(t, "\t\t\t\tif (xb.firmware[i][len - 1] == '1' || xb.firmware[i][len - 1] == '2')\n\t\t\t\t\txb.firmware[i][len - 1] = 0;\n",
              "\t\t\t\tif (name[-1] == '1' || name[-1] == '2')\n\t\t\t\t\tname[-1] = 0;\n")
    return L.sub(t, "\t\t\tp = &buf[pos];\n", "\t\t\tchar *name;\n\n\t\t\tp = &buf[pos];\n")


for n, fn in [('nameall', name_all), ('namelate', name_late), ('namefn', name_fn), ('nameblock', name_block), ('nameinc', name_inc), ('nameinc2', name_inc2),
              ('tab', tab), ('fwp', fwp), ('plus', plus), ('plusc', plusc), ('crcp', crcp), ('crcp2', crcp2), ('lastc2', lastp2), ('str0', str0), ('endp', endp)]:
    reg(n, fl(fn))


# other sections: bl and security
def sec(sec_, fn):
    a, b = F.SECS[sec_]

    def f(s):
        i, j = s.index(a), s.index(b)
        return s[:i] + fn(s[i:j]) + s[j:]
    return f


def blent(t):
    """struct fileent pointer, as the files loop has"""
    t = L.sub(t, "\t\t\tp = &buf[pos];\n", "\t\t\tstruct fileent *e = &xb.files[blOrder[i]];\n\n\t\t\tp = &buf[pos];\n")
    h, _, r = t.partition("struct fileent *e = &xb.files[blOrder[i]];")
    return h + "struct fileent *e = &xb.files[blOrder[i]];" + r.replace("xb.files[blOrder[i]].", "e->")


def blent2(t):
    t = L.sub(t, "\t\t\tif (len < 0) {", "\t\t\te = &xb.files[blOrder[i]];\n\t\t\tif (len < 0) {")
    t = L.sub(t, "\t\t\tp = &buf[pos];\n", "\t\t\tstruct fileent *e;\n\n\t\t\tp = &buf[pos];\n")
    return t.replace("xb.files[blOrder[i]].", "e->")


def blidx(t):
    """the file's index in a local"""
    t = L.sub(t, "\t\t\tp = &buf[pos];\n", "\t\t\tint k = blOrder[i];\n\n\t\t\tp = &buf[pos];\n")
    h, _, r = t.partition("int k = blOrder[i];")
    return h + "int k = blOrder[i];" + r.replace("xb.files[blOrder[i]]", "xb.files[k]")


def secname(t):
    t = L.sub(t, "\t\t\tp = &buf[pos];\n", "\t\t\tchar *name = xb.flashFiles[i];\n\n\t\t\tp = &buf[pos];\n")
    h, _, r = t.partition("char *name = xb.flashFiles[i];")
    return h + "char *name = xb.flashFiles[i];" + r.replace("xb.flashFiles[i]", "name")


def secc(t):
    t = L.sub(t, "\t\t\tp = &buf[pos];\n", "\t\t\tuint32_t *c = &xb.flashCrc[i];\n\n\t\t\tp = &buf[pos];\n")
    h, _, r = t.partition("uint32_t *c = &xb.flashCrc[i];")
    return h + "uint32_t *c = &xb.flashCrc[i];" + r.replace("xb.flashCrc[i]", "*c")


def rawname(t):
    t = L.sub(t, "\t\t\tp = &buf[pos];\n", "\t\t\tchar *name = xb.rawPatch[i].name;\n\n\t\t\tp = &buf[pos];\n")
    h, _, r = t.partition("char *name = xb.rawPatch[i].name;")
    return h + "char *name = xb.rawPatch[i].name;" + r.replace("xb.rawPatch[i].name", "name")


def rawptr(t):
    t = L.sub(t, "\t\t\tp = &buf[pos];\n", "\t\t\ttypeof(&xb.rawPatch[0]) r = &xb.rawPatch[i];\n\n\t\t\tp = &buf[pos];\n")
    return t.replace("xb.rawPatch[i].", "r->")


def rawinc(t):
    return L.sub(t, "++xb.nRawPatches, xb.rawPatch[i].name, xb.rawPatch[i].offset);", "xb.nRawPatches + 1, xb.rawPatch[i].name, xb.rawPatch[i].offset);\n\t\t\t\txb.nRawPatches++;") if 0 else t


reg('blent', sec('bl', blent))
reg('blent2', sec('bl', blent2))
reg('blidx', sec('bl', blidx))
reg('secname', sec('sec', secname))
reg('secc', sec('sec', secc))
reg('rawname', sec('raw', rawname))
reg('rawptr', sec('raw', rawptr))
del ALL['contnc']

T.E['d'] = {}


def lab(x):
    def f(s):
        for e in x.split('+'):
            s = ALL[e](s)
        return s
    return f


class D(dict):
    def __missing__(self, k):
        return lab(k)


T.E['d'] = D()


def single():
    V = {}
    for d in T.SUBS:
        V[d + '|'] = T.state(d + '|')
        for e in ALL:
            lb = '%s|d=%s' % (d, e)
            V[lb] = T.state(lb)
    rs = T.run(V, 'd_single', 10)
    T.floors(rs)
    sc = {r[3]: r[0] for r in rs}
    tab_ = sorted(ALL, key=lambda e: min(sc['%s|d=%s' % (d, e)] for d in T.SUBS))
    print('edit: ' + ' '.join(d or 'none' for d in T.SUBS))
    for e in tab_:
        print(e, ' '.join(str(sc['%s|d=%s' % (d, e)]) for d in T.SUBS))


def pair(thresh=12):
    V = {}
    base = {}
    keep = []
    for ln in open(T.os.path.join(T.A8, 'd_single.txt')):
        c = ln.rstrip('\n').split('\t')
        sc, lb = float(c[0]), c[3]
        if lb.endswith('|'):
            base[lb[:-1]] = sc
    for ln in open(T.os.path.join(T.A8, 'd_single.txt')):
        c = ln.rstrip('\n').split('\t')
        sc, lb = float(c[0]), c[3]
        d, _, a = lb.partition('|')
        if a and sc < 600 and sc != base[d]:
            keep.append(a[2:])
    keep = sorted(set(keep))
    print(keep)
    for x, y in itertools.combinations(keep, 2):
        for d in T.SUBS:
            lb = '%s|d=%s+%s' % (d, x, y)
            try:
                V[lb] = T.state(lb)
            except ValueError:
                pass
    print(len(V))
    rs = T.run(V, 'd_pair', 15)
    T.floors(rs)


if __name__ == '__main__':
    if sys.argv[1] == 'single':
        single()
    else:
        pair()
