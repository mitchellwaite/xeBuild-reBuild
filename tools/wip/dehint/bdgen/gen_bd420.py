"""Attempt 30: on case 6 first + and9 (gen_bd418's c2c6 base) with the barrier off, where fail lives: c2 (closing case
2, the 1 loose / 7 strict near miss: only the size log's own -1), c23in (inside the size log's if, case 2's smc test
`goto fail`), c23end (case 23 written with the good path first and the log falling into fail), end (src's), and the
fallback src / and9.  Each also with the barrier kept.  Runs on src as of 6083630d."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdrun, bdhints
import a30lib
import gen_bd410 as g0
import gen_bd417 as g7

SZ = '''		if ((e->size & ~3) != e->size) {
			log_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);
			goto fail;
		}
		appendAddonPatches(e);
		break;
'''
SZ_IN = '''		if ((e->size & ~3) != e->size) {
			log_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);
		fail:
			BAR*pr = -1;
			break;
		}
		appendAddonPatches(e);
		break;
'''
SZ_END = '''		if ((e->size & ~3) == e->size) {
			appendAddonPatches(e);
			break;
		}
		log_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);
	fail:
		BAR*pr = -1;
		break;
'''
END = '''	return;
	/* one -1 block for the patch size, SMC and (xb.type <= BUILD_DEVGL16) signature
	   failures: the asm keeps it a block of its own (else the -1 is appended
	   to the size log, which crossjump can't then share) */
fail:
	__asm__ __volatile__("");
	*pr = -1;
}
'''
FB = g0.FB
AND9 = g0.AND9


def c6(b):
    i, j = bdrun.fnspan(b, a30lib.LB)
    h, a, t = g7.arms(b[i:j])
    n = g7.names(a)
    return g7.reorder(b, ['6'] + [x for x in n if x != '6'])


def mk(b, fb, pos, bar):
    if fb == 'and9':
        b = bdrun.sub(b, FB, AND9, 1)
    B = '__asm__ __volatile__("");\n\t\t\t' if bar else ''
    if pos == 'c2':
        b = bdrun.sub(b, g0.C2A, g0.C2B, 1)
        b = bdrun.sub(b, g0.ENDA, '}\n', 1)
        if not bar:
            b = bdhints.off(b, 'vol_fail')
    elif pos in ('c23in', 'c23end'):
        b = bdrun.sub(b, SZ, (SZ_IN if pos == 'c23in' else SZ_END.replace('\t\t\t', '\t\t')).replace('BAR', B if pos == 'c23in' else B.replace('\t\t\t', '\t\t')), 1)
        b = bdrun.sub(b, g0.ENDA, '}\n', 1)
    else:
        if not bar:
            b = bdhints.off(b, 'vol_fail')
    return c6(b)


def CASES(base):
    return [(' '.join(map(str, k)), lambda b, k=k: mk(b, *k)) for k in itertools.product(['and9', 'src'], ['c2', 'c23in', 'c23end', 'end'], [0, 1])]


FOCUS = ['_loadBlFiles']
