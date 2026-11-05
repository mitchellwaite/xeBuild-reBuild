"""isUpdateBl (attempt 13): return forms read off the Linux build (tmp/xeBuild64 407840: a 23..25 range, then
(15..16) | (9..10)), with no expect.  The question is whether a smaller body gets early inlined into addUpdateBls
(growth 10 is refused now), so the loop's own predictors apply to the first test."""
import itertools, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import bdhints

FOCUS = ['_addUpdateBls', '_isUpdateBl']
OLD = 'return __builtin_expect(type == 23 || type == 15, 0) || type == 16 || type == 9 || type == 10 || type == 24 || type == 25;'

R = {
    '23r': '(type >= 23 && type <= 25)',
    '15r': '(type >= 15 && type <= 16)',
    '9r': '(type >= 9 && type <= 10)',
    '23u': '(uint32_t)(type - 23) <= 2',
    '15u': '(uint32_t)(type - 15) <= 1',
    '9u': '(uint32_t)(type - 9) <= 1',
    '23e': 'type == 23 || type == 24 || type == 25',
    '15e': 'type == 15 || type == 16',
    '9e': 'type == 9 || type == 10',
}


def CASES(base):
    out = []
    for sp in ('r', 'u', 'e'):
        for perm in itertools.permutations(['23', '15', '9']):
            expr = ' || '.join(R[p + sp] for p in perm)
            out.append(('%s %s' % (sp, '-'.join(perm)), base.replace(OLD, 'return ' + expr + ';')))
    sw = ('switch (type) {\n\tcase 9: case 10: case 15: case 16: case 23: case 24: case 25:\n\t\treturn 1;\n\t}\n\treturn 0;')
    out.append(('switch', base.replace(OLD, sw)))
    out.append(('if23', base.replace(OLD, 'if (type == 23)\n\t\treturn 1;\n\treturn type == 15 || type == 16 || type == 9 || type == 10 || type == 24 || type == 25;')))
    return out
