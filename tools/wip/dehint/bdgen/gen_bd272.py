"""Attempt 16, exp_t10: the CG fallback calls checkBl itself instead of `goto chk`.  For type 10 everything after
chk: is a no-op (not a signature type, not 14, and the kit tail only breaks), so the behaviour is the same.  The
idea: the CG checkBl block (bbro block 14, 4 with the expect, 44 without) then sits behind a call-guarded edge
(PRED_CALL on `suGetCG != 0`) instead of the early-return-predicted break, about half the frequency.
Axes: arm form, checkBl's type argument, the type == 10 test (with or without the expect).  Runs on src as of e76f027f."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun

OLD = '''			} else if (__builtin_expect(type == 10, 0)) {
				if (!suGetCG(&e->data, &e->size))
					break;
				goto chk;
			} else
'''
ARM = {
    'if': '''				if (suGetCG(&e->data, &e->size))
					*pr = checkBl(e->data, e->size, %s, e->crc);
				break;
''',
    'brk': '''				if (!suGetCG(&e->data, &e->size))
					break;
				*pr = checkBl(e->data, e->size, %s, e->crc);
				break;
''',
}
TY = {'type': 'type', '10': '10'}
TEST = {'plain': 'type == 10', 'exp': '__builtin_expect(type == 10, 0)'}


def CASES(base):
    out = []
    for a, ty, te in itertools.product(ARM, TY, TEST):
        new = '\t\t\t} else if (%s) {\n' % TEST[te] + ARM[a] % TY[ty] + '\t\t\t} else\n'
        out.append(('%s %s %s' % (a, ty, te), lambda b, new=new: bdrun.sub(b, OLD, new, 1)))
    return out


FOCUS = ['_loadBlFiles']
