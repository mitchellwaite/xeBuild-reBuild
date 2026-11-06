"""Attempt 8: parseButtonX with a result test that is live at profile_estimate and threaded
away after inlining (the attempt-7 lever), in place of the z feed (and the power expect).

python tools/wip/dehint/op8bx.py [-top N] [-show KEY]
Keys are <head>_<chain>_<tail>_<exp>:
  head: r  `if (!s) return 0;`      i  `if (s) { ... }` around everything (b = 0 init)
        z  `if (!s) b = 0; else {...}`
  chain where the test goes: a  after the whole chain (power included)
        e  only inside the non-power arm, after its chain
        p  only after the part call
  tail: n `if (!b) return 0; return b;`   y `if (b) return b; return 0;`
        g `if (!b) goto z;` with z: the !s return (r head only)
  exp:  E power expect kept, N none."""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

SIG = 'static int parseButtonX(const char *s)'
CH = [('"remopower", 9', '0x20'), ('"remox", 5', '0x22'), ('"winbutton", 9', '0x24')]


def body(head, where, tail, exp):
    I = '\t'
    pw = '!strnicmp(s, "power", 5)'
    if exp == 'E':
        pw = '__builtin_expect(%s, 1)' % pw

    def test(ind):
        if tail == 'n':
            return ind + 'if (!b)\n' + ind + '\treturn 0;\n'
        if tail == 'y':
            return ind + 'if (b)\n' + ind + '\treturn b;\n' + ind + 'return 0;\n'
        return ind + 'if (!b)\n' + ind + '\tgoto z;\n'

    def chain(ind):
        t = ''
        for k, (n, v) in enumerate(CH):
            t += ind + ('if' if k == 0 else 'else if') + ' (!strnicmp(s, %s))\n%s\tb = %s;\n' % (n, ind, v)
        t += ind + 'else {\n' if where == 'p' else ind + 'else\n'
        t += ind + '\tb = parseButtonPart(s);\n'
        if where == 'p':
            t += test(ind + '\t') + ind + '}\n'
        return t

    def core(ind):
        t = ind + 'if (%s)\n%s\tb = 0x11;\n' % (pw, ind)
        t += ind + 'else {\n' + chain(ind + '\t')
        if where == 'e':
            t += test(ind + '\t')
        t += ind + '}\n'
        if where == 'a':
            t += test(ind)
        return t

    out = '{\n\tint b = 0;\n\n'
    if head == 'r':
        out += '\tif (!s) {\nz:\n\t\treturn 0;\n\t}\n' if tail == 'g' else '\tif (!s)\n\t\treturn 0;\n'
        out += core('\t')
    elif head == 'i':
        out += '\tif (s) {\n' + core('\t\t') + '\t}\n'
    else:
        out += '\tif (!s)\n\t\tb = 0;\n\telse {\n' + core('\t\t') + '\t}\n'
    if not (tail == 'y' and where == 'a' and head == 'r'):
        out += '\treturn b;\n'
    out += '}\n'
    return out


def keys():
    for h, w, t, e in itertools.product('riz', 'aep', 'nyg', 'EN'):
        if t == 'g' and h != 'r':
            continue
        yield '%s_%s_%s_%s' % (h, w, t, e)


def make(base, key):
    h, w, t, e = key.split('_')
    i = base.find(SIG)
    j = base.find('\n}\n', i) + 3
    return base[:i] + SIG + '\n' + body(h, w, t, e) + base[j:]


def main():
    a = sys.argv[1:]
    top = 40
    if '-top' in a:
        i = a.index('-top'); top = int(a[i + 1]); del a[i:i + 2]
    base = open(optlib.SRC).read()
    if '-show' in a:
        k = a[a.index('-show') + 1]
        out = os.path.join(optlib.BUILD, 'a8', 'op8bx_%s.c' % k)
        open(out, 'w', newline='\n').write(make(base, k))
        print(out)
        return
    ks = list(keys())
    with ThreadPoolExecutor(8) as p:
        res = list(p.map(lambda k: (k, optlib.score_text(make(base, k))), ks))
    res.sort(key=lambda x: x[1].get('total', 10 ** 9) if not x[1].get('identical') else -1)
    for f, r in res[:top]:
        print('%-10s %s' % (f, optlib.fmt(r)[:150]))


if __name__ == '__main__':
    main()
