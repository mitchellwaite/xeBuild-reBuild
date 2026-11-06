"""Attempt 3: parseButton's own shape, with no hints, on top of optricks part+m_bx
(parseButtonX and the hand-written part gone, gcc splits parseButton itself).
The idea: a different parseButton profile could give both the split (call likely,
winbutton expect gone) and the xellbutton site's frequencies (remopower 18, !s 37).

python tools/wip/dehint/opbtn.py [-o DIR] [names..]"""
import os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib, optricks

NAMES = [('power', 5, '0x11'), ('remopower', 9, '0x20'), ('remox', 5, '0x22'),
         ('winbutton', 9, '0x24'), ('wirelessx', 9, '0x55')]
WIRED = [('wiredxb1', '0x59'), ('wiredxb2', '0x58'), ('wiredxb3', '0x5a'),
         ('wiredxf1', '0x56'), ('wiredxf2', '0x57')]
TAIL = [('eject', 5, '0x12'), ('kiosk', 5, '0x41')]


def chain_assign(ind, expect_win=False):
    """the current else-if chain assigning b"""
    t = ind + 'if (!strnicmp(s, "power", 5))\n' + ind + '\tb = 0x11;\n'
    for n, l, v in NAMES[1:] + [('wiredx', 6, None)] + TAIL:
        cond = '!strnicmp(s, "%s", %d)' % (n, l)
        if n == 'winbutton' and expect_win:
            cond = '__builtin_expect(%s, 1)' % cond
        if v is None:
            t += ind + 'else if (%s) {\n' % cond
            t += wired_assign(ind + '\t')
            t += ind + '}'
            t += ' '
            continue
        if t.endswith('} '):
            t = t[:-1] + ' else if (%s)\n' % cond + ind + '\tb = %s;\n' % v
        else:
            t += ind + 'else if (%s)\n' % cond + ind + '\tb = %s;\n' % v
    return t


def wired_assign(ind):
    t = ''
    for i, (n, v) in enumerate(WIRED):
        t += ind + ('if' if i == 0 else 'else if') + ' (!strnicmp(s, "%s", 8))\n' % n + ind + '\tb = %s;\n' % v
    t += ind + 'else\n' + ind + '\tb = 0x5a;\n'
    return t


def wired_ret(ind):
    t = ''
    for n, v in WIRED:
        t += ind + 'if (!strnicmp(s, "%s", 8))\n' % n + ind + '\treturn %s;\n' % v
    t += ind + 'return 0x5a;\n'
    return t


def chain_ret(ind):
    t = ''
    for n, l, v in NAMES:
        t += ind + 'if (!strnicmp(s, "%s", %d))\n' % (n, l) + ind + '\treturn %s;\n' % v
    t += ind + 'if (!strnicmp(s, "wiredx", 6)) {\n' + wired_ret(ind + '\t') + ind + '}\n'
    for n, l, v in TAIL:
        t += ind + 'if (!strnicmp(s, "%s", %d))\n' % (n, l) + ind + '\treturn %s;\n' % v
    return t


def fn(body):
    return 'int parseButton(const char *s)\n{\n' + body + '}\n'


V = {}
V['cur'] = fn('\tint b = 0;\n\n\tif (!s)\n\t\treturn 0;\n' + chain_assign('\t', True) + '\treturn b;\n')
V['noexp'] = fn('\tint b = 0;\n\n\tif (!s)\n\t\treturn 0;\n' + chain_assign('\t') + '\treturn b;\n')
V['ifs'] = fn('\tint b = 0;\n\n\tif (s) {\n' + chain_assign('\t\t') + '\t}\n\treturn b;\n')
V['ifs_exp'] = fn('\tint b = 0;\n\n\tif (s) {\n' + chain_assign('\t\t', True) + '\t}\n\treturn b;\n')
V['ret'] = fn('\tif (!s)\n\t\treturn 0;\n' + chain_ret('\t') + '\treturn 0;\n')
V['ret_ifs'] = fn('\tif (s) {\n' + chain_ret('\t\t') + '\t}\n\treturn 0;\n')
V['retb'] = fn('\tint b = 0;\n\n\tif (!s)\n\t\treturn b;\n' + chain_assign('\t') + '\treturn b;\n')
# assign chain whose wiredx arm returns
V['mix'] = fn('\tif (!s)\n\t\treturn 0;\n' + chain_ret('\t').replace(
    '\t\treturn 0x5a;\n\t}\n', '\t\treturn 0x5a;\n\t}\n') + '\treturn 0;\n')
# unsigned / char locals
V['u32'] = V['noexp'].replace('\tint b = 0;', '\tuint32_t b = 0;')
V['u8'] = V['noexp'].replace('\tint b = 0;', '\tuint8_t b = 0;')
V['u32_exp'] = V['cur'].replace('\tint b = 0;', '\tuint32_t b = 0;')
V['u8_exp'] = V['cur'].replace('\tint b = 0;', '\tuint8_t b = 0;')
# b assigned in an else at the end
V['else0'] = fn('\tint b;\n\n\tif (!s)\n\t\treturn 0;\n' + chain_assign('\t') + '\telse\n\t\tb = 0;\n\treturn b;\n')
V['ifs_else0'] = fn('\tint b;\n\n\tif (s) {\n' + chain_assign('\t\t') + '\t\telse\n\t\t\tb = 0;\n\t} else\n\t\tb = 0;\n\treturn b;\n')


def build(body):
    t, got = optricks.apply(optricks.base(), ['part', 'm_bx'])
    assert got == ['part', 'm_bx'], got
    i = t.index('int parseButton(const char *s)\n{')
    j = t.index('\n}\n', i) + 3
    return t[:i] + body + t[j:]


def run(n):
    return n, optlib.fmt(optlib.score_text(build(V[n])))


if __name__ == '__main__':
    a = sys.argv[1:]
    out = None
    if a[:1] == ['-o']:
        out = a[1]
        a = a[2:]
        os.makedirs(out, exist_ok=True)
    names = a or list(V)
    if out:
        for n in names:
            open(os.path.join(out, n + '.c'), 'w', newline='\n').write(build(V[n]))
    with ThreadPoolExecutor(6) as ex:
        for n, r in ex.map(run, names):
            print(n, r)
