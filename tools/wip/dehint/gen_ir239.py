"""Attempt 18: lattice around e.t_addr: E statement x t set in the arms (both, 3000 only, 3800 only, none) x what the bound test reads x attribute subsets.
Does the pin + t-in-arms lose an option of the attribute?"""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_ir235 import *
OPT = ('no-if-conversion', 'no-if-conversion2', 'no-tree-tail-merge')
subsets = [c for n in range(4) for c in itertools.combinations(OPT, n)]
def att(c):
    return '__attribute__((optimize(' + ', '.join('"%s"' % x for x in c) + '))) ' if c else ''
ELS = {'pin': PIN, 'pint': PIN + ' t = addr;', 'ta': 't = addr;', 'tpin': 't = addr; ' + PIN, 'none': ';'}
ARMS = {'both': (' t = addr;', ' t = addr;'), 'a30': ('', ' t = addr;'), 'a38': (' t = addr;', ''), 'no': ('', '')}
CMP = {'t': 't', 'u': '(unsigned)addr'}
forms = {}
for (ek, e), (ak, (a38, a30)), (ck, c), sub in itertools.product(ELS.items(), ARMS.items(), CMP.items(), subsets):
    f = body(att(sub), e, cmpa=c)
    f = f.replace('using 0x3800\\n", size);\n', 'using 0x3800\\n", size);' + a38 + '\n').replace('using 0x3000\\n", size);\n', 'using 0x3000\\n", size);' + a30 + '\n')
    forms['.'.join((ek, ak, ck, ''.join(x[3] + x[-1] for x in sub) or 'a0'))] = (f, len(sub))
if __name__ == '__main__':
    res = []
    for k, (f, n) in forms.items():
        s = score(text(f))
        if s[0] == 'E':
            continue
        res.append((s[1], s[0], k, n))
    print(len(res))
    for r in sorted(res, key=lambda x: (x[0], x[1]))[:30]:
        print(r)
    print('no pin:')
    for r in sorted([r for r in res if 'pin' not in r[2]], key=lambda x: (x[0], x[1]))[:10]:
        print(r)
    print('pin, fewest options:')
    for n in (0, 1, 2):
        for r in sorted([r for r in res if 'pin' in r[2] and r[3] == n], key=lambda x: (x[0], x[1]))[:4]:
            print(r)
