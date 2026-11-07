"""Attempt 26: gen_bd371's `c2` position (fail closes case 2: `if (e->offset) break; fail: *pr = -1; break;`) on the
and9 base, with the barrier kept or off, and loadBl's other tricks off alone or in pairs (t5le, exp_pr, exp_t10, the
`else if (type)` dead test as a plain else, the constant_p entry gone, pin_d).  Also on src's fallback (if/else-if)
for comparison.  Runs on src as of 9744ca00."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun, bdhints
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_bd370 as g0

C2 = '''		if (e->offset)
			break;
	fail:
		__asm__ __volatile__("");
		*pr = -1;
		break;
	default:'''
ELSE_OLD = '''				} else if (type)
					log_printf(1, "loaded %s, signature check passed!\\n", e->name);'''
ELSE_NEW = '''				} else
					log_printf(1, "loaded %s, signature check passed!\\n", e->name);'''
CP_OLD = '''		if ((char *)__builtin_constant_p(i) == (char *)1 && (char *)__builtin_constant_p(type) == (char *)1) {
			type = (type & 1) + 18;
			goto chk;
		}
'''
EXTRA = {
    'else': lambda b: bdrun.sub(b, ELSE_OLD, ELSE_NEW, 1),
    'cp': lambda b: bdrun.sub(b, CP_OLD, '', 1),
}
OFFS = ['lab_t5le', 'exp_pr', 'exp_t10', 'pin_d', 'else', 'cp']


def mk(b, fb, pos, bar, offs):
    if fb == 'and9':
        b = g0.PRE(b)
    if pos == 'c2':
        b = bdrun.sub(b, g0.SMC_OLD, C2, 1)
        b = bdrun.sub(b, g0.END_OLD, '}\n', 1)
        if not bar:
            b = bdrun.sub(b, '\tfail:\n\t\t__asm__ __volatile__("");\n', '\tfail:\n', 1)
    elif not bar:
        b = bdrun.sub(b, 'fail:\n\t__asm__ __volatile__("");\n', 'fail:\n', 1)
    for o in offs:
        b = EXTRA[o](b) if o in EXTRA else bdhints.off(b, o)
    return b


def CASES(base):
    out = []
    sets = [()] + [(o,) for o in OFFS] + list(itertools.combinations(OFFS[:3], 2)) + [tuple(OFFS[:3])]
    for fb, pos, bar, offs in itertools.product(['and9', 'src'], ['c2', 'end'], [1, 0], sets):
        if pos == 'end' and fb == 'and9' and bar and not offs:
            pass
        out.append(('%s %s %s %s' % (fb, pos, 'bar' if bar else 'nobar', '+'.join(offs) or '-'),
                    lambda b, a=(fb, pos, bar, offs): mk(b, *a)))
    return out


FOCUS = ['_loadBlFiles']
