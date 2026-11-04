"""fl4d.py [N seed]: at the `files` helper, no dead tests: natural helper edits in combination.
gen(choice) -> source.  Without args: each axis value alone, then N random combinations."""
import itertools, random, re, sys
import fllib as L, fl4lib as F

BASE = F.gen({}, ('files',))
PRE = 'static void setupFiles(void)\n{\n\tint i;\n\tstruct fileent *e;\n\n'


def rep_all(s, old, new):
    assert old in s, old[:50]
    return s.replace(old, new)


def add_helper(s, h):
    k = s.index('static void setupFiles(void)')
    return s[:k] + h + '\n' + s[k:]


AX = {}


def ax(name):
    def deco(f):
        AX[name] = f
        return f
    return deco


# forms of setupFiles
FOR = '\tfor (i = 0; i < xb.nFiles; i++) {\n\t\te = &xb.files[i];\n'


def w_gt(s):
    return L.sub(s, FOR, '\tfor (i = 0; xb.nFiles > i; i++) {\n\t\te = &xb.files[i];\n')


def w_scope(s):
    s = L.sub(s, FOR, '\tfor (i = 0; i < xb.nFiles; i++) {\n\t\tstruct fileent *e = &xb.files[i];\n\n')
    return L.sub(s, 'static void setupFiles(void)\n{\n\tint i;\n\tstruct fileent *e;\n', 'static void setupFiles(void)\n{\n\tint i;\n')


def w_while(s):
    s = L.sub(s, FOR, '\ti = 0;\n\twhile (i < xb.nFiles) {\n\t\te = &xb.files[i];\n')
    k = s.index('strcpy(e->name, fnSmcConfig);')
    k2 = s.index('\t\t}\n\t}\n', k)
    return s[:k2] + '\t\t}\n\t\ti++;\n\t}\n' + s[k2 + len('\t\t}\n\t}\n'):]


def w_param(s):
    s = L.sub(s, 'static void setupFiles(void)', 'static void setupFiles(struct fileent *files)')
    s = L.sub(s, FOR, '\tfor (i = 0; i < xb.nFiles; i++) {\n\t\te = &files[i];\n')
    return L.sub(s, 'setupFiles();', 'setupFiles(xb.files);')


def w_n(s):
    s = L.sub(s, 'static void setupFiles(void)', 'static void setupFiles(int type)')
    k = s.index('static void setupFiles'); k2 = s.index('uint32_t parseIni')
    b = s[k:k2].replace('xb.type', 'type')
    s = s[:k] + b + s[k2:]
    return L.sub(s, 'setupFiles();', 'setupFiles(xb.type);')


AX['w'] = {'gt': w_gt, 'scope': w_scope, 'while': w_while, 'param': w_param, 'type': w_n}

FAIL = 'static uint32_t iniFail(unsigned char *buf)\n{\n\tfree(buf);\n\treturn 0;\n}\n'


def fail(s):
    k = s.index('uint32_t parseIni')
    a, b = s[:k], s[k:]
    b = re.sub(r'free\(buf\);\n\s*return 0;', 'return iniFail(buf);', b)
    return add_helper(a + b, FAIL)


NAME = 'static void copyName(char *dst, unsigned char *p, int len)\n{\n\tstrncpy(dst, (char *)p, len);\n\tdst[len] = 0;\n}\n'


def name(which):
    def f(s):
        k = s.index('uint32_t parseIni')
        a, b = s[:k], s[k:]
        pat = {'bl': r'strncpy\((xb\.files\[blOrder\[i\]\]\.name), \(char \*\)p, (len)\);\n\s*\S+ = 0;',
               'raw': r'strncpy\((xb\.rawPatch\[i\]\.name), \(char \*\)p, (comma)\);\n\s*\S+ = 0;',
               'fl': r'strncpy\((xb\.firmware\[i\]), \(char \*\)p, (len)\);\n\s*\S+ = 0;',
               'sec': r'strncpy\((xb\.flashFiles\[i\]), \(char \*\)p, (len)\);\n\s*\S+ = 0;'}
        for w in which:
            b, c = re.subn(pat[w], lambda m: 'copyName(%s, p, %s);' % (m.group(1), m.group(2)), b)
            assert c == 1, w
        return add_helper(a + b, NAME)
    return f


HEX = 'static uint32_t crcValue(char *tmp, unsigned char *p)\n{\n\tstrncpy(tmp, (char *)p, 8);\n\ttmp[8] = 0;\n\treturn myatox32(tmp, 0);\n}\n'


def hexv(s):
    k = s.index('uint32_t parseIni')
    a, b = s[:k], s[k:]
    b, c = re.subn(r'strncpy\(tmp, \(char \*\)&buf\[pos\], 8\);\n\s*tmp\[8\] = 0;\n(\s*)((?:crc = )?\S+) = myatox32\(tmp, 0\);',
                   lambda m: '%s = crcValue(tmp, &buf[pos]);' % m.group(2), b)
    assert c == 3
    return add_helper(a + b, HEX)


FLEN = 'static int fieldLen(unsigned char *buf, int pos, int size)\n{\n\treturn memFindChar(&buf[pos], 0, size - pos);\n}\n'


def flen(s):
    k = s.index('uint32_t parseIni')
    a, b = s[:k], s[k:]
    b, c = re.subn(r'n = memFindChar\(&buf\[pos\], 0, size - pos\);', 'n = fieldLen(buf, pos, size);', b)
    assert c == 4
    return add_helper(a + b, FLEN)


SECT = 'static int sectionEnd(unsigned char *buf, int off, int size)\n{\n\treturn off + memFindChar(&buf[off], \'[\', size - off);\n}\n'


def sect(s):
    k = s.index('uint32_t parseIni')
    a, b = s[:k], s[k:]
    b, c = re.subn(r"end = off \+ memFindChar\(&buf\[off\], '\[', size - off\);", 'end = sectionEnd(buf, off, size);', b)
    assert c == 3
    return add_helper(a + b, SECT)


def split(fn):
    """a helper used for one error log"""
    return fn


def label(s):
    i = s.index('\tif (xb.blSuffix[0])\n\t\tsprintf(label')
    j = s.index('\toff = memFindStr(buf, size, label, 1);')
    LB = s[i:j]
    s = s[:i] + '\tblLabel(label);\n' + s[j:]
    return add_helper(s, 'static void blLabel(char *label)\n{\n%s}\n' % LB)


def cbb(s):
    a, b = F.MK['cbb']
    i, j = s.index(a), s.index(b)
    B = s[i:j]
    s = s[:i] + '\tsetCbb();\n\n' + s[j:]
    return add_helper(s, 'static void setCbb(void)\n{\n%s}\n' % B)


def ks(s):
    i = s.index('\t\tmemset(xb.kernelStr, 0')
    j = s.index('\t\tlog_printf(1, "ini version %s')
    KS = s[i:j]
    s = s[:i] + '\t\tsetKernelStr(&buf[off]);\n' + s[j:]
    return add_helper(s, 'static void setKernelStr(unsigned char *p)\n{\n\tint len;\n\n%s}\n' % KS.replace('&buf[off]', 'p'))


def after(s):
    """setupFiles after parseIni, declared before"""
    k = s.index('static void setupFiles(void)')
    k2 = s.index(F.HEAD)
    H = s[k:k2]
    s = s[:k] + 'static void setupFiles(void);\n\n' + s[k2:]
    m = s.index('/* offset of the value after `key` in buf, or -1 */')
    return s[:m] + H + s[m:]


AX = {'w': AX['w'], 'fail': {'y': fail}, 'name': {'all': name(['bl', 'raw', 'fl', 'sec']), 'bl': name(['bl']), 'raw': name(['raw']), 'fl': name(['fl']), 'sec': name(['sec']), 'blsec': name(['bl', 'sec'])},
      'hex': {'y': hexv}, 'flen': {'y': flen}, 'sect': {'y': sect}, 'label': {'y': label}, 'cbb': {'y': cbb}, 'ks': {'y': ks}, 'after': {'y': after}}
ORDER = ['w', 'after', 'fail', 'name', 'hex', 'flen', 'sect', 'label', 'cbb', 'ks']


def gen(c, base=None):
    s = base or BASE
    for a in ORDER:
        if a in c:
            s = AX[a][c[a]](s)
    return s


def lab(c):
    return ','.join('%s=%s' % (a, c[a]) for a in ORDER if a in c)


if __name__ == '__main__':
    V = {'': BASE}
    for a in ORDER:
        for v in AX[a]:
            V[lab({a: v})] = gen({a: v})
    if len(sys.argv) > 1:
        N, seed = int(sys.argv[1]), int(sys.argv[2])
        rng = random.Random(seed)
        while len(V) < N:
            c = {}
            for a in ORDER:
                if rng.random() < 0.3:
                    c[a] = rng.choice(list(AX[a]))
            V[lab(c)] = gen(c)
    print(len(V))
    F.run(V, 'd', show=40)
