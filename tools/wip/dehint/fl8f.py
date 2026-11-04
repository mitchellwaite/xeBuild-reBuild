"""fl8f.py: tests with a natural second spelling that threading makes silent (section heads off != -1 / off >= 0, comma == -1 / comma < 0 ...),
and setupFiles' body forms (inlined after IPA, so its names aren't normalised).
  python fl8f.py single
  python fl8f.py rand N [seed]     combinations of the ones that move something, near the floor
Labels `drops|f=edit+edit`."""
import itertools, os, random, sys
import fllib as L, fl6lib as F, fl8lib as T

ALL = {}
S = F.SECS


def sect(name, old, new, count=1):
    a, b = S[name]

    def f(s):
        i, j = s.index(a), s.index(b)
        return s[:i] + L.sub(s[i:j], old, new, count) + s[j:]
    return f


HEADS = {'raw': 'off != -1', 'flash': 'off != -1', 'sec': 'off != -1', 'bl': 'off >= 0'}
for sc, h in HEADS.items():
    for alt in ('off >= 0', 'off != -1', 'off > -1', '-1 != off', 'off + 1 != 0', '!(off < 0)'):
        if alt != h:
            ALL['h%s_%s' % (sc, alt.replace(' ', '').replace('!', 'n').replace('>=', 'ge').replace('>', 'gt').replace('<', 'lt').replace('=', 'e').replace('-', 'm').replace('+', 'p').replace('(', '').replace(')', ''))] = sect(sc, '\tif (%s) {' % h, '\tif (%s) {' % alt)
# version's own head
ALL['hver_ge'] = lambda s: L.sub(s, '\toff = memFindStr(buf, size, "[version]", 1);\n\tif (off != -1) {', '\toff = memFindStr(buf, size, "[version]", 1);\n\tif (off >= 0) {')
ALL['rawc_lt'] = sect('raw', 'if (comma == -1 || comma >= nul) {', 'if (comma < 0 || comma >= nul) {')
ALL['rawc_rev'] = sect('raw', 'if (comma == -1 || comma >= nul) {', 'if (comma >= nul || comma == -1) {')
ALL['rawc_nest'] = sect('raw', 'if (comma == -1 || comma >= nul) {\n\t\t\t\tlog_printf(0, "\\n******* ERROR: an entry in [rawpatch] is missing offset info!\\n");\n\t\t\t\tfree(buf);\n\t\t\t\treturn 0;\n\t\t\t}\n',
                        'if (comma == -1) {\n\t\t\t\tlog_printf(0, "\\n******* ERROR: an entry in [rawpatch] is missing offset info!\\n");\n\t\t\t\tfree(buf);\n\t\t\t\treturn 0;\n\t\t\t}\n\t\t\tif (comma >= nul) {\n\t\t\t\tlog_printf(0, "\\n******* ERROR: an entry in [rawpatch] is missing offset info!\\n");\n\t\t\t\tfree(buf);\n\t\t\t\treturn 0;\n\t\t\t}\n')
ALL['rawc_good'] = sect('raw', 'if (comma == -1 || comma >= nul) {', 'if (!(comma != -1 && comma < nul)) {')
ALL['rawn_lt'] = sect('raw', 'if (n == 0 || n > 10) {', 'if (n > 10 || n == 0) {')
ALL['rawn_u'] = sect('raw', 'if (n == 0 || n > 10) {', 'if (n < 1 || n > 10) {')
ALL['rawl_gt'] = sect('raw', 'if (comma <= 1023) {', 'if (comma < 1024) {')
ALL['rawend_lt'] = sect('raw', '\t\t\tif (pos >= end)\n\t\t\t\ti = 16;\n', '\t\t\tif (pos > end - 1)\n\t\t\t\ti = 16;\n')
ALL['rawlast'] = sect('raw', 'if (pos < end) {', 'if (end > pos) {')
ALL['rawi0'] = sect('raw', '\t\tfor (i = xb.nRawPatches; i < 16; i++) {', '\t\ti = xb.nRawPatches;\n\t\tfor (; i < 16; i++) {')
ALL['rawcn'] = sect('raw', "\t\t\tnul = memFindChar(p, 0, size - pos);\n\t\t\tcomma = memFindChar(p, ',', size - pos);\n", "\t\t\tcomma = memFindChar(p, ',', size - pos);\n\t\t\tnul = memFindChar(p, 0, size - pos);\n")
ALL['flc_lt'] = sect('flash', 'if (comma >= 0 && comma < nul) {', 'if (comma != -1 && comma < nul) {')
ALL['flc_rev'] = sect('flash', 'if (comma >= 0 && comma < nul) {', 'if (comma < nul && comma >= 0) {')
ALL['blc_ge'] = sect('bl', '\t\t\tlen = comma;\n\t\t\tnoCrc = 0;\n\t\t\tif (comma > nul) {\n\t\t\t\tlen = nul;\n\t\t\t\tnoCrc = 1;\n\t\t\t}\n', '\t\t\tif (comma > nul) {\n\t\t\t\tlen = nul;\n\t\t\t\tnoCrc = 1;\n\t\t\t} else {\n\t\t\t\tlen = comma;\n\t\t\t\tnoCrc = 0;\n\t\t\t}\n')
ALL['blc_sw'] = sect('bl', '\t\t\tlen = comma;\n\t\t\tnoCrc = 0;\n', '\t\t\tnoCrc = 0;\n\t\t\tlen = comma;\n')
ALL['bl_l1'] = sect('bl', 'if (len < 0) {', 'if (len == -1) {')
ALL['bl_e'] = sect('bl', 'if (pos > end) {', 'if (end < pos) {')
ALL['sec_flip'] = sect('sec', '\t\t\tif (comma > nul) {\n\t\t\t\tnoCrc = 1;\n\t\t\t\tlen = nul;\n\t\t\t} else {\n\t\t\t\tnoCrc = 0;\n\t\t\t\tlen = comma;\n\t\t\t}\n', '\t\t\tif (comma <= nul) {\n\t\t\t\tnoCrc = 0;\n\t\t\t\tlen = comma;\n\t\t\t} else {\n\t\t\t\tnoCrc = 1;\n\t\t\t\tlen = nul;\n\t\t\t}\n')
ALL['sec_sw'] = sect('sec', '\t\t\tif (comma > nul) {\n\t\t\t\tnoCrc = 1;\n\t\t\t\tlen = nul;\n\t\t\t} else {\n\t\t\t\tnoCrc = 0;\n\t\t\t\tlen = comma;\n\t\t\t}\n', '\t\t\tnoCrc = 0;\n\t\t\tlen = comma;\n\t\t\tif (comma > nul) {\n\t\t\t\tnoCrc = 1;\n\t\t\t\tlen = nul;\n\t\t\t}\n')


# setupFiles
def sf(fn):
    a = "static void setupFiles(void)\n"
    b = "/* an entry's name,crc separators."

    def f(s):
        i, j = s.index(a), s.index(b)
        return s[:i] + fn(s[i:j]) + s[j:]
    return f


def rep(old, new, count=1):
    return sf(lambda t: L.sub(t, old, new, count))


ALL['sf_eloop'] = sf(lambda t: L.sub(L.sub(t, "\tstruct fileent *e;\n", ""), "\t\te = &xb.files[i];\n", "\t\tstruct fileent *e = &xb.files[i];\n\n"))
ALL['sf_efor'] = sf(lambda t: L.sub(L.sub(L.sub(t, "\t\te = &xb.files[i];\n", ""), "for (i = 0; ; i++) {", "e = xb.files;\n\tfor (i = 0; ; i++, e++) {"), "\tstruct fileent *e;\n", "\tstruct fileent *e;\n"))


def sfname(t):
    t = L.sub(t, "\t\tswitch (e->type) {\n", "\t\tname = e->name;\n\t\tswitch (e->type) {\n")
    t = t.replace("e->name,", "name,")
    t = L.sub(t, "\tstruct fileent *e;\n", "\tstruct fileent *e;\n\tchar *name;\n")
    return t


ALL['sf_name'] = sf(sfname)


def sfnoe(t):
    t = L.sub(L.sub(t, "\t\te = &xb.files[i];\n", ""), "\tstruct fileent *e;\n", "")
    return t.replace("e->", "xb.files[i].")


ALL['sf_noe'] = sf(sfnoe)


def sfcon(t):
    t = L.sub(t, "\t\tcase 23:\n" if 0 else "\t\t\tstrcpy(e->name, fnPatches);\n", "\t\t\tstrcpy(e->name, fnPatches);\n\t\t\tcon = consoleNames[xb.flags & CONSOLE_MASK];\n")
    t = t.replace("strcat(e->name, consoleNames[xb.flags & CONSOLE_MASK]);", "strcat(e->name, con);")
    return L.sub(t, "\tstruct fileent *e;\n", "\tstruct fileent *e;\n\tconst char *con;\n")


ALL['sf_con'] = sf(sfcon)


def sftype(t):
    """the entry's type in a local through the arms"""
    return t


def sfty(t):
    t = t.replace("e->type = ", "ty = ")
    t = L.sub(t, "\t\tswitch (e->type) {\n", "\t\te->type = ty;\n\t\tswitch (ty) {\n")
    return L.sub(t, "\tstruct fileent *e;\n", "\tstruct fileent *e;\n\tint ty;\n")


ALL['sf_ty'] = sf(sfty)


def sfloc(t):
    """the table in a local, one copy of the stores"""
    m = t.index("\t\tif (xb.type == BUILD_JTAG) {\n")
    n = t.index("\t\tswitch (e->type) {\n")
    x = t[m:n]
    import re
    x = re.sub(r"e->type = (\w+)\[i\]\.type;\n\s*e->offset = \w+\[i\]\.offset;\n", lambda k: "loc = %s;\n" % k.group(1), x)
    t = t[:m] + x + "\t\te->type = loc[i].type;\n\t\te->offset = loc[i].offset;\n" + t[n:]
    return L.sub(t, "\tstruct fileent *e;\n", "\tstruct fileent *e;\n\tstruct fileloc *loc;\n")


ALL['sf_loc'] = sf(sfloc)
ALL['sf_for'] = rep("for (i = 0; ; i++) {\n\t\tif (i >= xb.nFiles)\n\t\t\tbreak;\n", "i = 0;\n\twhile (1) {\n\t\tif (i >= xb.nFiles)\n\t\t\tbreak;\n") if 0 else rep("for (i = 0; ; i++) {\n\t\tif (i >= xb.nFiles)\n\t\t\tbreak;\n", "for (i = 0; ; i++) {\n\t\tif (i >= xb.nFiles)\n\t\t\treturn;\n")
ALL['sf_i'] = rep("\tint i;\n", "\tlong i;\n")
ALL['sf_decl'] = rep("\tint i;\n\tstruct fileent *e;\n", "\tstruct fileent *e;\n\tint i;\n")
ALL['sf_blank'] = rep("\t\t}\n\t}\n\n}\n", "\t\t}\n\t}\n}\n")
ALL['sf_g2'] = rep('\t\t\t\tif (xb.glitch2mfg)\n\t\t\t\t\tstrcat(e->name, "g2m");\n\t\t\t\telse\n\t\t\t\t\tstrcat(e->name, "g2");\n', '\t\t\t\tstrcat(e->name, xb.glitch2mfg ? "g2m" : "g2");\n')
ALL['sf_cm'] = sf(lambda t: t.replace("(xb.flags & CONSOLE_MASK) ==", "consoleType ==").replace("\t\t\t\tif (consoleType == CONSOLE_TRINITY)", "\t\t\t\tuint32_t consoleType = xb.flags & CONSOLE_MASK;\n\n\t\t\t\tif (consoleType == CONSOLE_TRINITY)"))
ALL['sf_sfx'] = rep('\t\t\tif (xb.blSuffix[0])\n\t\t\t\tstrcat(e->name, xb.blSuffix);\n', '\t\t\tstrcat(e->name, xb.blSuffix);\n')


class D(dict):
    def __missing__(self, k):
        def f(s):
            for e in k.split('+'):
                s = ALL[e](s)
            return s
        return f


T.E['f'] = D()


def single():
    V = {}
    for d in T.SUBS:
        V[d + '|'] = T.state(d + '|')
        for e in ALL:
            lb = '%s|f=%s' % (d, e)
            V[lb] = T.state(lb)
    rs = T.run(V, 'f_single', 8)
    T.floors(rs)
    sc = {r[3]: r[0] for r in rs}
    print('edit: ' + ' '.join(d or 'none' for d in T.SUBS))
    for e in sorted(ALL, key=lambda e: min(sc['%s|f=%s' % (d, e)] for d in T.SUBS)):
        print(e, ' '.join(str(sc['%s|f=%s' % (d, e)]) for d in T.SUBS))


if __name__ == '__main__':
    single()
