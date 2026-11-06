"""Attempt 7: the xellbutton reader as a real function that also handles the default
(it stores xb.xellButton and logs the default itself), with joins instead of returns.

Generated from parts: how `!s` is handled, how the chain stores (b / field / return), and
where the default test sits; the call site becomes `xellButtonIni(getIniValue(...))` or
`xellButtonIni()` (the helper reads the ini value).

python tools/wip/dehint/op7bx2.py [-top N] [-show KEY]
"""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

SIG = 'static int parseButtonX(const char *s)'
SITE = '''			xb.xellButton = parseButtonX(getIniValue("xellbutton"));
			if (!xb.xellButton) {
				log_printf(1, "default console DVD eject button is being used to start xell\\n");
				xb.xellButton = 0x12;
			}
'''
LOGD = 'log_printf(1, "default console DVD eject button is being used to start xell\\n");'
CH = [('"power", 5', '0x11'), ('"remopower", 9', '0x20'), ('"remox", 5', '0x22'), ('"winbutton", 9', '0x24')]


def chain(ind, lhs):
    t = ''
    for k, (n, v) in enumerate(CH):
        t += ind + ('if' if k == 0 else 'else if') + ' (!strnicmp(s, %s))\n%s\t%s = %s;\n' % (n, ind, lhs, v)
    return t + ind + 'else\n' + ind + '\t%s = parseButtonPart(s);\n' % lhs


def body(nul, lhs, dflt):
    """nul: ifs (if (s) {chain}) | else (if (!s) x = 0; else chain) | init (x = 0 first; if (s))
    lhs: b | f (xb.xellButton);  dflt: fb (test the field) | bb (test b, then store)"""
    x = 'b' if lhs == 'b' else 'xb.xellButton'
    t = '\tint b;\n\n' if lhs == 'b' else ''
    if nul == 'ifs':
        if lhs == 'b':
            t = '\tint b = 0;\n\n'
        else:
            t += '\txb.xellButton = 0;\n'
        t += '\tif (s) {\n' + chain('\t\t', x) + '\t}\n'
    elif nul == 'else':
        t += '\tif (!s)\n\t\t%s = 0;\n\telse ' % x + chain('\t', x).lstrip('\t')
    elif nul == 'init':
        t += '\t%s = 0;\n\tif (s) {\n' % x + chain('\t\t', x) + '\t}\n'
    if lhs == 'b':
        if dflt == 'fb':
            t += '\txb.xellButton = b;\n\tif (!xb.xellButton) {\n\t\t' + LOGD + '\n\t\txb.xellButton = 0x12;\n\t}\n'
        else:
            t += '\txb.xellButton = b;\n\tif (!b) {\n\t\t' + LOGD + '\n\t\txb.xellButton = 0x12;\n\t}\n'
    else:
        t += '\tif (!xb.xellButton) {\n\t\t' + LOGD + '\n\t\txb.xellButton = 0x12;\n\t}\n'
    return t


def make(base, key):
    nul, lhs, dflt, site = key
    if lhs == 'f' and dflt == 'bb':
        return None
    b = body(nul, lhs, dflt)
    if site == 'arg':
        fn = 'static void parseButtonX(const char *s)\n{\n' + b + '}\n'
        call = '\t\t\tparseButtonX(getIniValue("xellbutton"));\n'
    else:
        fn = 'static void parseButtonX(void)\n{\n\tconst char *s = getIniValue("xellbutton");\n' + b + '}\n'
        call = '\t\t\tparseButtonX();\n'
    i = base.find(SIG)
    j = base.find('\n}\n', i) + 3
    t = base[:i] + fn + base[j:]
    assert SITE in t
    return t.replace(SITE, call)


def main():
    a = sys.argv[1:]
    top = 40
    if '-top' in a:
        i = a.index('-top'); top = int(a[i + 1]); del a[i:i + 2]
    base = open(optlib.SRC).read()
    keys = list(itertools.product(['ifs', 'else', 'init'], ['b', 'f'], ['fb', 'bb'], ['arg', 'void']))
    if '-show' in a:
        k = tuple(a[a.index('-show') + 1].split(','))
        out = os.path.join(optlib.BUILD, 'op7bx2_show.c')
        open(out, 'w', newline='\n').write(make(base, k))
        print(out)
        return
    jobs = [(k, make(base, k)) for k in keys]
    jobs = [j for j in jobs if j[1]]
    with ThreadPoolExecutor(max(2, os.cpu_count() or 4)) as p:
        res = list(p.map(lambda j: (j[0], optlib.score_text(j[1])), jobs))
    res.sort(key=lambda x: x[1].get('total', 10 ** 9))
    for f, r in res[:top]:
        print('%-20s %s' % (' '.join(f), optlib.fmt(r)[:140]))


if __name__ == '__main__':
    main()
