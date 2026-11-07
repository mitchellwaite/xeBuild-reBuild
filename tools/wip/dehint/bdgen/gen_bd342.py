"""Attempt 23, exp_upd: gen_bd341 found `if (type == 23) return 1; if (type == 15) return 1; return 16 || 9 || ..;`
IDENTICAL with no expect.  This sweeps the spellings around it to find the most natural one that still matches:
the two lone tests' order, else-if, the `||` group's order, and the group written as its own if.  Runs on src as of
604028f1."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun

OLD = '''int isUpdateBl(int type)
{
	return __builtin_expect(type == 23 || type == 15, 0) || type == 16 || type == 9 || type == 10 || type == 24 || type == 25;
}'''

LONE = {'23,15': [23, 15], '15,23': [15, 23]}
REST = {'16 9 10 24 25': [16, 9, 10, 24, 25], '9 10 16 24 25': [9, 10, 16, 24, 25], '9 16 10 24 25': [9, 16, 10, 24, 25],
        '25 24 16 10 9': [25, 24, 16, 10, 9], '24 25 9 10 16': [24, 25, 9, 10, 16], '10 9 16 24 25': [10, 9, 16, 24, 25]}
FORM = ['if', 'elseif', 'ifret0']


def body(lone, rest, form):
    a, b = lone
    g = ' || '.join('type == %d' % t for t in rest)
    if form == 'if':
        return '\tif (type == %d)\n\t\treturn 1;\n\tif (type == %d)\n\t\treturn 1;\n\treturn %s;' % (a, b, g)
    if form == 'elseif':
        return '\tif (type == %d)\n\t\treturn 1;\n\telse if (type == %d)\n\t\treturn 1;\n\telse\n\t\treturn %s;' % (a, b, g)
    return '\tif (type == %d)\n\t\treturn 1;\n\tif (type == %d)\n\t\treturn 1;\n\tif (%s)\n\t\treturn 1;\n\treturn 0;' % (a, b, g)


FOCUS = ['_addUpdateBls', '_isUpdateBl']


def CASES(base):
    out = []
    for (lk, l), (rk, r), f in itertools.product(LONE.items(), REST.items(), FORM):
        v = body(l, r, f)
        out.append(('%s | %s | %s' % (lk, rk, f), lambda b, v=v: bdrun.sub(b, OLD, 'int isUpdateBl(int type)\n{\n%s\n}' % v, 1)))
    return out
