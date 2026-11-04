"""fl6lib: attempt 6's generator on current src/filelist_ini.c (master 71b15324).

drop(s, 'T1,T2,T3,KF'): remove dead tests (T1 before strncpy firmware, T2 after the first strrchr (old off4),
T3 before the crc's tmp[8], KF findKey's key == NULL).
E: {axis: {value: fn(s)->s}} natural edits.  state('T1,T3|a=v,b=w') -> source: the part before | lists tests to DROP.
run(V, name): score {label: source} in parallel, log to build/filelist_ini/a6/<name>.txt.
python fl6lib.py <state>.. : scores and prints parseIni and getter diffs.
"""
import difflib, os, re, sys, threading
from concurrent.futures import ThreadPoolExecutor
import fllib as L

L.FLAGS[:] = ['-O3']
A6 = os.path.join(L.BD, 'a6')
os.makedirs(A6, exist_ok=True)
S0 = open(os.path.join(L.R, 'src', 'filelist_ini.c'), newline='').read()

T1C = ("\t\t\t\t/* this and the other two can't-happen tests in [flashfs] are dead, and steer gcc: what they free\n"
       "\t\t\t\t   sets [rawpatch]'s comma/nul compare and flashfs's copy order (notes/filelist_ini.md) */\n")
T1 = "\t\t\t\tif (off < -1) {\n\t\t\t\t\t*buf = 0;\n\t\t\t\t\tbuf[size] = 0;\n\t\t\t\t}\n"
T2 = "\t\t\t\t\tif (off < -1) {\n\t\t\t\t\t\t*buf = 0;\n\t\t\t\t\t}\n"
T3 = "\t\t\t\t\t\tif (off < 0) {\n\t\t\t\t\t\t\t*buf = 0;\n\t\t\t\t\t\t\tbuf[size] = 0;\n\t\t\t\t\t\t}\n"
KF = ("\t\t\t\t/* defensive, and dead (key was read above): VRP removes it, and\n"
      "\t\t\t\t   until then it sets findKey's SSA numbers in the getters (a register tie) */\n"
      "\t\t\t\tif (key == NULL)\n\t\t\t\t\treturn -1;\n")
DROPS = {'T1': T1C + T1, 'T2': T2, 'T3': T3, 'KF': KF}
for k, v in DROPS.items():
    assert S0.count(v) == 1, k


def drop(s, names):
    for n in names:
        if n:
            s = L.sub(s, DROPS[n], '')
    return s


HEAD = '/* read the file list ini: the files for this build type'


def helper(s, text):
    h = s.index(HEAD)
    return s[:h] + text + '\n' + s[h:]


SECS = {
    'bl': ('\t/* [<console>bl<blSuffix>]', '\tif (xb.type != BUILD_JTAG && xb.type <= BUILD_DEVGL16) {\n'),
    'raw': ('\t/* [rawpatch]: name,offset */\n', '\t/* [flashfs]: name[,crc]'),
    'flash': ('\t/* [flashfs]: name[,crc]', '\t/* [security]: name[,crc] */\n'),
    'sec': ('\t/* [security]: name[,crc] */\n', '\tfree(buf);\n\tlog_printf(1, "------ ini parsing completed'),
}


def secsub(s, sec, old, new, count=1):
    a, b = SECS[sec]
    i, j = s.index(a), s.index(b)
    return s[:i] + L.sub(s[i:j], old, new, count) + s[j:]


# ---- [`-search: all three sections
ENDL = "end = off + memFindChar(&buf[off], '[', size - off);"


def sect_ret(s):
    s = helper(s, "/* end of the section starting at off */\nstatic int sectionEnd(unsigned char *buf, int size, int off)\n{\n\treturn off + memFindChar(&buf[off], '[', size - off);\n}\n")
    return L.sub(s, ENDL, 'end = sectionEnd(buf, size, off);', 3)


def sect_out(s):
    s = L.sub(s, ENDL, 'sectionEnd(buf, size, off, &end);', 3)
    return helper(s, "static void sectionEnd(unsigned char *buf, int size, int off, int *end)\n{\n\t*end = off + memFindChar(&buf[off], '[', size - off);\n}\n")


def sect_raw(fn):
    """only [rawpatch], returning"""
    def f(s):
        s = helper(s, fn)
        return secsub(s, 'raw', ENDL, 'end = sectionEnd(buf, size, off);')
    return f


def sect_len(s):
    """length of the section, end = off + ..."""
    s = helper(s, "static int sectionLen(unsigned char *p, int rem)\n{\n\treturn memFindChar(p, '[', rem);\n}\n")
    return L.sub(s, ENDL, "end = off + sectionLen(&buf[off], size - off);", 3)


def sect_pos(s):
    """pos and end together"""
    s = helper(s, "static void sectionRange(unsigned char *buf, int size, int off, int *pos, int *end)\n{\n\t*end = off + memFindChar(&buf[off], '[', size - off);\n\t*pos = off;\n}\n")
    for sec in ('bl', 'sec'):
        s = secsub(s, sec, ENDL + '\n\t\tpos = off;\n', 'sectionRange(buf, size, off, &pos, &end);\n')
    s = secsub(s, 'raw', ENDL + '\n', 'sectionRange(buf, size, off, &pos, &end);\n')
    s = secsub(s, 'raw', '\t\tpos = off;\n', '')
    return s


# ---- rawPatch entry
def rawent(kind):
    def f(s):
        a, b = SECS['raw']
        i, j = s.index(a), s.index(b)
        t = s[i:j]
        if kind == 'name':  # char *name local
            t = L.sub(t, '\t\t\tp = &buf[pos];\n', '\t\t\tchar *name = xb.rawPatch[i].name;\n\n\t\t\tp = &buf[pos];\n')
            t = t.replace('xb.rawPatch[i].name', 'name').replace('char *name = name', 'char *name = xb.rawPatch[i].name')
        if kind == 'off':  # uint32_t offset local
            t = L.sub(t, 'xb.rawPatch[i].offset = myatou32(tmp, -1);\n\t\t\t\tif (xb.rawPatch[i].offset != (uint32_t)-1)',
                      'val = myatou32(tmp, -1);\n\t\t\t\txb.rawPatch[i].offset = val;\n\t\t\t\tif (val != (uint32_t)-1)')
            t = L.sub(t, '\t\t\tp = &buf[pos];\n', '\t\t\tuint32_t val;\n\n\t\t\tp = &buf[pos];\n')
        if kind == 'ptr':  # pointer to the entry
            t = L.sub(t, '\t\t\tp = &buf[pos];\n', '\t\t\ttypeof(&xb.rawPatch[0]) r = &xb.rawPatch[i];\n\n\t\t\tp = &buf[pos];\n')
            t = t.replace('xb.rawPatch[i].', 'r->')
        return s[:i] + t + s[j:]
    return f


# ---- copy helper
def copyname(secs):
    def f(s):
        s = helper(s, "/* len bytes of name, terminated */\nstatic void copyName(char *dst, const unsigned char *src, int len)\n{\n\tstrncpy(dst, (const char *)src, len);\n\tdst[len] = 0;\n}\n")
        if 'b' in secs:
            s = secsub(s, 'bl', "strncpy(xb.files[blOrder[i]].name, (char *)p, len);\n\t\t\txb.files[blOrder[i]].name[len] = 0;", "copyName(xb.files[blOrder[i]].name, p, len);")
        if 'r' in secs:
            s = secsub(s, 'raw', "strncpy(xb.rawPatch[i].name, (char *)p, comma);\n\t\t\t\txb.rawPatch[i].name[comma] = 0;", "copyName(xb.rawPatch[i].name, p, comma);")
        if 'f' in secs:
            s = secsub(s, 'flash', "strncpy(xb.firmware[i], (char *)p, len);\n\t\t\t\txb.firmware[i][len] = 0;", "copyName(xb.firmware[i], p, len);")
        if 's' in secs:
            s = secsub(s, 'sec', "strncpy(xb.flashFiles[i], (char *)p, len);\n\t\t\t\txb.flashFiles[i][len] = 0;", "copyName(xb.flashFiles[i], p, len);")
        return s
    return f


def copyadv(secs):
    """copy and advance pos through a pointer"""
    def f(s):
        s = helper(s, "/* the name at *pos, terminated; moves *pos past its separator */\nstatic void takeName(char *dst, unsigned char *buf, int *pos, int len)\n{\n\tstrncpy(dst, (char *)&buf[*pos], len);\n\tdst[len] = 0;\n\t*pos = *pos + len + 1;\n}\n")
        if 'b' in secs:
            s = secsub(s, 'bl', "strncpy(xb.files[blOrder[i]].name, (char *)p, len);\n\t\t\txb.files[blOrder[i]].name[len] = 0;\n\t\t\tpos = pos + len + 1;", "takeName(xb.files[blOrder[i]].name, buf, &pos, len);")
        if 'r' in secs:
            s = secsub(s, 'raw', "strncpy(xb.rawPatch[i].name, (char *)p, comma);\n\t\t\t\txb.rawPatch[i].name[comma] = 0;\n\t\t\t\tpos = pos + comma + 1;", "takeName(xb.rawPatch[i].name, buf, &pos, comma);")
        if 's' in secs:
            s = secsub(s, 'sec', "strncpy(xb.flashFiles[i], (char *)p, len);\n\t\t\t\txb.flashFiles[i][len] = 0;\n\t\t\t\tpos = pos + len + 1;", "takeName(xb.flashFiles[i], buf, &pos, len);")
        return s
    return f


# ---- digits/crc field readers
def readtmp(secs):
    """copy n bytes at pos to tmp"""
    def f(s):
        s = helper(s, "/* n bytes of a value, as a string in tmp */\nstatic void copyValue(char *tmp, unsigned char *src, int n)\n{\n\tstrncpy(tmp, (char *)src, n);\n\ttmp[n] = 0;\n}\n")
        if 'b' in secs:
            s = secsub(s, 'bl', "strncpy(tmp, (char *)&buf[pos], 8);\n\t\t\t\t\ttmp[8] = 0;", "copyValue(tmp, &buf[pos], 8);")
        if 'r' in secs:
            s = secsub(s, 'raw', "strncpy(tmp, (char *)&buf[pos], n);\n\t\t\t\ttmp[n] = 0;", "copyValue(tmp, &buf[pos], n);")
        if 'f' in secs:
            s = secsub(s, 'flash', "strncpy(tmp, (char *)&buf[pos], 8);\n\t\t\t\t\t\ttmp[8] = 0;", "copyValue(tmp, &buf[pos], 8);")
        if 's' in secs:
            s = secsub(s, 'sec', "strncpy(tmp, (char *)&buf[pos], 8);\n\t\t\t\t\t\ttmp[8] = 0;", "copyValue(tmp, &buf[pos], 8);")
        return s
    return f


def fieldlen(secs):
    """memFindChar(&buf[pos], 0, size - pos) as a helper"""
    N = "n = memFindChar(&buf[pos], 0, size - pos);"

    def f(s):
        s = helper(s, "/* length of the string at pos */\nstatic int fieldLen(unsigned char *buf, int size, int pos)\n{\n\treturn memFindChar(&buf[pos], 0, size - pos);\n}\n")
        for c, sec in (('b', 'bl'), ('r', 'raw'), ('f', 'flash'), ('s', 'sec')):
            if c in secs:
                s = secsub(s, sec, N, "n = fieldLen(buf, size, pos);")
        return s
    return f


# ---- findField placement.  Current src has findField for sec.
FF = ("/* an entry's name,crc separators.  Called once, so inlined after parseIni's own names are numbered, and the\n"
      "   loads and stores of *comma and *nul only go after that: it sets [security]'s compare order and takes the\n"
      "   place of the dead tests that did (notes/filelist_ini.md) */\n"
      "static void findField(unsigned char *p, int rem, int *comma, int *nul)\n{\n\t*comma = memFindChar(p, ',', rem);\n\t*nul = memFindChar(p, 0, rem);\n}\n\n")
assert S0.count(FF) == 1
CFIRST = "\t\t\tcomma = memFindChar(p, ',', size - pos);\n\t\t\tnul = memFindChar(p, 0, size - pos);\n"
NFIRST = "\t\t\tnul = memFindChar(p, 0, size - pos);\n\t\t\tcomma = memFindChar(p, ',', size - pos);\n"
CALL = "\t\t\tfindField(p, size - pos, &comma, &nul);\n"


def ffbl(s):
    return secsub(s, 'bl', CFIRST, CALL)


def ffinline(s):
    s = L.sub(s, FF, '')
    return secsub(s, 'sec', CALL, CFIRST)


def ffn(secs, nm='findFieldN'):
    """a nul-first helper for raw and/or flash"""
    def f(s):
        s = helper(s, "static void %s(unsigned char *p, int rem, int *comma, int *nul)\n{\n\t*nul = memFindChar(p, 0, rem);\n\t*comma = memFindChar(p, ',', rem);\n}\n" % nm)
        for c, sec in (('r', 'raw'), ('f', 'flash')):
            if c in secs:
                s = secsub(s, sec, NFIRST, "\t\t\t%s(p, size - pos, &comma, &nul);\n" % nm)
        return s
    return f


def ffret(s):
    """rawpatch: nul out, returns comma"""
    s = helper(s, "static int findComma(unsigned char *p, int rem, int *nul)\n{\n\t*nul = memFindChar(p, 0, rem);\n\treturn memFindChar(p, ',', rem);\n}\n")
    return secsub(s, 'raw', NFIRST, "\t\t\tcomma = findComma(p, size - pos, &nul);\n")


def prein(s):
    """preParse inline again"""
    a = s.index('/* the terminators around iniPreParse.')
    b = s.index('/* the files this build type uses.')
    s = s[:a] + s[b:]
    return L.sub(s, "\tsize = preParse(buf, size);\n", "\tbuf[size] = 0xff;\n\tsize = iniPreParse(buf, size);\n\tbuf[size] = 0;\n")


E = {
    'sect': {'r': sect_ret, 'o': sect_out, 'l': sect_len, 'p': sect_pos,
             'R': sect_raw("static int sectionEnd(unsigned char *buf, int size, int off)\n{\n\treturn off + memFindChar(&buf[off], '[', size - off);\n}\n")},
    'ent': {'name': rawent('name'), 'off': rawent('off'), 'ptr': rawent('ptr')},
    'copy': {x: copyname(x) for x in ('brfs', 'r', 'rf', 'brs', 'bs', 'f', 'fs', 's', 'b', 'rs', 'br')},
    'adv': {x: copyadv(x) for x in ('brs', 'r', 'bs', 's', 'b', 'rs', 'br')},
    'val': {x: readtmp(x) for x in ('brfs', 'r', 'brs', 'bfs', 'f', 'rf')},
    'flen': {x: fieldlen(x) for x in ('brfs', 'r', 'rf', 'f', 'bs', 'brs', 'fs', 's', 'b')},
    'ff': {'bl': ffbl, 'none': ffinline, 'r': ffn('r'), 'f': ffn('f'), 'rf': ffn('rf'), 'ret': ffret,
           'blrf': lambda s: ffn('rf')(ffbl(s))},
    'pre': {'in': prein},
}
# order axes are applied in
ORDER = ['pre', 'ff', 'copy', 'adv', 'val', 'flen', 'ent', 'sect']


def state(lb):
    d, _, a = lb.partition('|')
    s = drop(S0, [x for x in d.split(',') if x])
    c = dict(x.split('=') for x in a.split(',') if x)
    for k in ORDER:
        if k in c:
            s = E[k][c[k]](s)
    for k in c:
        if k not in ORDER:
            s = E[k][c[k]](s)
    return s


def norm(d):
    return {k: [re.sub(r' \.-?[0-9a-f]+$', ' .', x) for x in v] for k, v in d.items()}


_rn = {}


def nscore(o, sc=None):
    sc = sc or L.score(o)
    if sc[0] == 0:
        return 0
    if not _rn:
        _rn.update(norm(L.dis(L.REF)))
    d = norm(L.dis(o))
    n = 0
    for k, v in _rn.items():
        w = d.get(k, [])
        if v != w:
            n += sum(1 for x in difflib.ndiff(v, w) if x[0] in '+-')
    return n + (0.5 if not n or sc[3] else 0)


_loc = threading.local()
_cnt = [0]
_lock = threading.Lock()


def one(kv):
    if not hasattr(_loc, 'id'):
        with _lock:
            _cnt[0] += 1
            _loc.id = _cnt[0]
    n, s = kv
    o = L.compile(s, None, 'a6_%d_%d' % (os.getpid(), _loc.id))
    if o is None:
        return 10**7, {}, [], n
    sc = L.score(o)
    return nscore(o, sc), sc[2], sc[3], n


def run(V, name, show=20):
    with ThreadPoolExecutor(4) as ex:
        rs = sorted(ex.map(one, V.items()), key=lambda r: r[0])
    with open(os.path.join(A6, name + '.txt'), 'a', newline='\n') as f:
        for r in rs:
            f.write('%s\t%s\t%s\t%s\n' % r)
    for r in rs[:show]:
        print(r)
    print('MATCH', [r[3] for r in rs if r[0] == 0][:40])
    return rs


def show(lb, fns=('parseIni',)):
    s = state(lb)
    open(os.path.join(A6, 'show.c'), 'w', newline='\n').write(s)
    o = L.compile(s, None, 'a6show')
    print('==', lb, nscore(o), L.score(o)[2:])
    A, B = norm(L.dis(L.REF)), norm(L.dis(o))
    for k in A:
        if A[k] != B.get(k):
            print('--', k)
            print('\n'.join(l for l in difflib.unified_diff(A[k], B.get(k, []), lineterm='', n=0) if not l.startswith(('---', '+++'))))


if __name__ == '__main__':
    for lb in sys.argv[1:]:
        show(lb)
