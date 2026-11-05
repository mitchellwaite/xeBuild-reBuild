"""Attempt 19: an E statement with a second operand that isn't constant at PRE and that dom3/vrp2 folds: PRE translates it through addr's PHI but
no predecessor has a leader (by_some false), so it stays in E.  (size & ~0x800) - 0x3000 is 0 on E's path, known only from the range test reassoc1 makes.
Measurement first: nobody would write these as they stand."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_ir235 import body, text, score, PIN, ATTR
from ir17lib import diff, put

OPT = ('no-if-conversion', 'no-if-conversion2', 'no-tree-tail-merge')
subsets = [c for n in range(4) for c in itertools.combinations(OPT, n)]
def att(c):
    return '__attribute__((optimize(' + ', '.join('"%s"' % x for x in c) + '))) ' if c else ''

Y = '((size & ~0x800) - 0x3000)'
Yu = '(((unsigned)size & ~0x800u) - 0x3000u)'
ELS = {
    'y_add': f'addr = addr + {Y};',
    'y_addu': f'addr = (int)((unsigned)addr + {Yu});',
    'y_t': f't = (unsigned)addr + {Yu};',
    'y_or': f't = (unsigned)addr | {Yu};',
    'y_t_addr': f't = (unsigned)addr + {Yu}; addr = t;',
    'y_x': f'addr ^= {Y};',
}
CMP = {'u': '(unsigned)addr', 't': 't'}
ARM = {'no': ('', ''), 'both': (' t = addr;', ' t = addr;')}
forms = {}
for (ek, e), (ck, c), (ak, (a38, a30)), sub in itertools.product(ELS.items(), CMP.items(), ARM.items(), subsets):
    if ck == 't' and ak == 'no':
        continue
    f = body(att(sub), e, cmpa=c)
    f = f.replace('using 0x3800\\n", size);\n', 'using 0x3800\\n", size);' + a38 + '\n').replace('using 0x3000\\n", size);\n', 'using 0x3000\\n", size);' + a30 + '\n')
    forms['.'.join((ek, ck, ak, ''.join(x[3] + x[-1] for x in sub) or 'a0'))] = f

if __name__ == '__main__':
    res = []
    for k, f in forms.items():
        s = score(text(f))
        if s[0] == 'E':
            print(k, s[1][:200])
            continue
        res.append((s[1], s[0], k, s[2]))
    res.sort(key=lambda x: (x[0], x[1]))
    print(len(res))
    for r in res[:30]:
        print(r)
