"""exp_upd (attempt 8): addUpdateBls with the update-type test written in its own loop (a macro or a copy of the
test), isUpdateBl plain.  Then the loop's test is predicted in addUpdateBls with the loop's predictors, not in
isUpdateBl's own profile.  23 first, every order of the other six; BDF=and for the `!=` && form."""
import itertools, os

OLD = 'return __builtin_expect(type == 23 || type == 15, 0) || type == 16 || type == 9 || type == 10 || type == 24 || type == 25;'
NEW = 'return type == 23 || type == 15 || type == 16 || type == 9 || type == 10 || type == 24 || type == 25;'
LOOP = '		if (!isUpdateBl(type))\n			continue;\n'
FIRST = [int(x) for x in os.environ.get('BDFIRST', '23').split(',')]


def CASES(base):
    t0 = base.replace(OLD, NEW)
    if LOOP not in t0 or t0 == base:
        raise ValueError('text')
    out = []
    rest = [x for x in (9, 10, 15, 16, 23, 24, 25) if x not in FIRST]
    for p in itertools.permutations(rest):
        o = FIRST + list(p)
        if os.environ.get('BDF') == 'and':
            s = '		if (' + ' && '.join('type != %d' % x for x in o) + ')\n			continue;\n'
        else:
            s = '		if (!(' + ' || '.join('type == %d' % x for x in o) + '))\n			continue;\n'
        out.append((' '.join(map(str, o)), t0.replace(LOOP, s)))
    return out


FOCUS = ['_addUpdateBls', '_isUpdateBl']
