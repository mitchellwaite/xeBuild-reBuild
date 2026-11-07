"""Attempt 20, loadFileCrc: two bytes logs (one per pad arm, so the non-pad path reaches its own before
profile_estimate and the pad log keeps calls on both sides of its compare).  Attempt 12's dup forms moved .rdata: the
reference has the bytes literal (0x3d) before the pad one (0x58), and expand emits literals in block order, so here the
bytes log comes first in the text: the non-pad arm first (negated pad test), or `size == e->size` first in the pad arm.
Both hints off.  Runs on src as of a0108d6d."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun

OLD = '''	e->size = size;
	if (pad && (size & 15))
		e->size = align16(size);
	/* hints: the "bytes" log must be hot enough for bb-reorder's second round
	   (build.sh's expect probability, 92-99); the pin sets e's register in the
	   out-of-line copy only (callers with pad == 0 drop this block) */
	if (verbose) {
		if (size != e->size) {
			log_printf(1, "reading %s (0x%x b pad 0x%x b)", name, size, align16(size));
		} else
			log_printf(1, "reading %s (0x%x bytes)", name, size);
	}
'''
P = 'log_printf(1, "reading %s (0x%x b pad 0x%x b)", name, size, align16(size));'
B = 'log_printf(1, "reading %s (0x%x bytes)", name, size);'

PADARM = {
    'ne': '\t\tif (size != e->size)\n\t\t\tP\n\t\telse\n\t\t\tB\n',
    'eq': '\t\tif (size == e->size)\n\t\t\tB\n\t\telse\n\t\t\tP\n',
}
FORMS = {
    # non-pad arm first
    'npfirst': '''	e->size = size;
	if (!pad || !(size & 15)) {
		if (verbose)
			B
	} else {
		e->size = align16(size);
		if (verbose) {
PADARM		}
	}
''',
    'npfirst2': '''	e->size = size;
	if (!(pad && (size & 15))) {
		if (verbose)
			B
	} else {
		e->size = align16(size);
		if (verbose) {
PADARM		}
	}
''',
    'padfirst': '''	e->size = size;
	if (pad && (size & 15)) {
		e->size = align16(size);
		if (verbose) {
PADARM		}
	} else if (verbose)
		B
''',
    'vfirst': '''	e->size = size;
	if (pad && (size & 15))
		e->size = align16(size);
	if (verbose) {
		if (!pad || !(size & 15))
			B
		else {
PADARM		}
	}
''',
}


def mk(b, form, pa):
    t = bdhints.off(b, 'exp_verbose', 'pin_e')
    arm = PADARM[pa]
    if form == 'vfirst':
        arm = arm.replace('\t\t', '\t\t\t')
    else:
        arm = arm.replace('\t\t', '\t\t\t')
    f = FORMS[form].replace('PADARM', arm).replace('P\n', P + '\n').replace('B\n', B + '\n')
    return bdrun.sub(t, OLD, f)


def CASES(base):
    out = []
    for c in itertools.product(FORMS, PADARM):
        out.append(('%s %s' % c, lambda b, c=c: mk(b, *c)))
    return out


FOCUS = ['_loadFileCrc']
