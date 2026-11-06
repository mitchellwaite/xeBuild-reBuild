"""Attempt 17, exp_upd: isUpdateBl forms that einline can take.  einline refuses the `||` chain because fnsplit
has already split it (isUpdateBl.part.N holds the tail tests), so isUpdateBl's header has one call edge and
growth 10 * (1 + 1) > early-inlining-insns 14.  A body with no branch can't be split: the tests joined by `|`
(one block) or other branch-free forms.  Axes: operator form, test order.  Runs on src as of d09240ad."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun

OLD = '''	return __builtin_expect(type == 23 || type == 15, 0) || type == 16 || type == 9 || type == 10 || type == 24 || type == 25;
'''
ORDERS = {
    'src': [23, 15, 16, 9, 10, 24, 25],
    'asc': [9, 10, 15, 16, 23, 24, 25],
    'desc': [25, 24, 23, 16, 15, 10, 9],
    '15f': [15, 23, 16, 9, 10, 24, 25],
    'b23l': [9, 10, 15, 16, 24, 25, 23],
}


def body(form, ts):
    if form == 'or':
        return '\treturn ' + ' || '.join('type == %d' % t for t in ts) + ';\n'
    if form == 'bor':
        return '\treturn ' + ' | '.join('(type == %d)' % t for t in ts) + ';\n'
    if form == 'borbare':
        return '\treturn ' + ' | '.join('type == %d' % t for t in ts) + ';\n'
    if form == 'ifs':
        return ''.join('\tif (type == %d)\n\t\treturn 1;\n' % t for t in ts) + '\treturn 0;\n'
    if form == 'sw':
        return '\tswitch (type) {\n' + ''.join('\tcase %d:\n' % t for t in ts) + '\t\treturn 1;\n\t}\n\treturn 0;\n'
    if form == 'swr':
        return '\tint r = 0;\n\n\tswitch (type) {\n' + ''.join('\tcase %d:\n' % t for t in ts) + '\t\tr = 1;\n\t}\n\treturn r;\n'
    if form == 'flag':
        return '\tint r = 0;\n\n' + ''.join('\tif (type == %d)\n\t\tr = 1;\n' % t for t in ts) + '\treturn r;\n'
    if form == 'oreq':
        return '\tint r = 0;\n\n' + ''.join('\tr |= type == %d;\n' % t for t in ts) + '\treturn r;\n'
    raise ValueError(form)


FORMS = ['or', 'bor', 'borbare', 'ifs', 'sw', 'swr', 'flag', 'oreq']


def CASES(base):
    out = []
    for f, o in itertools.product(FORMS, ORDERS):
        new = body(f, ORDERS[o])
        out.append(('%s %s' % (f, o), lambda b, new=new: bdrun.sub(b, OLD, new, 1)))
    return out


FOCUS = ['_addUpdateBls', '_isUpdateBl']
