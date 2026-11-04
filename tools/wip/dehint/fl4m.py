"""fl4m.py single|rand N seed [tests]: more natural helpers, mostly called once, near [flashfs] and before it, at fl4f's base."""
import random, re, sys
import fllib as L, fl4lib as F, fl4d as D, fl4f as B, fl4g as G

AX = {}


def split(s):
    k = s.index('uint32_t parseIni')
    return s[:k], s[k:]


def helper(s, h):
    return D.add_helper(s, h)


def basen(s):
    old = re.search(r"\t+s = strrchr\(xb\.firmware\[i\], '/'\);\n(?:.*\n)*?\t+s = s \? s \+ 1 : xb\.firmware\[i\];\n", s).group(0)
    # any test sites inside are dropped by callers that use this
    s = L.sub(s, old, '\t\t\t\t\ts = baseName(xb.firmware[i]);\n')
    return helper(s, "static char *baseName(char *path)\n{\n\tchar *s = strrchr(path, '/');\n\n\tif (s == NULL)\n\t\ts = strrchr(path, '\\\\');\n\treturn s ? s + 1 : path;\n}\n")


def strip(s):
    old = "\t\t\t\tif (xb.firmware[i][len - 1] == '1' || xb.firmware[i][len - 1] == '2')\n\t\t\t\t\txb.firmware[i][len - 1] = 0;\n"
    s = L.sub(s, old, '\t\t\t\tdropDigit(&xb.firmware[i][len - 1]);\n')
    return helper(s, "static void dropDigit(char *c)\n{\n\tif (*c == '1' || *c == '2')\n\t\t*c = 0;\n}\n")


def toolong(s):
    m = re.search(r"\t+if \(len > 21\) \{\n\t+s = strrchr\(xb\.firmware.*?\n\t+s = s \? s \+ 1 : xb\.firmware\[i\];\n\t+if \(strlen\(s\) > 21\) \{\n(.*?)\n\t+\}\n\t+\}\n", s, re.S)
    old = m.group(0)
    s = L.sub(s, old, '\t\t\t\tif (len > 21) {\n\t\t\t\t\tif (nameTooLong(xb.firmware[i])) {\n' + m.group(1) + '\n\t\t\t\t\t}\n\t\t\t\t}\n')
    return helper(s, "static int nameTooLong(char *path)\n{\n\tchar *s = strrchr(path, '/');\n\n\tif (s == NULL)\n\t\ts = strrchr(path, '\\\\');\n\ts = s ? s + 1 : path;\n\treturn strlen(s) > 21;\n}\n")


def hexs(which):
    def f(s):
        a, b = split(s)
        pats = re.compile(r'strncpy\(tmp, \(char \*\)&buf\[pos\], 8\);\n\s*tmp\[8\] = 0;\n(\s*)((?:crc = )?\S+) = myatox32\(tmp, 0\);')
        ms = list(pats.finditer(b))
        assert len(ms) == 3
        out, last = [], 0
        for i, m in enumerate(ms):
            out.append(b[last:m.start()])
            if i in which:
                out.append('%s = crcValue(tmp, &buf[pos]);' % m.group(2))
            else:
                out.append(m.group(0))
            last = m.end()
        out.append(b[last:])
        return helper(a + ''.join(out), D.HEX)
    return f


def flens(which):
    def f(s):
        a, b = split(s)
        ms = list(re.finditer(r'n = memFindChar\(&buf\[pos\], 0, size - pos\);', b))
        out, last = [], 0
        for i, m in enumerate(ms):
            out.append(b[last:m.start()])
            out.append('n = fieldLen(buf, pos, size);' if i in which else m.group(0))
            last = m.end()
        out.append(b[last:])
        return helper(a + ''.join(out), D.FLEN)
    return f


def sects(which):
    def f(s):
        a, b = split(s)
        ms = list(re.finditer(r"end = off \+ memFindChar\(&buf\[off\], '\[', size - off\);", b))
        out, last = [], 0
        for i, m in enumerate(ms):
            out.append(b[last:m.start()])
            out.append('end = sectionEnd(buf, off, size);' if i in which else m.group(0))
            last = m.end()
        out.append(b[last:])
        return helper(a + ''.join(out), D.SECT)
    return f


LOADB = '''	log_printf(1, "\\n------ parsing ini at '%s' ------\\n", path);
'''


def load(s):
    i = s.index(LOADB)
    j = s.index('\t/* [version] */\n')
    H = s[i:j]
    s = s[:i] + '\tbuf = loadIni(path, &size);\n\tif (buf == NULL)\n\t\treturn 0;\n\n' + s[j:]
    H2 = H.replace('return 0;', 'return NULL;').replace('size = getFileSize(f);', 'size = getFileSize(f);')
    return helper(s, 'static unsigned char *loadIni(char *path, int *psize)\n{\n\tFILE *f;\n\tunsigned char *buf;\n\tint size;\n\n%s\t*psize = size;\n\treturn buf;\n}\n' % H2)


def tail(s):
    return s


def outname(s):
    old = '\txb.nFlashFiles = xb.nFiles - 2;\n\tstrcpy(xb.outName, tmp);\n'
    s = L.sub(s, old, '\tsetOutName(tmp);\n')
    return helper(s, 'static void setOutName(const char *name)\n{\n\txb.nFlashFiles = xb.nFiles - 2;\n\tstrcpy(xb.outName, name);\n}\n')


def preface(s):
    old = '\tbuf[size] = 0xff;\n\tsize = iniPreParse(buf, size);\n\tbuf[size] = 0;\n'
    s = L.sub(s, old, '\tsize = preParse(buf, size);\n')
    return helper(s, 'static int preParse(unsigned char *buf, int size)\n{\n\tbuf[size] = 0xff;\n\tsize = iniPreParse(buf, size);\n\tbuf[size] = 0;\n\treturn size;\n}\n')


AX = {
    'base': {'y': basen}, 'tool': {'y': toolong}, 'strip': {'y': strip},
    'hex': {'b': hexs([0]), 'f': hexs([1]), 's': hexs([2]), 'bf': hexs([0, 1]), 'fs': hexs([1, 2]), 'bs': hexs([0, 2])},
    'flen': {'b': flens([0]), 'r': flens([1]), 'f': flens([2]), 's': flens([3]), 'rf': flens([1, 2]), 'br': flens([0, 1])},
    'sect': {'b': sects([0]), 'r': sects([1]), 's': sects([2])},
    'load': {'y': load}, 'out': {'y': outname}, 'pre': {'y': preface},
    'label': {'y': D.label}, 'name': D.AX['name'], 'cbb': {'y': D.cbb}, 'ks': {'y': D.ks},
}
ORDER = list(AX)


def gen(c, base):
    s = base
    for a in ORDER:
        if a in c:
            if a == 'base' and 'tool' in c:
                continue
            s = AX[a][c[a]](s)
    return s


def lab(c):
    return ','.join('%s=%s' % (a, c[a]) for a in ORDER if a in c)


if __name__ == '__main__':
    mode = sys.argv[1]
    V = {}
    if mode == 'single':
        tests = sys.argv[2] if len(sys.argv) > 2 else ''
        base = G.mk(F.st(tests))
        V[''] = base
        for a in ORDER:
            for v in AX[a]:
                try:
                    V[lab({a: v})] = gen({a: v}, base)
                except (AttributeError, ValueError, AssertionError) as e:
                    print('skip', a, v, e)
    else:
        N, seed = int(sys.argv[2]), int(sys.argv[3])
        tests = sys.argv[4] if len(sys.argv) > 4 else ''
        base = G.mk(F.st(tests))
        ax = (sys.argv[5].split(',') if len(sys.argv) > 5 else ORDER)
        rng = random.Random(seed)
        t = 0
        while len(V) < N and t < N * 30:
            t += 1
            c = {}
            for a in ax:
                if rng.random() < 0.3:
                    c[a] = rng.choice(list(AX[a]))
            V[lab(c)] = gen(c, base)
    print(len(V))
    F.run(V, 'm', show=30)
