"""Attempt 7: natural whole bodies for the xellbutton parser (parseButtonX), no builtins.

Each shape is a real second button reader for the xellbutton site: its own chain (so its own
profile), different exits / result handling, optionally with the xellbutton default and log
moved into it (then the call site changes too).

python tools/wip/dehint/op7bx.py [-top N] [-show KEY]
"""
import os, sys
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


def chain_b(ind, exp_power=False):
    t = ''
    for k, (n, v) in enumerate(CH):
        c = '!strnicmp(s, %s)' % n
        if k == 0 and exp_power:
            c = '__builtin_expect(%s, 1)' % c
        t += ind + ('if' if k == 0 else 'else if') + ' (%s)\n%s\tb = %s;\n' % (c, ind, v)
    t += ind + 'else\n' + ind + '\tb = parseButtonPart(s);\n'
    return t


def chain_ret(ind):
    t = ''
    for n, v in CH:
        t += ind + 'if (!strnicmp(s, %s))\n%s\treturn %s;\n' % (n, ind, v)
    t += ind + 'return parseButtonPart(s);\n'
    return t


def shapes():
    S = {}
    S['cur'] = None
    S['b_if'] = '{\n\tint b = 0;\n\n\tif (s) {\n' + chain_b('\t\t') + '\t}\n\treturn b;\n}\n'
    S['b_if_e'] = '{\n\tint b = 0;\n\n\tif (s) {\n' + chain_b('\t\t', True) + '\t}\n\treturn b;\n}\n'
    S['b_ifnn'] = '{\n\tint b = 0;\n\n\tif (s != NULL) {\n' + chain_b('\t\t') + '\t}\n\treturn b;\n}\n'
    S['b_ret'] = '{\n\tint b;\n\n\tif (!s)\n\t\treturn 0;\n' + chain_b('\t') + '\treturn b;\n}\n'
    S['b_ret_e'] = '{\n\tint b;\n\n\tif (!s)\n\t\treturn 0;\n' + chain_b('\t', True) + '\treturn b;\n}\n'
    S['r_ret'] = '{\n\tif (!s)\n\t\treturn 0;\n' + chain_ret('\t') + '}\n'
    S['r_if'] = '{\n\tif (s) {\n' + chain_ret('\t\t') + '\t}\n\treturn 0;\n}\n'
    S['b_else'] = '{\n\tint b;\n\n\tif (!s)\n\t\tb = 0;\n\telse ' + chain_b('\t').lstrip('\t') + '\treturn b;\n}\n'
    # the default handled here, the site stores the result
    S['d_b'] = ('{\n\tint b = 0;\n\n\tif (s) {\n' + chain_b('\t\t') + '\t}\n\tif (!b) {\n\t\t' + LOGD +
                '\n\t\tb = 0x12;\n\t}\n\treturn b;\n}\n',
                '\t\t\txb.xellButton = parseButtonX(getIniValue("xellbutton"));\n')
    S['d_ret'] = ('{\n\tint b;\n\n\tif (!s)\n\t\tgoto def;\n' + chain_b('\t') + '\tif (b)\n\t\treturn b;\ndef:\n\t' + LOGD +
                  '\n\treturn 0x12;\n}\n',
                  '\t\t\txb.xellButton = parseButtonX(getIniValue("xellbutton"));\n')
    # the helper stores xb.xellButton itself (reads the ini value too)
    S['v_store'] = ('{\n\tint b = 0;\n\n\tif (s) {\n' + chain_b('\t\t') + '\t}\n\txb.xellButton = b;\n\tif (!xb.xellButton) {\n\t\t' + LOGD +
                    '\n\t\txb.xellButton = 0x12;\n\t}\n\treturn 0;\n}\n',
                    '\t\t\tparseButtonX(getIniValue("xellbutton"));\n')
    S['v_store2'] = ('{\n\tint b;\n\n\tif (!s)\n\t\tb = 0;\n\telse ' + chain_b('\t').lstrip('\t') + '\txb.xellButton = b;\n\tif (!b) {\n\t\t' + LOGD +
                     '\n\t\txb.xellButton = 0x12;\n\t}\n\treturn 0;\n}\n',
                     '\t\t\tparseButtonX(getIniValue("xellbutton"));\n')
    return S


def make(base, key):
    s = shapes()[key]
    if s is None:
        return base
    site = None
    if isinstance(s, tuple):
        s, site = s
    i = base.find(SIG)
    j = base.find('\n}\n', i) + 3
    t = base[:i] + SIG + '\n' + s + base[j:]
    if site:
        assert SITE in t
        t = t.replace(SITE, site)
    return t


def main():
    a = sys.argv[1:]
    top = 40
    if '-top' in a:
        i = a.index('-top'); top = int(a[i + 1]); del a[i:i + 2]
    base = open(optlib.SRC).read()
    if '-show' in a:
        k = a[a.index('-show') + 1]
        out = os.path.join(optlib.BUILD, 'op7bx_%s.c' % k)
        open(out, 'w', newline='\n').write(make(base, k))
        print(out)
        return
    jobs = [((k,), make(base, k)) for k in shapes()]
    with ThreadPoolExecutor(max(2, os.cpu_count() or 4)) as p:
        res = list(p.map(lambda j: (j[0], optlib.score_text(j[1])), jobs))
    res.sort(key=lambda x: x[1].get('total', 10 ** 9))
    for f, r in res[:top]:
        print('%-12s %s' % (' '.join(f), optlib.fmt(r)[:150]))


if __name__ == '__main__':
    main()
