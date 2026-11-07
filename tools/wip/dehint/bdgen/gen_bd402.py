"""Attempt 29: gen_bd401's diagnostic with the existing barrier instead of a new asm.  The empty asm moves from the head
of fail to a label after its -1 (`fail: *pr = -1; out: __asm__ __volatile__("");`), so the asm block is the return
block's prev_bb, and the fallback's failures `goto out` (a plain return there).  Edges into the asm block then get no
early return (fail's own preds don't either: fail's single successor is the asm block, not the return block), so the
CG and else edges lose PRED_TREE_EARLY_RETURN without a new hint; the barrier is already counted (vol_fail), so if it
matched, exp_t10's job would have moved onto it (report as such).  Axes: which failures go to out (CG + else, + CF),
the constant_p weight (near miss `pi it`, src's `pi pt`, `ii it`), t5le / exp_pr on or off.  Runs on src as of
1caeb924 with gen_bd390's PRE (exp_t10 off)."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun, bdhints
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_bd390 import PRE

FB = '''			if (type == 9) {
				if (!suGetCF(&e->data, &e->size))
					break;
			} else if (type == 10) {
				if (!suGetCG(&e->data, &e->size))
					break;
				goto chk;
			} else
				break;
'''
END = '''fail:
	__asm__ __volatile__("");
	*pr = -1;
}
'''
END2 = '''fail:
	*pr = -1;
out:
	__asm__ __volatile__("");
}
'''
CP = '(char *)__builtin_constant_p(i) == (char *)1 && __builtin_constant_p(type) == 1'
W = {
    'pi_it': CP,
    'pi_pt': '(char *)__builtin_constant_p(i) == (char *)1 && (char *)__builtin_constant_p(type) == (char *)1',
    'ii_it': '__builtin_constant_p(i) == 1 && __builtin_constant_p(type) == 1',
    'ii_pt': '__builtin_constant_p(i) == 1 && (char *)__builtin_constant_p(type) == (char *)1',
}
ARMS = {
    'cg_else': ('break', 'goto out', 'goto out'),
    'all': ('goto out', 'goto out', 'goto out'),
}


def fb(cf, cg, other):
    return '''			if (type == 9) {
				if (!suGetCF(&e->data, &e->size))
					%s;
			} else if (type == 10) {
				if (!suGetCG(&e->data, &e->size))
					%s;
				goto chk;
			} else
				%s;
''' % (cf, cg, other)


def mk(b, a, w, h):
    b = bdrun.sub(b, FB, fb(*ARMS[a]), 1)
    b = bdrun.sub(b, END, END2, 1)
    b = bdrun.sub(b, CP, W[w], 1)
    if h:
        b = bdhints.off(b, *h)
    return b


HS = {'': (), 'nt5': ('lab_t5le',), 'npr': ('exp_pr',), 'both': ('lab_t5le', 'exp_pr')}


def CASES(base):
    return [('%s %s %s' % (a, w, h), lambda b, a=a, w=w, h=h: mk(b, a, w, HS[h]))
            for a, w, h in itertools.product(ARMS, W, HS)]


FOCUS = ['_loadBlFiles']
