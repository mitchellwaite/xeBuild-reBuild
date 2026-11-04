"""fl3d.py show <tag> <fn> <pass-suffix>: fn's body from one pass of a flpass dump (pa, pb), no decls.
fl3d.py cmp <fn> <passes..>: diff pa vs pb for those.
fl3d.py first <fn> [regex]: for every tree pass, how many lines differ pa vs pb once bb numbers are
stripped, and the count of lines matching regex in pa and pb (to see when a test dies)."""
import difflib, glob, os, re, sys
import fllib as L


def body(tag, fn, ps):
    fs = glob.glob(os.path.join(L.BD, 'dump', tag, '-.*' + ps))
    if not fs:
        return ''
    t = open(fs[0], errors='replace').read()
    for q in re.split(r'(?m)^(?=;; Function )', t):
        if q.startswith(';; Function %s ' % fn):
            m = q.rfind('\n%s (' % fn)
            q = q[m:]
            return '\n'.join(l for l in q.splitlines() if not re.match(r'^  [\w. *]+ [\w.]+;$', l))
    return ''


def nobb(s):
    s = re.sub(r'\bbb \d+', 'bb', s)
    s = re.sub(r'\((\d+)\)', '()', s)
    return s


if sys.argv[1] == 'cmp':
    fn = sys.argv[2]
    for p in sys.argv[3:]:
        print('=====', p)
        print('\n'.join(difflib.unified_diff(body('pa', fn, p).splitlines(), body('pb', fn, p).splitlines(), lineterm='', n=int(os.environ.get('N', '0')))))
elif sys.argv[1] == 'first':
    fn = sys.argv[2]
    rx = re.compile(sys.argv[3]) if len(sys.argv) > 3 else None
    names = sorted({re.search(r'-\.(\d+t\.[\w.+-]+)$', f).group(1) for f in glob.glob(os.path.join(L.BD, 'dump', 'pa', '-.*t.*'))}, key=lambda x: int(re.match(r'\d+', x).group()))
    for p in names:
        a, b = body('pa', fn, p), body('pb', fn, p)
        if not a:
            continue
        al, bl = nobb(a).splitlines(), nobb(b).splitlines()
        d = sum(1 for x in difflib.ndiff(al, bl) if x[0] in '+-') if abs(len(al) - len(bl)) < 200 else -1
        extra = ''
        if rx:
            extra = ' %d %d' % (len(rx.findall(a)), len(rx.findall(b)))
        print(p, d, extra)
else:
    print(body(sys.argv[2], sys.argv[3], sys.argv[4]))
