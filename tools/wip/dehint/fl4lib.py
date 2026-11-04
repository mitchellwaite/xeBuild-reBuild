"""fl4lib: attempt 4's generator, on current src.
gen(tests, secs, kf, ku, edits): parseIni with the dead tests in `tests` ({site: (cond, arm)}, sites nb i nul off3 off4 len x;
arm is a ';' list of stores) and the sections in `secs` moved to static functions called once.
Sections: files cbb ver bl raw flash sec.  secs maps a section to a mode: 'free' (helper frees, caller `if (!f()) return 0`).
Tie vector vec(o) as in fl3g.  run(V, name): parallel score, appends to build/filelist_ini/a4/<name>.txt."""
import difflib, os, re, threading
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import fllib as L

L.FLAGS[:] = ['-O3']
A4 = os.path.join(L.BD, 'a4')
os.makedirs(A4, exist_ok=True)
S0 = open(os.environ.get('FL4SRC') or os.path.join(L.R, 'src', 'filelist_ini.c'), newline='').read()

CUR = {'nb': ('nbl != 6 && nbl != 9', 'xb.nFiles = 0'), 'i': ('i < 0', 'xb.nRawPatches = 0'), 'nul': ('nul < -1', '*buf = 0'),
       'off3': ('off < -1', 'buf[size] = 0; *buf = 0'), 'off4': ('off < -1', '*buf = 0'), 'len': ('len < 0', '*buf = 0'),
       'x': ('off < 0', '*buf = 0; buf[1] = 0')}
SITES = ['nb', 'i', 'nul', 'off3', 'off4', 'len', 'x']
RX = re.compile(r'([ \t]*)if \((nbl != 6 && nbl != 9|i < 0|nul < -1|off < -1|len < 0|off < 0)\) \{\n((?:[ \t]*[^\n]*= 0;\n)+)[ \t]*\}\n')
_ms = list(RX.finditer(S0))
assert len(_ms) == 7, len(_ms)
_parts, _last = [], 0
INDENT = {}
for _n, _m in zip(SITES, _ms):
    _parts.append(S0[_last:_m.start()])
    _parts.append('@@%s@@' % _n)
    INDENT[_n] = _m.group(1)
    _last = _m.end()
_parts.append(S0[_last:])
MARKED = ''.join(_parts)
MARKED = re.sub(r'[ \t]*/\* this and the other can\'t-happen.*?\*/\n', '', MARKED, flags=re.S)


def test(name, cond, arm):
    ind = INDENT.get(name, '\t')
    a = ''.join('%s\t%s;\n' % (ind, x.strip()) for x in arm.split(';') if x.strip())
    return '%sif (%s) {\n%s%s}\n' % (ind, cond, a, ind)


def st(label):
    """'nb,len,nul,off4' or 'nb=2' etc. -> {site: (cond, arm)}: site's cond with its arm cut or padded to k stores"""
    r = {}
    if not label:
        return r
    for kv in label.split(','):
        n, _, k = kv.partition('=')
        c, a = CUR[n]
        if k:
            stores = ['*buf = 0', 'buf[size] = 0', 'buf[1] = 0', 'buf[2] = 0', 'buf[3] = 0', 'buf[4] = 0']
            a = '; '.join(stores[:int(k)])
        r[n] = (c, a)
    return r


# section boundaries in MARKED
MK = {
    'ver': ('\t/* [version] */\n', '\txb.nFlashFiles = xb.nFiles - 2;\n'),
    'files': ('\t/* the files this build type uses */\n', '\t/* [<console>bl<blSuffix>]'),
    'bl': ('\t/* [<console>bl<blSuffix>]', '\tif (xb.type != BUILD_JTAG && xb.type <= BUILD_DEVGL16) {\n'),
    'cbb': ('\tif (xb.type != BUILD_JTAG && xb.type <= BUILD_DEVGL16) {\n', '\t/* [rawpatch]: name,offset */\n'),
    'raw': ('\t/* [rawpatch]: name,offset */\n', '\t/* [flashfs]: name[,crc]'),
    'flash': ('\t/* [flashfs]: name[,crc]', '\t/* [security]: name[,crc] */\n'),
    'sec': ('\t/* [security]: name[,crc] */\n', '\tfree(buf);\n\tlog_printf(1, "------ ini parsing completed'),
}
FN = {
    'files': ('static void setupFiles(void)', 'setupFiles();', 'int i;\n\tstruct fileent *e;\n'),
    'cbb': ('static void setCbb(void)', 'setCbb();', ''),
    'bl': ('static int parseBl(unsigned char *buf, int size, int nbl, char *tmp)', 'if (!parseBl(buf, size, nbl, tmp))\n\t\treturn 0;',
           'unsigned char *p;\n\tint off, end, pos, len, nul, comma, n, i;\n\tuint32_t noCrc;\n\tchar label[50];\n'),
    'raw': ('static int parseRawpatch(unsigned char *buf, int size, char *tmp)', 'if (!parseRawpatch(buf, size, tmp))\n\t\treturn 0;',
            'unsigned char *p;\n\tint off, end, pos, nul, comma, n, i;\n'),
    'flash': ('static int parseFlashfs(unsigned char *buf, int size, char *tmp)', 'if (!parseFlashfs(buf, size, tmp))\n\t\treturn 0;',
              'unsigned char *p;\n\tint off, pos, len, nul, comma, n, i;\n\tuint32_t noCrc;\n\tchar *s;\n\tuint32_t crc;\n'),
    'sec': ('static int parseSecurity(unsigned char *buf, int size, char *tmp)', 'if (!parseSecurity(buf, size, tmp))\n\t\treturn 0;',
            'unsigned char *p;\n\tint off, end, pos, len, nul, comma, n, i;\n\tuint32_t noCrc;\n'),
}
HEAD = '/* read the file list ini: the files for this build type'


def gen(tests=None, secs=(), kf=True, ku=True, edits=()):
    s = MARKED
    helpers = ''
    for k in ['files', 'bl', 'cbb', 'raw', 'flash', 'sec']:
        if k not in secs:
            continue
        a, b = MK[k]
        i, j = s.index(a), s.index(b)
        body = s[i:j]
        sig, call, decl = FN[k]
        ret = ''
        if sig.startswith('static int'):
            ret = '\treturn 1;\n'
        helpers += '%s\n{\n\t%s\n%s%s}\n\n' % (sig, decl, body, ret)
        s = s[:i] + '\t' + call + '\n' + s[j:]
    h = s.index(HEAD)
    s = s[:h] + helpers + s[h:]
    tests = tests or {}
    for n in SITES:
        s = s.replace('@@%s@@' % n, test(n, *tests[n]) if n in tests else '')
    KF = '\t\t\t\t/* defensive, and dead (key was read above): VRP removes it, and\n\t\t\t\t   until then it sets findKey\'s SSA numbers in the getters */\n\t\t\t\tif (key == NULL)\n\t\t\t\t\treturn -1;\n'
    KU = '\t/* defensive and dead, as in findKey: sets the order of this function\'s\n\t   buf[i]/key[0] compare */\n\tif (key == NULL)\n\t\treturn NULL;\n'
    if not kf:
        s = L.sub(s, KF, '')
    if not ku:
        s = L.sub(s, KU, '')
    for o, n in edits:
        s = L.sub(s, o, n)
    return s


T1 = ('cmp    edx,ebx', 'mov    DWORD PTR [esp+0x34],0x1', 'jle')
T2 = 'lea    ebp,[ebx+ebp*1+0x1]'
T3 = ('mov    ebx,0xffffffff', 'xor    edi,edi')


def vec(o):
    d = L.dis(o).get('_parseIni', [])
    t1 = any(d[i] == T1[0] and d[i + 1] == T1[1] and d[i + 2].startswith(T1[2]) for i in range(len(d) - 2))
    t2 = T2 in d
    t3 = any(d[i] == T3[0] and d[i + 1] == T3[1] for i in range(len(d) - 1))
    return ('1' if t1 else '-') + ('2' if t2 else '-') + ('3' if t3 else '-')


_rn = {}


def norm(d):
    return {k: [re.sub(r' \.-?[0-9a-f]+$', ' .', x) for x in v] for k, v in d.items()}


def nscore(o, sc=None):
    """diff lines with branch targets blanked, so one size change doesn't count everywhere; 0 only for a whole-object match"""
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
    o = L.compile(s, None, 'a4_%d' % _loc.id)
    if o is None:
        return 10**7, '', {}, [], n
    sc = L.score(o)
    return nscore(o, sc), vec(o), sc[2], sc[3], n


def run(V, name, show=20):
    with ThreadPoolExecutor(4) as ex:
        rs = sorted(ex.map(one, V.items()), key=lambda r: r[0])
    with open(os.path.join(A4, name + '.txt'), 'a', newline='\n') as f:
        for r in rs:
            f.write('%s\t%s\t%s\t%s\t%s\n' % r)
    print(Counter((r[0], r[1]) for r in rs if r[0] < 30).most_common(8))
    for r in rs[:show]:
        print(r)
    print('MATCH', [r[4] for r in rs if r[0] == 0][:40])
    return rs


if __name__ == '__main__':
    assert L.same(L.compile(gen(CUR), None, 'a4base')), 'base must match'
    print('base MATCH')
