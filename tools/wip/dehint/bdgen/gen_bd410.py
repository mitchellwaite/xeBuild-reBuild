"""Attempt 30 baseline: src with all seven loadBl hints off (a30lib.off7), and with each one kept back alone, plus the
and9 + c2 base (attempts 25/26) with the same seven off.  Runs on src as of 6083630d."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdrun, bdhints
from a30lib import off7

FB = '''			if (type == 9) {
				if (!suGetCF(&e->data, &e->size))
					break;
			} else if (__builtin_expect(type == 10, 0)) {
				if (!suGetCG(&e->data, &e->size))
					break;
				goto chk;
			} else
				break;
'''
AND9 = '''			if (type == 9 && suGetCF(&e->data, &e->size))
				;
			else if (__builtin_expect(type == 10, 0) && suGetCG(&e->data, &e->size))
				goto chk;
			else
				break;
'''
C2A = '''		e->offset = smcSetLoad(e->size);
		if (!e->offset)
			goto fail;
		break;
'''
C2B = '''		e->offset = smcSetLoad(e->size);
		if (e->offset)
			break;
	fail:
		__asm__ __volatile__("");
		*pr = -1;
		break;
'''
ENDA = '''	return;
	/* one -1 block for the patch size, SMC and (xb.type <= BUILD_DEVGL16) signature
	   failures: the asm keeps it a block of its own (else the -1 is appended
	   to the size log, which crossjump can't then share) */
fail:
	__asm__ __volatile__("");
	*pr = -1;
}
'''


def and9c2(b):
    b = bdrun.sub(b, FB, AND9, 1)
    b = bdrun.sub(b, C2A, C2B, 1)
    b = bdrun.sub(b, ENDA, '}\n', 1)
    return b


KEEPS = ['exp_t10', 'exp_pr', 'lab_t5le', 'vol_fail', 'cp', 'etype']


def CASES(base):
    c = [('src off7', lambda b: off7(b)),
         ('src off7 -pin_d', lambda b: bdhints.off(off7(b), 'pin_d'))]
    c += [('src off7 keep ' + k, lambda b, k=k: off7(b, (k,))) for k in KEEPS]
    c += [('c2 off7', lambda b: off7(and9c2(b)))]
    c += [('c2 off7 keep ' + k, lambda b, k=k: off7(and9c2(b), (k,))) for k in KEEPS]
    return c


FOCUS = ['_loadBlFiles']
