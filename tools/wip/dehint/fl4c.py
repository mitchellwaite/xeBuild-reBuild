"""fl4c.py: file table section as helpers in many forms, plus the small helpers elsewhere (label, build type, cbb...)."""
import itertools, re, sys
import fllib as L, fl4lib as F

M = F.MARKED
a, b = F.MK['files']
FS = M[M.index(a):M.index(b)]
LOC0 = FS.index('\t\tif (xb.type == BUILD_JTAG) {\n')
SW0 = FS.index('\t\tswitch (e->type) {\n')
SWEND = FS.rindex('\t}\n')
LOC = FS[LOC0:SW0]
SW = FS[SW0:SWEND]
C23 = SW[SW.index('\t\t\tstrcpy(e->name, fnPatches);\n'):SW.index('\t\tcase 24:')]
C23B = C23[:C23.rindex('\t\t\tbreak;\n')]


def files(mode, c23):
    """(helpers, replacement text for the section)"""
    sw = SW
    h = ''
    if c23:
        h += 'static void patchName(struct fileent *e)\n{\n%s}\n\n' % C23B
        sw = sw.replace(C23B, '\t\t\tpatchName(e);\n')
    loc = LOC
    if 'S' in mode:
        h += 'static void setFileName(struct fileent *e)\n{\n%s}\n\n' % sw
        sw = '\t\tsetFileName(e);\n'
    if 'L' in mode:
        h += 'static void setFileLoc(struct fileent *e, int i)\n{\n%s}\n\n' % loc
        loc = '\t\tsetFileLoc(e, i);\n'
    body = '\t\te = &xb.files[i];\n' + loc + sw
    if 'W' in mode:
        h += 'static void setupFiles(void)\n{\n\tint i;\n\tstruct fileent *e;\n\n\tfor (i = 0; i < xb.nFiles; i++) {\n%s\t}\n}\n\n' % body
        return h, '\tsetupFiles();\n'
    if 'E' in mode:
        h += 'static void setupFile(int i)\n{\n\tstruct fileent *e = &xb.files[i];\n\n%s}\n\n' % (loc + sw)
        return h, '\tfor (i = 0; i < xb.nFiles; i++)\n\t\tsetupFile(i);\n'
    if 'P' in mode:
        h += 'static void setupFile(struct fileent *e, int i)\n{\n%s}\n\n' % (loc + sw)
        return h, '\tfor (i = 0; i < xb.nFiles; i++)\n\t\tsetupFile(&xb.files[i], i);\n'
    return h, '\tfor (i = 0; i < xb.nFiles; i++) {\n%s\t}\n' % body


def gen(mode, c23, extra=(), tests=None):
    s = M
    h, r = files(mode, c23)
    s = L.sub(s, FS, r)
    if 'label' in extra:
        LB = s[s.index('\tif (xb.blSuffix[0])\n\t\tsprintf(label'):s.index('\toff = memFindStr(buf, size, label, 1);')]
        h += 'static void blLabel(char *label)\n{\n%s}\n\n' % LB
        s = L.sub(s, LB, '\tblLabel(label);\n')
    if 'vt' in extra:
        i = s.index('\t\tif (xb.type == BUILD_JTAG) {\n\t\t\txb.nFiles = 19;')
        j = s.index('\t} else {\n\t\tlog_printf(0, "\\n******* ERROR: could not find label [version]')
        B = s[i:j]
        B2 = B.replace('nbl = 9;\n', '').replace('\t\t\tnbl = 6;\n', '\t\t\treturn 6;\n').replace('xb.outName);\n\t\t} else {\n\t\t\tif (xb.type == BUILD_DEVKIT', 'xb.outName);\n\t\t\treturn 9;\n\t\t} else {\n\t\t\tif (xb.type == BUILD_DEVKIT')
        h += 'static int setBuildType(char *tmp)\n{\n%s}\n\n' % B2
        s = L.sub(s, B, '\t\tnbl = setBuildType(tmp);\n')
    if 'ks' in extra:
        KS = s[s.index('\t\tmemset(xb.kernelStr, 0'):s.index('\t\tlog_printf(1, "ini version %s')]
        h += 'static void setKernelStr(unsigned char *p)\n{\n\tint len;\n\n%s}\n\n' % KS.replace('&buf[off]', 'p')
        s = L.sub(s, KS, '\t\tsetKernelStr(&buf[off]);\n')
    if 'done' in extra:
        pass
    k = s.index(F.HEAD)
    s = s[:k] + h + s[k:]
    tests = tests or {}
    for n in F.SITES:
        s = s.replace('@@%s@@' % n, F.test(n, *tests[n]) if n in tests else '')
    return s


if __name__ == '__main__':
    MODES = ['', 'W', 'E', 'P', 'S', 'L', 'SL', 'WS', 'WL', 'WSL', 'ES', 'EL', 'ESL', 'PS', 'PL', 'PSL']
    EX = ['label', 'vt', 'ks']
    V = {}
    for m in MODES:
        for c in (0, 1):
            for r in range(0, 4):
                for x in itertools.combinations(EX, r):
                    V['%s|%d|%s' % (m, c, '+'.join(x))] = gen(m, c, x)
    print(len(V))
    F.run(V, 'c', show=40)
