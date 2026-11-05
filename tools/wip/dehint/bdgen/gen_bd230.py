"""loadFileCrc (attempt 12): the verbose block's structure with no expect and no e pin.  With both off only the
"bytes" log's block is placed late (18 loose); it needs frequency >= 2000 for bb-reorder's round 2.
Axes: the size compare's opcode (the nonequal heuristic predicts `!=` taken, so the bytes arm gets 28%), which arm comes
first, where the verbose test sits relative to the pad test, and the pad log's last argument."""
import itertools, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import bdhints, bdrun

OLD = '''	if (verbose) {
		if (size != e->size) {
			log_printf(1, "reading %s (0x%x b pad 0x%x b)", name, size, align16(size));
		} else
			log_printf(1, "reading %s (0x%x bytes)", name, size);
	}
'''
PAD = 'log_printf(1, "reading %%s (0x%%x b pad 0x%%x b)", name, size, %s);'
BYTES = 'log_printf(1, "reading %s (0x%x bytes)", name, size);'
TESTS = {
    'ne': ('size != e->size', True),
    'gt': ('e->size > size', True),
    'lt': ('size < e->size', True),
    'ge': ('e->size >= size', None),  # not the same test; skip
    'eq': ('size == e->size', False),
    'le': ('e->size <= size', False),
}
ARGS = {'a16': 'align16(size)', 'es': 'e->size'}
VT = {'v': 'verbose', 'v0': 'verbose != 0', 'vg': 'verbose > 0'}


def CASES(base):
    t0 = bdhints.off(base, 'exp_verbose', 'pin_e')
    if OLD not in t0:
        raise ValueError('old')
    out = []
    for (tk, (tst, padfirst)), ak, vk in itertools.product(TESTS.items(), ARGS, VT):
        if padfirst is None:
            continue
        p, b = PAD % ARGS[ak], BYTES
        if padfirst:
            body = '\tif (%s) {\n\t\tif (%s)\n\t\t\t%s\n\t\telse\n\t\t\t%s\n\t}\n' % (VT[vk], tst, p, b)
        else:
            body = '\tif (%s) {\n\t\tif (%s)\n\t\t\t%s\n\t\telse\n\t\t\t%s\n\t}\n' % (VT[vk], tst, b, p)
        out.append(('%s %s %s' % (tk, ak, vk), t0.replace(OLD, body)))
    # verbose inside each pad arm (no size compare: the arms decide)
    for ak in ARGS:
        alt = t0.replace('''	e->size = size;
	if (pad && (size & 15))
		e->size = align16(size);
''' + OLD, '''	e->size = size;
	if (pad && (size & 15)) {
		e->size = align16(size);
		if (verbose)
			%s
	} else if (verbose)
		%s
''' % (PAD % ARGS[ak], BYTES))
        out.append(('arms %s' % ak, alt))
    return out


FOCUS = ['_loadFileCrc', '_loadBaseFile', '_loadCommonFile', '_loadLocalFile', '_loadBaseFileMeta', '_loadInputFile', '_loadBinFile']
