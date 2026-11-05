"""loadFileCrc (attempt 12): around gen_bd231's `goto` form (layout right, 38 lines of name/size registers swapped).
The pad arm logs and jumps over the bytes log; variants of how the pad arm's tests are written and where `alloc` is."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import bdhints
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_bd231 as g

P, B = g.P, g.B
FORMS = {
    'goto': g.FORMS['goto'],
    'nest': '''	e->size = size;
	if (pad && (size & 15)) {
		e->size = align16(size);
		if (verbose) {
			if (size != e->size) {
				P
				goto alloc;
			}
		}
	}
	if (verbose)
		B
alloc:
''',
    'nest2': '''	e->size = size;
	if (pad && (size & 15)) {
		e->size = align16(size);
		if (size != e->size) {
			if (verbose)
				P
			goto alloc;
		}
	}
	if (verbose)
		B
alloc:
''',
    'outer': '''	e->size = size;
	if (pad && (size & 15))
		e->size = align16(size);
	if (verbose) {
		if (size != e->size) {
			P
			goto alloc;
		}
		B
	}
alloc:
''',
    'vfirst': '''	e->size = size;
	if (pad && (size & 15)) {
		e->size = align16(size);
		if (verbose && e->size != size) {
			P
			goto alloc;
		}
	}
	if (verbose)
		B
alloc:
''',
    'ret': '''	e->size = size;
	if (pad && (size & 15)) {
		e->size = align16(size);
		if (verbose && size != e->size) {
			P
			goto alloc;
		}
	}
	if (verbose)
		B
alloc:
	;
''',
    'padvar': '''	e->size = size;
	if (pad && (size & 15)) {
		e->size = align16(size);
		if (verbose && size != e->size) {
			log_printf(1, "reading %s (0x%x b pad 0x%x b)", name, size, e->size);
			goto alloc;
		}
	}
	if (verbose)
		B
alloc:
''',
}


def CASES(base):
    t0 = bdhints.off(base, 'exp_verbose', 'pin_e')
    if g.OLD not in t0:
        raise ValueError('old')
    out = []
    for k, f in FORMS.items():
        f = f.replace('P\n', P + '\n').replace('B\n', B + '\n')
        out.append((k, t0.replace(g.OLD, f)))
    return out


FOCUS = g.FOCUS
