"""loadFileCrc (attempt 12): whole forms of the pad-and-log section, no expect, no pin.
With src's form the non-pad path reaches the "bytes" log only through a jump thread (vrp/dom: size == e->size is known
there), and the thread leaves the log's frequency at 1102 although about 2950 flows into it; bb-reorder's round 2 needs
2000.  Forms here give the non-pad path its own way to the log before profile_estimate."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import bdhints

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
FORMS = {
    # two bytes logs, tail merge may join them
    'dup': '''	e->size = size;
	if (pad && (size & 15)) {
		e->size = align16(size);
		if (verbose) {
			if (size != e->size)
				P
			else
				B
		}
	} else if (verbose)
		B
''',
    'dup2': '''	e->size = size;
	if (pad && (size & 15)) {
		e->size = align16(size);
		if (verbose && size != e->size)
			P
		else if (verbose)
			B
	} else if (verbose)
		B
''',
    # the bytes log when nothing was padded, tested on the result
    'two': '''	e->size = size;
	if (pad && (size & 15))
		e->size = align16(size);
	if (verbose && size != e->size)
		P
	else if (verbose)
		B
''',
    'two2': '''	e->size = size;
	if (pad && (size & 15))
		e->size = align16(size);
	if (verbose && size == e->size)
		B
	else if (verbose)
		P
''',
    # a goto to the bytes log
    'goto': '''	e->size = size;
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
''',
    'goto2': '''	e->size = size;
	if (pad && (size & 15)) {
		e->size = align16(size);
		if (!verbose)
			goto alloc;
		if (size != e->size) {
			P
			goto alloc;
		}
	} else if (!verbose)
		goto alloc;
	B
alloc:
''',
    'goto3': '''	e->size = size;
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
}


def CASES(base):
    t0 = bdhints.off(base, 'exp_verbose', 'pin_e')
    if OLD not in t0:
        raise ValueError('old')
    out = []
    for k, f in FORMS.items():
        f = f.replace('P\n', P + '\n').replace('B\n', B + '\n')
        out.append((k, t0.replace(OLD, f)))
    return out


FOCUS = ['_loadFileCrc', '_loadBaseFile', '_loadCommonFile', '_loadLocalFile', '_loadBaseFileMeta', '_loadInputFile', '_loadBinFile']
