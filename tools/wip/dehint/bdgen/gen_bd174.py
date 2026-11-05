"""isUpdateBl with no expect: every order of the six other types after type == 23 (gen_bd173 found `23, 10, 9, ..` gets the rotation right but leaves 10 out of the bit test)."""
import itertools

OLD = 'return __builtin_expect(type == 23 || type == 15, 0) || type == 16 || type == 9 || type == 10 || type == 24 || type == 25;'


def CASES(base):
    out = []
    for p in itertools.permutations((9, 10, 15, 16, 24, 25)):
        s = ' || '.join('type == %d' % x for x in (23,) + p)
        out.append((' '.join(map(str, p)), base.replace(OLD, 'return ' + s + ';')))
    return out


FOCUS = ['_addUpdateBls', '_isUpdateBl']
