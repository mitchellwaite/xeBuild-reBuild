"""fl5b.py [n] [seed]: axes that change IPA inlining order or inlined bodies' numbering, with no dead tests, or subsets:
pos  where setupFiles is defined; decl forward declarations of the memFind functions; mc memFindChar forms; ms memFindStr forms;
sf   setupFiles' inner forms.  Sample n states."""
import itertools, os, random, sys
import fllib as L, fl5lib as F

SF_START = 'static void setupFiles(void)\n{'
c0 = F.S0.index('/* the files this build type uses.')
c1 = F.S0.index('/* read the file list ini: the files for this build type')
SF_TEXT = F.S0[c0:c1]
FWD = 'int memFindStr(unsigned char *buf, int size, const char *key, int label);\nint memFindChar(unsigned char *buf, char c, int size);\nvoid checkFileCase(void);\n'

POS = {
    'cur': None,
    'top': '/* copy the base dir\'s casing of',
    'pp': '/* strip comments and invalid characters',
    'ms': '/* offset after `str` in buf',
    'mc': 'int memFindChar(unsigned char *buf, char c, int size)\n{',
    'cfc': 'void checkFileCase(void)\n{',
    'after': '/* offset of the value after `key` in buf, or -1 */',
    'end': '/* load and pre-parse options.ini',
    'last': '/* .rdata after the functions',
}
DECL = {
    'cur': FWD,
    'none': '',
    'sc': 'int memFindChar(unsigned char *buf, char c, int size);\nint memFindStr(unsigned char *buf, int size, const char *key, int label);\nvoid checkFileCase(void);\n',
    'cs': 'void checkFileCase(void);\nint memFindStr(unsigned char *buf, int size, const char *key, int label);\nint memFindChar(unsigned char *buf, char c, int size);\n',
}
MC0 = 'int memFindChar(unsigned char *buf, char c, int size)\n{\n\tint i;\n\n\tfor (i = 0; i < size; i++)\n\t\tif (buf[i] == c)\n\t\t\treturn i;\n\treturn -1;\n}\n'
MC = {
    'cur': MC0,
    'brk': 'int memFindChar(unsigned char *buf, char c, int size)\n{\n\tint i, ret = -1;\n\n\tfor (i = 0; i < size; i++)\n\t\tif (buf[i] == c) {\n\t\t\tret = i;\n\t\t\tbreak;\n\t\t}\n\treturn ret;\n}\n',
    'first': 'int memFindChar(unsigned char *buf, char c, int size)\n{\n\tint i;\n\n\tfor (i = 0; ; i++) {\n\t\tif (i >= size)\n\t\t\treturn -1;\n\t\tif (buf[i] == c)\n\t\t\treturn i;\n\t}\n}\n',
    'firstb': 'int memFindChar(unsigned char *buf, char c, int size)\n{\n\tint i;\n\n\tfor (i = 0; ; i++) {\n\t\tif (i >= size)\n\t\t\tbreak;\n\t\tif (buf[i] == c)\n\t\t\treturn i;\n\t}\n\treturn -1;\n}\n',
    'while': 'int memFindChar(unsigned char *buf, char c, int size)\n{\n\tint i = 0;\n\n\twhile (i < size) {\n\t\tif (buf[i] == c)\n\t\t\treturn i;\n\t\ti++;\n\t}\n\treturn -1;\n}\n',
    'ptr': 'int memFindChar(unsigned char *buf, char c, int size)\n{\n\tint i;\n\tunsigned char *p = buf;\n\n\tfor (i = 0; i < size; i++, p++)\n\t\tif (*p == c)\n\t\t\treturn i;\n\treturn -1;\n}\n',
    'swap': 'int memFindChar(unsigned char *buf, char c, int size)\n{\n\tint i;\n\n\tfor (i = 0; i < size; i++)\n\t\tif (c == buf[i])\n\t\t\treturn i;\n\treturn -1;\n}\n',
    'ifnot': 'int memFindChar(unsigned char *buf, char c, int size)\n{\n\tint i;\n\n\tfor (i = 0; i < size; i++) {\n\t\tif (buf[i] != c)\n\t\t\tcontinue;\n\t\treturn i;\n\t}\n\treturn -1;\n}\n',
}
MS_T = ('\t\t\tif (j == len) {\n\t\t\t\tif (skipNul) {\n\t\t\t\t\tif (buf[i + len] == 0)\n\t\t\t\t\t\treturn i + len + 1;\n\t\t\t\t\treturn i + len;\n\t\t\t\t}\n'
        '\t\t\t\tif (buf[i + len] != 0)\n\t\t\t\t\treturn i + len;\n\t\t\t}\n')
MS = {
    'cur': MS_T,
    'else': '\t\t\tif (j == len) {\n\t\t\t\tif (skipNul) {\n\t\t\t\t\tif (buf[i + len] == 0)\n\t\t\t\t\t\treturn i + len + 1;\n\t\t\t\t\treturn i + len;\n\t\t\t\t} else if (buf[i + len] != 0)\n\t\t\t\t\treturn i + len;\n\t\t\t}\n',
    'not': '\t\t\tif (j == len) {\n\t\t\t\tif (!skipNul) {\n\t\t\t\t\tif (buf[i + len] != 0)\n\t\t\t\t\t\treturn i + len;\n\t\t\t\t} else {\n\t\t\t\t\tif (buf[i + len] == 0)\n\t\t\t\t\t\treturn i + len + 1;\n\t\t\t\t\treturn i + len;\n\t\t\t\t}\n\t\t\t}\n',
    'ne': '\t\t\tif (j == len) {\n\t\t\t\tif (skipNul) {\n\t\t\t\t\tif (buf[i + len] != 0)\n\t\t\t\t\t\treturn i + len;\n\t\t\t\t\treturn i + len + 1;\n\t\t\t\t}\n\t\t\t\tif (buf[i + len] != 0)\n\t\t\t\t\treturn i + len;\n\t\t\t}\n',
    'first': '\t\t\tif (j == len) {\n\t\t\t\tif (buf[i + len] != 0)\n\t\t\t\t\treturn i + len;\n\t\t\t\tif (skipNul)\n\t\t\t\t\treturn i + len + 1;\n\t\t\t}\n',
    'and': '\t\t\tif (j == len && skipNul) {\n\t\t\t\tif (buf[i + len] == 0)\n\t\t\t\t\treturn i + len + 1;\n\t\t\t\treturn i + len;\n\t\t\t}\n\t\t\tif (j == len && buf[i + len] != 0)\n\t\t\t\treturn i + len;\n',
    'cont': '\t\t\tif (j != len)\n\t\t\t\tcontinue;\n\t\t\tif (skipNul) {\n\t\t\t\tif (buf[i + len] == 0)\n\t\t\t\t\treturn i + len + 1;\n\t\t\t\treturn i + len;\n\t\t\t}\n\t\t\tif (buf[i + len] != 0)\n\t\t\t\treturn i + len;\n',
    'q': '\t\t\tif (j == len) {\n\t\t\t\tunsigned char c = buf[i + len];\n\n\t\t\t\tif (skipNul) {\n\t\t\t\t\tif (c == 0)\n\t\t\t\t\t\treturn i + len + 1;\n\t\t\t\t\treturn i + len;\n\t\t\t\t}\n\t\t\t\tif (c != 0)\n\t\t\t\t\treturn i + len;\n\t\t\t}\n',
    'off': '\t\t\tif (j == len) {\n\t\t\t\tint off = i + len;\n\n\t\t\t\tif (skipNul) {\n\t\t\t\t\tif (buf[off] == 0)\n\t\t\t\t\t\treturn off + 1;\n\t\t\t\t\treturn off;\n\t\t\t\t}\n\t\t\t\tif (buf[off] != 0)\n\t\t\t\t\treturn off;\n\t\t\t}\n',
}
MSH = {
    'cur': '\tint i, j, len;\n\n\tlen = strlen(str);\n\tfor (i = 0; i < size - len; i++) {\n\t\tif (str[0] == buf[i]) {\n\t\t\tfor (j = 0; j < len; j++)\n\t\t\t\tif (buf[i + j] != str[j])\n\t\t\t\t\tj = len + 1;\n',
    'p': '\tint i, j, len;\n\tunsigned char *p;\n\n\tlen = strlen(str);\n\tfor (i = 0; i < size - len; i++) {\n\t\tif (str[0] == buf[i]) {\n\t\t\tp = &buf[i];\n\t\t\tfor (j = 0; j < len; j++)\n\t\t\t\tif (p[j] != str[j])\n\t\t\t\t\tj = len + 1;\n',
    'sw': '\tint i, j, len;\n\n\tlen = strlen(str);\n\tfor (i = 0; i < size - len; i++) {\n\t\tif (buf[i] == str[0]) {\n\t\t\tfor (j = 0; j < len; j++)\n\t\t\t\tif (buf[i + j] != str[j])\n\t\t\t\t\tj = len + 1;\n',
    'lim': '\tint i, j, len, lim;\n\n\tlen = strlen(str);\n\tlim = size - len;\n\tfor (i = 0; i < lim; i++) {\n\t\tif (str[0] == buf[i]) {\n\t\t\tfor (j = 0; j < len; j++)\n\t\t\t\tif (buf[i + j] != str[j])\n\t\t\t\t\tj = len + 1;\n',
    'sj': '\tint i, len;\n\n\tlen = strlen(str);\n\tfor (i = 0; i < size - len; i++) {\n\t\tif (str[0] == buf[i]) {\n\t\t\tint j;\n\n\t\t\tfor (j = 0; j < len; j++)\n\t\t\t\tif (buf[i + j] != str[j])\n\t\t\t\t\tj = len + 1;\n',
}
SF_E = 'e = &xb.files[i];'
SFX = {
    'cur': [],
    'escope': [('\tstruct fileent *e;\n\n\tfor (i = 0; ; i++) {', '\n\tfor (i = 0; ; i++) {\n\t\tstruct fileent *e;\n'),],
    'name': [('\t\tcase 23:\n\t\t\tstrcpy(e->name, fnPatches);\n', None)],
    'plainfor': [('\tfor (i = 0; ; i++) {\n\t\tif (i >= xb.nFiles)\n\t\t\tbreak;\n', '\tfor (i = 0; i < xb.nFiles; i++) {\n')],
    'ret': [('\t\tif (i >= xb.nFiles)\n\t\t\tbreak;\n', '\t\tif (i >= xb.nFiles)\n\t\t\treturn;\n')],
    'while': [('\tfor (i = 0; ; i++) {\n\t\tif (i >= xb.nFiles)\n\t\t\tbreak;\n', '\ti = -1;\n\twhile (++i < xb.nFiles) {\n')],
    'cn': [('strcat(e->name, consoleNames[xb.flags & CONSOLE_MASK]);\n\t\t\telse if (xb.glitch2) {', 'strcat(e->name, consoleNames[xb.flags & CONSOLE_MASK]);\n\t\t\telse if (xb.glitch2 != 0) {')],
    'e0': [('\t\tswitch (e->type) {\n', '\t\ti = i;\n\t\tswitch (e->type) {\n')],
    'gmatch': [('if (xb.glitch2mfg)\n\t\t\t\t\tstrcat(e->name, "g2m");\n\t\t\t\telse\n\t\t\t\t\tstrcat(e->name, "g2");\n', 'strcat(e->name, xb.glitch2mfg ? "g2m" : "g2");\n')],
    'chain': [('\t\t\tif (xb.type == BUILD_JTAG) {\n\t\t\te->type', '\t\t\tif (xb.type == BUILD_JTAG) {\n\t\t\te->type')],
}
del SFX['name'], SFX['chain']
AX = {'pos': list(POS), 'decl': list(DECL), 'mc': list(MC), 'ms': list(MS), 'msh': list(MSH), 'sf': list(SFX)}


def build(st, tests=(), kf=True, base=None):
    s = base if base is not None else F.gen(tests, kf)
    s = L.sub(s, MC0, MC[st.get('mc', 'cur')])
    s = L.sub(s, MS_T, MS[st.get('ms', 'cur')])
    s = L.sub(s, MSH['cur'], MSH[st.get('msh', 'cur')])
    s = L.sub(s, FWD, DECL[st.get('decl', 'cur')])
    x = st.get('sf', 'cur')
    sf = SF_TEXT
    for o, n in SFX[x]:
        sf = L.sub(sf, o, n)
    p = st.get('pos', 'cur')
    if p == 'cur':
        s = L.sub(s, SF_TEXT, sf)
    else:
        s = L.sub(s, SF_TEXT, '')
        a = POS[p]
        if s.count(a) != 1:
            raise ValueError(a)
        k = s.index(a)
        s = s[:k] + sf + s[k:]
        i = s.index('uint32_t parseIni(char *path)')
        if k > i:
            j = s.index('/* read the file list ini')
            s = s[:j] + 'static void setupFiles(void);\n\n' + s[j:]
    return s


def lab(st, t):
    return ','.join('%s=%s' % kv for kv in sorted(st.items())) + '|' + '+'.join(t)


if __name__ == '__main__':
    V = {}
    # one axis at a time, no tests
    for a, vs in AX.items():
        for v in vs:
            V[lab({a: v}, ())] = build({a: v})
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    r = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
    Tn = ['raw', 'off3', 'off4', 'x']
    while len(V) < n:
        st = {}
        for a, vs in AX.items():
            if r.random() < .35:
                st[a] = r.choice(vs)
        t = tuple(x for x in Tn if r.random() < .25)
        V[lab(st, t)] = build(st, t)
    print(len(V))
    F.run(V, 'b', show=30)
