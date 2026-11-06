"""Attempt 7: parseButtonX with defensive `s &&` tests on its else-if chain.

After the first null test, VRP/DOM thread the null path past every later `s` test, so the
code is the same; at profile_estimate each redundant `s` test leaks part of the else arm to
the `b = 0` exit, which is what the dead z feed did.  Axes: which of the five arms
(power, remopower, remox, winbutton, part) carry `s &&` / `if (s)`, an `if (!s) return 0;`
head or not, the power expect on/off, the result as `b` or returns.

python tools/wip/dehint/op7bx3.py [-top N] [-show KEY]
"""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

SIG = 'static int parseButtonX(const char *s)'
CH = [('"power", 5', '0x11'), ('"remopower", 9', '0x20'), ('"remox", 5', '0x22'), ('"winbutton", 9', '0x24')]


def body(g, head, exp, form):
    """g: 5 bools (guard on each arm); head: 0/1; form: b | r"""
    t = '{\n'
    if form == 'b':
        t += '\tint b = 0;\n\n'
    if head:
        t += '\tif (!s)\n\t\treturn 0;\n'
    for k, (n, v) in enumerate(CH):
        c = '!strnicmp(s, %s)' % n
        if k == 0 and exp:
            c = '__builtin_expect(%s, 1)' % c
        if g[k]:
            c = 's && ' + c
        if form == 'b':
            t += '\t' + ('if' if k == 0 else 'else if') + ' (%s)\n\t\tb = %s;\n' % (c, v)
        else:
            t += '\tif (%s)\n\t\treturn %s;\n' % (c, v)
    if form == 'b':
        t += '\telse if (s)\n\t\tb = parseButtonPart(s);\n' if g[4] else '\telse\n\t\tb = parseButtonPart(s);\n'
        t += '\treturn b;\n}\n'
    else:
        t += '\tif (s)\n\t\treturn parseButtonPart(s);\n\treturn 0;\n}\n' if g[4] else '\treturn parseButtonPart(s);\n}\n'
    return t


def make(base, key):
    g, head, exp, form = key
    if not head and not g[0]:
        return None   # s would be used unchecked
    i = base.find(SIG)
    j = base.find('\n}\n', i) + 3
    return base[:i] + SIG + '\n' + body(g, head, exp, form) + base[j:]


def name(k):
    g, head, exp, form = k
    return '%s h%d %s %s' % (''.join('1' if x else '0' for x in g), head, 'e' if exp else '-', form)


def main():
    a = sys.argv[1:]
    top = 40
    if '-top' in a:
        i = a.index('-top'); top = int(a[i + 1]); del a[i:i + 2]
    base = open(optlib.SRC).read()
    keys = list(itertools.product(itertools.product([0, 1], repeat=5), [0, 1], [0, 1], ['b', 'r']))
    if '-show' in a:
        s = a[a.index('-show') + 1].split(',')
        k = (tuple(int(c) for c in s[0]), int(s[1]), int(s[2]), s[3])
        out = os.path.join(optlib.BUILD, 'op7bx3_show.c')
        open(out, 'w', newline='\n').write(make(base, k))
        print(out)
        return
    jobs = [(k, make(base, k)) for k in keys]
    jobs = [j for j in jobs if j[1]]
    print('jobs', len(jobs), flush=True)
    with ThreadPoolExecutor(max(2, os.cpu_count() or 4)) as p:
        res = list(p.map(lambda j: (j[0], optlib.score_text(j[1])), jobs))
    res.sort(key=lambda x: x[1].get('total', 10 ** 9))
    for f, r in res[:top]:
        print('%-20s %s' % (name(f), optlib.fmt(r)[:140]))


if __name__ == '__main__':
    main()
