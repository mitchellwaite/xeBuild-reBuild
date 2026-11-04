"""fl5lib: attempt 5's generator on current src/filelist_ini.c.

gen(tests, kf, helpers, edits):
  tests: which of raw off3 off4 x (the parseIni dead tests) stay
  kf: findKey's `key == NULL` stays
  helpers: {section: form}; a section is bl cbb raw flash sec (the whole section), or blL rawL flashL secL (only its loop,
    label check and not-found stay in the caller), or flashB rawB blB secB (one entry per call, returning pos or -1).
    A form is a string of letters:
      f  free(buf) stays in the helper (default: caller frees)
      u  returns uint32_t rather than int
      t  tmp is local to the helper (default: parameter)
      1  test-first loop form (for (i = 0; ; i++) { if (i >= N) break; ...)
      b  `break` instead of `i = N` at the loop end
  One-letter helper names are not used; run(V, name) scores in parallel and logs to build/filelist_ini/a5/<name>.txt.
"""
import difflib, os, re, threading
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import fllib as L

L.FLAGS[:] = ['-O3']
A5 = os.path.join(L.BD, 'a5')
os.makedirs(A5, exist_ok=True)
S0 = open(os.path.join(L.R, 'src', 'filelist_ini.c'), newline='').read()

# markers for the dead tests
TESTS = {
    'raw': ("\t\t\t/* this and the three can't-happen tests in [flashfs] are dead, and steer gcc: what they free\n"
            "\t\t\t   sets flashfs's threaded copy order and its comma/nul compare (notes/filelist_ini.md) */\n"
            "\t\t\tif (off < -1) {\n\t\t\t\t*buf = 0;\n\t\t\t}\n\t\t\tif (pos >= end)\n",
            "\t\t\tif (off < -1) {\n\t\t\t\t*buf = 0;\n\t\t\t}\n"),
    'off3': ("\t\t\t\tif (off < -1) {\n\t\t\t\t\t*buf = 0;\n\t\t\t\t\tbuf[size] = 0;\n\t\t\t\t}\n\t\t\t\tif (len > 21) {\n",
             "\t\t\t\tif (off < -1) {\n\t\t\t\t\t*buf = 0;\n\t\t\t\t\tbuf[size] = 0;\n\t\t\t\t}\n"),
    'off4': ("\t\t\t\t\tif (off < -1) {\n\t\t\t\t\t\t*buf = 0;\n\t\t\t\t\t}\n\t\t\t\t\tif (s == NULL)\n",
             "\t\t\t\t\tif (off < -1) {\n\t\t\t\t\t\t*buf = 0;\n\t\t\t\t\t}\n"),
    'x': ("\t\t\tif (off < 0) {\n\t\t\t\t*buf = 0;\n\t\t\t}\n\t\t\tif (pos >= size)\n",
          "\t\t\tif (off < 0) {\n\t\t\t\t*buf = 0;\n\t\t\t}\n"),
}
TAIL = {'raw': '\t\t\tif (pos >= end)\n', 'off3': '\t\t\t\tif (len > 21) {\n', 'off4': '\t\t\t\t\tif (s == NULL)\n', 'x': '\t\t\tif (pos >= size)\n'}
KF = ("\t\t\t\t/* defensive, and dead (key was read above): VRP removes it, and\n"
      "\t\t\t\t   until then it sets findKey's SSA numbers in the getters (a register tie) */\n"
      "\t\t\t\tif (key == NULL)\n\t\t\t\t\treturn -1;\n")
assert S0.count(KF) == 1

MARKED = S0
for k, (whole, t) in TESTS.items():
    assert MARKED.count(whole) == 1, k
    MARKED = MARKED.replace(whole, '@@%s@@' % k + TAIL[k])

# section boundaries
MK = {
    'bl': ('\t/* [<console>bl<blSuffix>]', '\tif (xb.type != BUILD_JTAG && xb.type <= BUILD_DEVGL16) {\n'),
    'cbb': ('\tif (xb.type != BUILD_JTAG && xb.type <= BUILD_DEVGL16) {\n', '\t/* [rawpatch]: name,offset */\n'),
    'raw': ('\t/* [rawpatch]: name,offset */\n', '\t/* [flashfs]: name[,crc]'),
    'flash': ('\t/* [flashfs]: name[,crc]', '\t/* [security]: name[,crc] */\n'),
    'sec': ('\t/* [security]: name[,crc] */\n', '\tfree(buf);\n\tlog_printf(1, "------ ini parsing completed'),
}
HEAD = '/* read the file list ini: the files for this build type'
NAMES = {'bl': 'parseBl', 'cbb': 'setCbb', 'raw': 'parseRawpatch', 'flash': 'parseFlashfs', 'sec': 'parseSecurity'}
# locals each section uses, if declared in a helper
LOCALS = {
    'bl': 'unsigned char *p;\n\tint off, end, pos, len, nul, comma, n, i;\n\tuint32_t noCrc;\n\tchar label[50];\n',
    'raw': 'unsigned char *p;\n\tint off, end, pos, nul, comma, n, i;\n',
    'flash': 'unsigned char *p;\n\tint off, pos, len, nul, comma, n, i;\n\tuint32_t noCrc;\n\tchar *s;\n\tuint32_t crc;\n',
    'sec': 'unsigned char *p;\n\tint off, end, pos, len, nul, comma, n, i;\n\tuint32_t noCrc;\n',
}
LOOPHEAD = {
    'bl': '\t\tfor (i = 0; i < nbl; ) {\n',
    'raw': '\t\tfor (i = xb.nRawPatches; i < 16; i++) {\n',
    'flash': '\t\tfor (i = 0; i < 256; i++) {\n',
    'sec': '\t\tfor (i = 0; i < 10; i++) {\n',
}
LOOPEND = {'raw': ('\t\t\tif (pos >= end)\n\t\t\t\ti = 16;\n', 'pos >= end'),
           'flash': ('\t\t\tif (pos >= size)\n\t\t\t\ti = 256;\n', 'pos >= size'),
           'sec': ('\t\t\tif (pos >= end)\n\t\t\t\ti = 10;\n', 'pos >= end')}
NCOUNT = {'bl': 'nbl', 'raw': '16', 'flash': '256', 'sec': '10'}
FREERET = re.compile(r'([ \t]*)free\(buf\);\n[ \t]*return 0;\n')


def loopform(body, sec, form):
    """apply 1 and b inside a section's text"""
    if '1' in form:
        h = LOOPHEAD[sec]
        m = re.match(r'\t\tfor \((i = [^;]+); i < (\w+); ?(i\+\+)?\) \{\n', h)
        new = '\t\tfor (%s; ; %s) {\n\t\t\tif (i >= %s)\n\t\t\t\tbreak;\n' % (m.group(1), m.group(3) or '', m.group(2))
        body = L.sub(body, h, new)
    if 'b' in form and sec in LOOPEND:
        o, c = LOOPEND[sec]
        body = L.sub(body, o, '\t\t\tif (%s)\n\t\t\t\tbreak;\n' % c)
    return body


def nofree(body, code='return 0;'):
    return FREERET.sub(lambda m: m.group(1) + code + '\n', body)


def loopspan(s, sec):
    """(start, end) of the for loop's text in s (brace matched)"""
    h = s.index(LOOPHEAD[sec])
    i = s.index('{', h)
    d = 0
    j = i
    while True:
        if s[j] == '{':
            d += 1
        elif s[j] == '}':
            d -= 1
            if d == 0:
                break
        j += 1
    j = s.index('\n', j) + 1
    return h, j


def gen(tests=(), kf=True, helpers=None, edits=(), raws=()):
    s = MARKED
    helpers = helpers or {}
    # dead tests first, so they travel with their sections
    for k in TESTS:
        s = s.replace('@@%s@@' % k, TESTS[k][1] if k in tests else '')
    if not kf:
        s = L.sub(s, KF, '')
    fns = ''
    for sec in ['bl', 'cbb', 'raw', 'flash', 'sec']:
        a, b = MK[sec]
        i, j = s.index(a), s.index(b)
        body = s[i:j]
        for key in helpers:
            if key == sec or key[:-1] == sec:
                form = helpers[key]
                kind = key[len(sec):]
                if kind == '':
                    fn, call, body = whole(sec, body, form)
                elif kind == 'L':
                    fn, call, body = loop(sec, body, form)
                elif kind == 'B':
                    fn, call, body = entry(sec, body, form)
                fns += fn
                break
        else:
            pass
        s = s[:i] + body + s[j:]
    h = s.index(HEAD)
    s = s[:h] + fns + s[h:]
    for o, n in edits:
        s = L.sub(s, o, n)
    return s


def sig(form, name, params):
    return 'static %s %s(%s)' % ('uint32_t' if 'u' in form else 'int', name, params)


def whole(sec, body, form):
    name = NAMES[sec]
    if sec == 'cbb':
        return 'static void setCbb(void)\n{\n%s}\n\n' % body, '', '\tsetCbb();\n'
    body = loopform(body, sec, form)
    decl = LOCALS[sec]
    params = 'unsigned char *buf, int size'
    args = 'buf, size'
    if sec == 'bl':
        params += ', int nbl'
        args += ', nbl'
    if 't' in form:
        decl += '\tchar tmp[0x400];\n'
    else:
        params += ', char *tmp'
        args += ', tmp'
    if 'f' in form:
        call = '\tif (!%s(%s))\n\t\treturn 0;\n' % (name, args)
    else:
        body = nofree(body)
        call = '\tif (!%s(%s)) {\n\t\tfree(buf);\n\t\treturn 0;\n\t}\n' % (name, args)
    fn = '%s\n{\n\t%s\n%s\treturn 1;\n}\n\n' % (sig(form, name, params), decl, body)
    return fn, call, call


def loop(sec, body, form):
    """only the loop is the helper"""
    name = NAMES[sec] + 'Entries'
    body = loopform(body, sec, form)
    h = body.index('\t\tfor (')
    tmp = body[h:]
    a, b = loopspan_from(tmp)
    lp = tmp[a:b]
    decl = {'bl': 'unsigned char *p;\n\tint len, nul, comma, n, i;\n\tuint32_t noCrc;\n',
            'raw': 'unsigned char *p;\n\tint nul, comma, n, i;\n',
            'flash': 'unsigned char *p;\n\tint len, nul, comma, n, i;\n\tuint32_t noCrc;\n\tchar *s;\n\tuint32_t crc;\n',
            'sec': 'unsigned char *p;\n\tint len, nul, comma, n, i;\n\tuint32_t noCrc;\n'}[sec]
    params = {'bl': 'unsigned char *buf, int size, int pos, int end, int nbl, const char *label',
              'raw': 'unsigned char *buf, int size, int off, int end',
              'flash': 'unsigned char *buf, int size, int off',
              'sec': 'unsigned char *buf, int size, int pos, int end'}[sec]
    args = {'bl': 'buf, size, pos, end, nbl, label', 'raw': 'buf, size, off, end', 'flash': 'buf, size, off', 'sec': 'buf, size, pos, end'}[sec]
    if sec in ('raw', 'flash'):
        decl += '\tint pos = off;\n'
    if 't' in form:
        decl += '\tchar tmp[0x400];\n'
    else:
        params += ', char *tmp'
        args += ', tmp'
    if sec == 'raw':
        # the tail check is part of the helper, it reads pos
        tail = body[h + b:]
        m = re.match(r'\t\tif \(pos < end\) \{\n.*?\n\t\t\}\n', tail, re.S)
        lp += m.group(0)
        b += len(m.group(0))
    if 'f' in form:
        call = '\t\tif (!%s(%s))\n\t\t\treturn 0;\n' % (name, args)
    else:
        lp = nofree(lp)
        call = '\t\tif (!%s(%s)) {\n\t\t\tfree(buf);\n\t\t\treturn 0;\n\t\t}\n' % (name, args)
    fn = '%s\n{\n\t%s\n%s\treturn 1;\n}\n\n' % (sig(form, name, params), decl, lp)
    nb = body[:h] + tmp[:a] + call + tmp[b:]
    if sec in ('raw', 'flash'):
        nb = L.sub(nb, '\t\tpos = off;\n', '')
    if sec in ('sec',):
        pass
    return fn, call, nb


def loopspan_from(s):
    i = s.index('{')
    d = 0
    j = i
    while True:
        if s[j] == '{':
            d += 1
        elif s[j] == '}':
            d -= 1
            if d == 0:
                break
        j += 1
    return 0, s.index('\n', j) + 1


def entry(sec, body, form):
    """one entry per call, returns the new pos or -1; the caller keeps the for and its end test"""
    name = NAMES[sec] + 'Entry'
    h = body.index('\t\tfor (')
    tmp = body[h:]
    a, b = loopspan_from(tmp)
    lp = tmp[a:b]
    head, _, rest = lp.partition('\n')
    inner = rest[:rest.rindex('\t\t}')]
    tail_ = ''
    if sec in LOOPEND:
        o, c = LOOPEND[sec]
        inner = L.sub(inner, o, '')
        tail_ = o
    if sec == 'bl':
        o = '\t\t\ti++;\n'
        inner = L.sub(inner, o, '')
        # the end test stays in the caller
        m = re.search(r'\t\t\tif \(pos > end\) \{\n.*?\n\t\t\t\}\n', inner, re.S)
        tail_ = o + m.group(0)
        inner = inner.replace(m.group(0), '')
    decl = {'bl': 'unsigned char *p;\n\tint len, nul, comma, n;\n\tuint32_t noCrc;\n',
            'raw': 'unsigned char *p;\n\tint nul, comma, n;\n',
            'flash': 'unsigned char *p;\n\tint len, nul, comma, n;\n\tuint32_t noCrc;\n\tchar *s;\n\tuint32_t crc;\n',
            'sec': 'unsigned char *p;\n\tint len, nul, comma, n;\n\tuint32_t noCrc;\n'}[sec]
    params = 'unsigned char *buf, int size, int pos, int i'
    args = 'buf, size, pos, i'
    if sec == 'bl':
        params += ', const char *label'
        args += ', label'
    if 't' in form:
        decl += '\tchar tmp[0x400];\n'
    else:
        params += ', char *tmp'
        args += ', tmp'
    inner = nofree(inner, 'return -1;')
    fn = 'static int %s(%s)\n{\n\t%s\n%s\treturn pos;\n}\n\n' % (name, params, decl, inner)
    call = '\t\t\tpos = %s(%s);\n\t\t\tif (pos < 0) {\n\t\t\t\tfree(buf);\n\t\t\t\treturn 0;\n\t\t\t}\n' % (name, args)
    nb = body[:h] + tmp[:a] + head + '\n' + call + tail_ + '\t\t}\n' + tmp[b:]
    return fn, call, nb


_rn = {}


def norm(d):
    return {k: [re.sub(r' \.-?[0-9a-f]+$', ' .', x) for x in v] for k, v in d.items()}


def nscore(o, sc=None):
    """diff lines with branch targets blanked; 0 only for a whole-object match"""
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
    o = L.compile(s, None, 'a5_%d' % _loc.id)
    if o is None:
        return 10**7, {}, [], n
    sc = L.score(o)
    return nscore(o, sc), sc[2], sc[3], n


def run(V, name, show=20):
    with ThreadPoolExecutor(4) as ex:
        rs = sorted(ex.map(one, V.items()), key=lambda r: r[0])
    with open(os.path.join(A5, name + '.txt'), 'a', newline='\n') as f:
        for r in rs:
            f.write('%s\t%s\t%s\t%s\n' % r)
    for r in rs[:show]:
        print(r)
    print('MATCH', [r[3] for r in rs if r[0] == 0][:40])
    return rs


if __name__ == '__main__':
    import sys
    assert L.same(L.compile(gen(('raw', 'off3', 'off4', 'x')), None, 'a5base')), 'base must match'
    print('base MATCH')
    print(L.score(L.compile(gen(()), None, 'a5none'))[:3])
    print(L.score(L.compile(gen(('raw', 'off3', 'off4', 'x'), kf=False), None, 'a5nokf'))[:3])
    for sp in sys.argv[1:]:
        h = dict(x.split(':') if ':' in x else (x, '') for x in sp.split(','))
        o = L.compile(gen((), True, h), None, 'a5t')
        print(sp, L.score(o)[:3], nscore(o))
