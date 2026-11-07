"""Attempt 26: gen_bd371's `c2` fail position (fail closes case 2) without the barrier, crossed with gen_bd363's update
fallbacks (src, and9, nest9, nogo; type == 10 expect on or off), the size error through fail or its own
`*pr = -1; break;`, and the tail forms (t5le / `*pr` expect on or off, plain break).  Runs on src as of 9744ca00."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_bd370 as g0
import gen_bd363 as g3

C2 = '''		if (e->offset)
			break;
	fail:
		*pr = -1;
		break;
	default:'''


def mk(b, f, t10, sz, tk, lab, exp):
    b = bdrun.sub(b, g3.OLD, g3.FB[f].replace('T10', g3.T10).replace(g3.T10, g3.T10S[t10]), 1)
    b = bdrun.sub(b, g0.SMC_OLD, C2, 1)
    b = bdrun.sub(b, g0.END_OLD, '}\n', 1)
    b = bdrun.sub(b, g0.SIZE_OLD, g0.SIZE[sz], 1)
    b = bdrun.sub(b, g0.TAIL_OLD, g0.tail(tk, lab, exp), 1)
    return b


def CASES(base):
    out = []
    tails = [('g', 1, 1), ('g', 0, 1), ('g', 1, 0), ('g', 0, 0), ('plain', 0, 0)]
    for f, t10, sz, (tk, lab, exp) in itertools.product(g3.FB, g3.T10S, ['g', 'brk'], tails):
        out.append(('%s %s %s %s%s%s' % (f, t10, sz, tk, ' lab' if lab else '', ' exp' if exp else ''),
                    lambda b, a=(f, t10, sz, tk, lab, exp): mk(b, *a)))
    return out


FOCUS = ['_loadBlFiles']
