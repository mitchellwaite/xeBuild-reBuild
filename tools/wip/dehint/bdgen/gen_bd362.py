"""Attempt 25, exp_t10: gen_bd360's `and9` family (the CF-failure flow passes the `type == 10` test at
profile_estimate; 28 loose without the expect, IDENTICAL with it), without the CG `goto chk` (a type-10 entry then
passes the SE test, which is false for it), and with the update tests as one condition.  Expect off.
Runs on src as of 3778d12d."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun

OLD = '''		if (*pr) {
			if (type == 9) {
				if (!suGetCF(&e->data, &e->size))
					break;
			} else if (__builtin_expect(type == 10, 0)) {
				if (!suGetCG(&e->data, &e->size))
					break;
				goto chk;
			} else
				break;
		}
'''
CF = 'suGetCF(&e->data, &e->size)'
CG = 'suGetCG(&e->data, &e->size)'
F = {
    'nogo1': '''		if (*pr && !(type == 9 && %s) && !(type == 10 && %s))
			break;
''' % (CF, CG),
    'nogo2': '''		if (*pr) {
			if (!(type == 9 && %s) && !(type == 10 && %s))
				break;
		}
''' % (CF, CG),
    'nogo3': '''		if (*pr) {
			if ((type != 9 || !%s) && (type != 10 || !%s))
				break;
		}
''' % (CF, CG),
    'nogo4': '''		if (*pr) {
			if (type != 9 || !%s) {
				if (type != 10 || !%s)
					break;
			}
		}
''' % (CF, CG),
    'go_or': '''		if (*pr) {
			if (!(type == 9 && %s)) {
				if (!(type == 10 && %s))
					break;
				goto chk;
			}
		}
''' % (CF, CG),
    'go_in': '''		if (*pr && !(type == 9 && %s)) {
			if (type != 10 || !%s)
				break;
			goto chk;
		}
''' % (CF, CG),
}


def CASES(base):
    return [(k, lambda b, k=k: bdrun.sub(b, OLD, F[k], 1)) for k in F]


FOCUS = ['_loadBlFiles']
