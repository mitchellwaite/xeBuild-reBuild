"""Attempt 17, exp_upd: types, which earlier type sweeps didn't cover for isUpdateBl.  Parameter type x return type
x addUpdateBls' `type` local, no expect.  Runs on src as of d09240ad."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun

OLD = '''int isUpdateBl(int type)
{
	return __builtin_expect(type == 23 || type == 15, 0) || type == 16 || type == 9 || type == 10 || type == 24 || type == 25;
}
'''
NEW = '''%s isUpdateBl(%s type)
{
	return type == 23 || type == 15 || type == 16 || type == 9 || type == 10 || type == 24 || type == 25;
}
'''
LOC_OLD = '''	uint32_t i;
	int type, j, off = 0;

	for (i = 1; i < (uint32_t)xb.nFlashFiles; i++) {
		e = &xb.files[i];
		type = e->type;
		if (!isUpdateBl(type))'''
PT = ['int', 'uint32_t', 'unsigned', 'long', 'uint8_t', 'uint16_t', 'char', 'int8_t']
RT = ['int', 'uint32_t', '_Bool', 'uint8_t', 'long']
LT = ['int', 'uint32_t']


def mk(b, pt, rt, lt):
    b = bdrun.sub(b, OLD, NEW % (rt, pt), 1)
    if lt != 'int':
        new = LOC_OLD.replace('\tint type, j, off = 0;', '\t%s type;\n\tint j, off = 0;' % lt)
        b = bdrun.sub(b, LOC_OLD, new, 1)
    return b


def CASES(base):
    return [('%s %s %s' % c, lambda b, c=c: mk(b, *c)) for c in itertools.product(PT, RT, LT)]


FOCUS = ['_addUpdateBls', '_isUpdateBl']
