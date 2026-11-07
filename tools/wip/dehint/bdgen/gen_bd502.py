"""Attempt 38: case 6's checkBl through `goto chk` (the same behaviour: for type 6 after a good checkBl the
signature block and the tail do nothing), as a real entry into chk that could stand in for the __builtin_constant_p
entry, or change its weight.  Axes: case 6 form x constant_p entry kept / off x exp_t10 kept / off.
Run: python tools/wip/dehint/bdrun.py tools/wip/dehint/bdgen/gen_bd502.py"""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun

C6 = '''		*pr = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);
		if (!*pr)
			*pr = checkBl(e->data, e->size, 6, e->crc);
		break;
	case 24:
'''
FORMS = {
    'src': C6,
    'chk': '''		*pr = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);
		if (*pr)
			break;
		goto chk;
	case 24:
''',
    'chk_if': '''		*pr = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);
		if (!*pr)
			goto chk;
		break;
	case 24:
''',
}
CP_A = '''		if ((char *)__builtin_constant_p(i) == (char *)1 && (char *)__builtin_constant_p(type) == (char *)1) {
			type = (type & 1) + 18;
			goto chk;
		}
'''


def mk(b, f, cp, t10):
    b = bdrun.sub(b, C6, FORMS[f], 1)
    if not cp:
        b = bdrun.sub(b, CP_A, '', 1)
    if not t10:
        b = bdhints.off(b, 'exp_t10')
    return b


def CASES(base):
    out = []
    for f, cp, t10 in itertools.product(FORMS, [1, 0], [1, 0]):
        if f == 'src' and cp and t10:
            continue
        out.append(('%s cp%d t10%d' % (f, cp, t10), lambda b, c=(f, cp, t10): mk(b, *c)))
    return out


FOCUS = ['_loadBlFiles']
