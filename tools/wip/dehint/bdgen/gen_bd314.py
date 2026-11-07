"""Attempt 20, loadFileCrc: attempt 12's goto form (layout right, both hints off) has name and size swapped (ebp/edi)
because IRA pushes name (r99) before crc (r103): name's frequency fell with the pad log's (504 against src's stale 2833).
Natural variations that change name's or crc's reference frequencies, or the pad log's: the goto arm nested or with
`&&`, the pad log's third argument, the zero-byte test spelled `size == 0` or with the log first, the crc tail as an
early `if (!crc)` return, the crc32 result compared as `c != crc`.  Runs on src as of a0108d6d."""
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
B = '\t\tlog_printf(1, "reading %s (0x%x bytes)", name, size);\n'
FORMS = {
    'and': '''	e->size = size;
	if (pad && (size & 15)) {
		e->size = align16(size);
		if (verbose && size != e->size) {
			log_printf(1, "reading %s (0x%x b pad 0x%x b)", name, size, ARG);
			goto alloc;
		}
	}
	if (verbose)
		log_printf(1, "reading %s (0x%x bytes)", name, size);
alloc:
''',
    'nest': '''	e->size = size;
	if (pad && (size & 15)) {
		e->size = align16(size);
		if (verbose) {
			if (size != e->size) {
				log_printf(1, "reading %s (0x%x b pad 0x%x b)", name, size, ARG);
				goto alloc;
			}
		}
	}
	if (verbose)
		log_printf(1, "reading %s (0x%x bytes)", name, size);
alloc:
''',
}
ZOLD = '''	if (!size) {
		fclose(f);
		log_printf(0, "\\n******WARNING: '%s' is a 0 byte file, loading skipped!\\n", name);
		return 1;
	}
'''
Z = {
    'src': ZOLD,
    'eq0': ZOLD.replace('if (!size) {', 'if (size == 0) {'),
}
COLD = '''	if (crc) {
		c = crc32(e->data, size);
		log_printf(1, " (crc32: 0x%08x ini: 0x%08x)\\n", c, crc);
		if (crc != c) {
'''
C = {
    'src': COLD,
    'cne': COLD.replace('if (crc != c) {', 'if (c != crc) {'),
}


def mk(b, form, arg, z, c):
    t = bdhints.off(b, 'exp_verbose', 'pin_e')
    old = OLD
    t = bdrun.sub(t, old, FORMS[form].replace('ARG', arg))
    t = bdrun.sub(t, ZOLD, Z[z])
    t = bdrun.sub(t, COLD, C[c])
    return t


def CASES(base):
    out = []
    for c in itertools.product(FORMS, ['align16(size)', 'e->size'], Z, C):
        out.append(('%s %s %s %s' % c, lambda b, c=c: mk(b, *c)))
    return out


FOCUS = ['_loadFileCrc']
