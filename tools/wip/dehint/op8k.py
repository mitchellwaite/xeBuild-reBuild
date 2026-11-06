"""Attempt 8: the dead feeds with their __builtin_constant_p / __builtin_expect values shared
(one SSA value tested several times: each test gets the same prediction, all fold at once).

python tools/wip/dehint/op8k.py [-show KEY -o out.c]"""
import os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

REV = ('''			if (__builtin_constant_p(xb.blSuffix[1] + 1)) { if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 2), 0)) goto dz1; return; }
			if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 15), 0)) { if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 16), 0)) goto dz2; }
''')
ZF = '''		if (__builtin_constant_p(xb.xellButton + 1)) { if (__builtin_constant_p(xb.xellButton + 2) > 0) goto z; }
'''

C = '__builtin_constant_p(xb.blSuffix[1])'
REVS = {
    # one cp, three expects of it
    'k1': '\t\t\tint k = %s;\n\n\t\t\tif (k) { if (__builtin_expect(k, 0)) goto dz1; return; }\n'
          '\t\t\tif (__builtin_expect(k, 0)) { if (__builtin_expect(k, 0)) goto dz2; }\n' % C,
    # one cp, one expect
    'k2': '\t\t\tint k = %s;\n\t\t\tlong e = __builtin_expect(k, 0);\n\n\t\t\tif (k) { if (e) goto dz1; return; }\n'
          '\t\t\tif (e) { if (e) goto dz2; }\n' % C,
    # two cp (different args), one expect each group
    'k3': '\t\t\tint k = %s, m = __builtin_constant_p(xb.blSuffix[1] + 1);\n\t\t\tlong e = __builtin_expect(m, 0);\n\n'
          '\t\t\tif (k) { if (e) goto dz1; return; }\n\t\t\tif (e) { if (e) goto dz2; }\n' % C,
    # expect of the cp directly, used for all tests; first test plain cp
    'k4': '\t\t\tlong e = __builtin_expect(%s, 0);\n\n\t\t\tif (%s) { if (e) goto dz1; return; }\n'
          '\t\t\tif (e) { if (e) goto dz2; }\n' % (C, '__builtin_constant_p(xb.blSuffix[1] + 1)'),
    # expect computed inline each time from one cp
    'k5': '\t\t\tint k = %s;\n\n\t\t\tif (k) { if (__builtin_expect(k, 0)) goto dz1; return; }\n'
          '\t\t\tif (__builtin_expect(k, 0)) { if (__builtin_expect(k + 1, 1)) goto dz2; }\n' % C,
}
_K = '\t\t\tint k = %s;\n' % C
_E = '\t\t\tlong e = __builtin_expect(k, 0);\n'
for nm, inner in [('ka', '__builtin_expect(k == 1, 0)'), ('kb', '__builtin_expect(k > 0, 0)'),
                  ('kc', '__builtin_expect(k & 1, 0)'), ('kd', '__builtin_expect(__builtin_constant_p(xb.blSuffix[2]), 0)')]:
    REVS[nm] = (_K + '\n\t\t\tif (k) { if (__builtin_expect(k, 0)) goto dz1; return; }\n'
                '\t\t\tif (__builtin_expect(k, 0)) { if (%s) goto dz2; }\n' % inner)
for nm, inner in [('e1', 'e == 1'), ('e2', 'e > 0'), ('e3', 'e & 1'), ('e4', 'e != 0 && k == 1'),
                  ('e5', '__builtin_expect(k == 1, 0)'), ('e6', 'e >= 1'), ('e7', 'e == k')]:
    REVS[nm] = (_K + _E + '\n\t\t\tif (k) { if (e) goto dz1; return; }\n'
                '\t\t\tif (e) { if (%s) goto dz2; }\n' % inner)
ZFS = {
    'z1': '\t\tint k = __builtin_constant_p(xb.xellButton);\n\n\t\tif (k) { if (k > 0) goto z; }\n',
}


MS = '__builtin_memset(s, 0, __builtin_constant_p(xb.macid[1] + 9));'
TOP = 'void applyIniOptions(void)\n{\n\tchar *s;\n\tint i;\n'


def make(base, key):
    t = base
    if key.startswith('m:'):
        # one cp for the whole function: memset size and the rev feeds
        key = key[2:]
        t = t.replace(REV, REVS[key].replace(_K, ''))
        assert MS in t and TOP in t
        t = t.replace(MS, '__builtin_memset(s, 0, k);')
        t = t.replace(TOP, TOP + '\tint k = %s;\n' % C)
        return t
    for part in key.split('+'):
        if part in REVS:
            assert REV in t
            t = t.replace(REV, REVS[part])
        elif part in ZFS:
            assert ZF in t
            t = t.replace(ZF, ZFS[part])
    return t


def main():
    a = sys.argv[1:]
    base = optlib.read_src(optlib.SRC)
    if '-show' in a:
        k = a[a.index('-show') + 1]
        t = make(base, k)
        if '-o' in a:
            open(a[a.index('-o') + 1], 'w', newline='\n').write(t)
        print(optlib.fmt(optlib.score_text(t)))
        return
    ks = list(REVS) + list(ZFS) + ["m:e1", "m:e3", "m:e5", "m:ka", "e1+z1"]
    with ThreadPoolExecutor(8) as p:
        res = list(p.map(lambda k: (k, optlib.score_text(make(base, k))), ks))
    for f, r in res:
        print('%-8s %s' % (f, optlib.fmt(r)[:200]))


if __name__ == '__main__':
    main()
