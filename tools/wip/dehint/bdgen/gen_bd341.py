"""Attempt 23, exp_upd: if-chains.  At profile_estimate a lone `if (type == 23) return 1;` gets nonequal + early return
(19.9%, inside the <= 28% window); post-IPA ifcombine can pair it with a following lone test into `(23|x)` (a fresh
SSA bool that dom2 then reuses for the body's `type == 23`), as long as the inner block holds only its cond.
Axes: which tests are lone ifs and which are an `||` group, and the order.  Runs on src as of 604028f1."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun

OLD = '''int isUpdateBl(int type)
{
	return __builtin_expect(type == 23 || type == 15, 0) || type == 16 || type == 9 || type == 10 || type == 24 || type == 25;
}'''


def ifs(ts, last='ret0'):
    s = ''.join('\tif (type == %d)\n\t\treturn 1;\n' % t for t in ts[:-1])
    if last == 'ret0':
        return s + '\tif (type == %d)\n\t\treturn 1;\n\treturn 0;' % ts[-1]
    return s + '\treturn type == %d;' % ts[-1]


def mixed(lone, rest):
    return ''.join('\tif (type == %d)\n\t\treturn 1;\n' % t for t in lone) + '\treturn ' + ' || '.join('type == %d' % t for t in rest) + ';'


F = {
    'ifs src': ifs([23, 15, 16, 9, 10, 24, 25]),
    'ifs src retlast': ifs([23, 15, 16, 9, 10, 24, 25], 'x'),
    'm 23,15 | 16 9 10 24 25': mixed([23, 15], [16, 9, 10, 24, 25]),
    'm 23,15 | 9 16 10 24 25': mixed([23, 15], [9, 16, 10, 24, 25]),
    'm 23,15,16,9 | 10 24 25': mixed([23, 15, 16, 9], [10, 24, 25]),
    'm 23 | 15 9 16 10 24 25': mixed([23], [15, 9, 16, 10, 24, 25]),
    'm 23 | 15 16 9 10 24 25': mixed([23], [15, 16, 9, 10, 24, 25]),
    'm 23 | 9 15 16 10 24 25': mixed([23], [9, 15, 16, 10, 24, 25]),
    'ifs 23 15 9 16 10 24 25': ifs([23, 15, 9, 16, 10, 24, 25]),
    'ifs 23 9 15 16 10 24 25': ifs([23, 9, 15, 16, 10, 24, 25]),
}
FOCUS = ['_addUpdateBls', '_isUpdateBl']


def CASES(base):
    return [(k, lambda b, v=v: bdrun.sub(b, OLD, 'int isUpdateBl(int type)\n{\n%s\n}' % v, 1)) for k, v in F.items()]
