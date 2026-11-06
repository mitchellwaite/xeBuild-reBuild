"""Attempt 5: parseButtonX's z feed as control flow.  The 3-cp branching feed is
replaced by 1- or 2-cp feeds at one of four positions in the else arm (F0..F3) whose
dead arms run gotos to labels anywhere in the copy, or returns; the power expect on/off.
python tools/wip/dehint/op5bx.py [-r removals] [-top N] [-maxcp N]"""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib, optricks

SIG = 'static int parseButtonX(const char *s)'
CP = '__builtin_constant_p(xb.xellButton + %d)'
TG = ['goto z;', 'goto Lp;', 'goto Lr;', 'goto Lx;', 'goto Lw;', 'goto Lpt;', 'goto Lret;',
      'return 0;', 'return b;']


def feeds(maxcp):
    out = [('-', '')]
    for x in TG:
        out.append(('1[%s]' % x, 'if (%s) %s' % (CP % 1, x)))
    if maxcp >= 2:
        for x, y in itertools.product(TG, TG):
            out.append(('n[%s|%s]' % (x, y), 'if (%s) { if (%s) %s %s }' % (CP % 1, CP % 2, x, y)))
            out.append(('s[%s|%s]' % (x, y), 'if (%s) %s if (%s) %s' % (CP % 1, x, CP % 2, y)))
    if maxcp >= 3:
        out.append(('cur', 'if (%s) { if (%s) goto z; if (%s) goto z; }' % (CP % 1, CP % 2, CP % 3)))
    return out


def body(pos, feed, exp):
    used = {l for l in ('z', 'Lp', 'Lr', 'Lx', 'Lw', 'Lpt', 'Lret') if ('goto %s;' % l) in feed}
    F = ['', '', '', '']
    F[pos] = feed
    L = lambda l: (l + ':\n') if l in used else ''
    t = '{\n\tint b = 0;\n\n\tif (!s) {\nz:\n\t\treturn 0;\n\t}\n'
    t += ('\tif (__builtin_expect(!strnicmp(s, "power", 5), 1)) {\n' if exp else
          '\tif (!strnicmp(s, "power", 5)) {\n')
    t += L('Lp') + '\t\tb = 0x11;\n\t} else {\n'
    t += '\t\t' + F[0] + '\n' + L('Lr') + '\t\tif (!strnicmp(s, "remopower", 9))\n\t\t\tb = 0x20;\n\t\telse {\n'
    t += '\t\t' + F[1] + '\n' + L('Lx') + '\t\tif (!strnicmp(s, "remox", 5))\n\t\t\tb = 0x22;\n\t\telse {\n'
    t += '\t\t' + F[2] + '\n' + L('Lw') + '\t\tif (!strnicmp(s, "winbutton", 9))\n\t\t\tb = 0x24;\n\t\telse {\n'
    t += '\t\t' + F[3] + '\n' + L('Lpt') + '\t\t\tb = parseButtonPart(s);\n\t\t}}}\n\t}\n'
    t += L('Lret') + '\treturn b;\n}\n'
    return t


def replace_fn(text, newbody):
    i = text.find(SIG)
    j = text.find('\n}\n', i) + 3
    return text[:i] + SIG + '\n' + newbody + text[j:]


def ncp(name):
    if name == '-':
        return 0
    if name == 'cur':
        return 3
    return 1 if name.startswith('1') else 2


def main():
    a = sys.argv[1:]
    rem = []
    if '-r' in a:
        i = a.index('-r')
        rem = [x for x in a[i + 1].split(',') if x]
        del a[i:i + 2]
    top = 30
    if '-top' in a:
        i = a.index('-top')
        top = int(a[i + 1])
        del a[i:i + 2]
    maxcp = 2
    if '-maxcp' in a:
        i = a.index('-maxcp')
        maxcp = int(a[i + 1])
        del a[i:i + 2]
    base, got = optricks.apply(optricks.base(), rem)
    jobs = []
    for exp in (True, False):
        for pos in range(4):
            for n, f in feeds(maxcp):
                if pos and n in ('-', 'cur'):
                    continue
                jobs.append(((exp, pos, n), ncp(n) + exp, replace_fn(base, body(pos, f, exp))))
    print('removals', got, len(jobs), 'jobs', flush=True)
    with ThreadPoolExecutor(4) as p:
        res = list(p.map(lambda j: (j[0], j[1], optlib.score_text(j[2], optricks.flags_for(rem))), jobs))
    res.sort(key=lambda x: (x[2].get('total', 10 ** 9), x[1]))
    for k, n, r in res[:top]:
        print('%-50s n=%d %s' % (repr(k), n, optlib.fmt(r)))
    print('IDENTICAL:', [(k, n) for k, n, r in res if r.get('identical')])


if __name__ == '__main__':
    main()
