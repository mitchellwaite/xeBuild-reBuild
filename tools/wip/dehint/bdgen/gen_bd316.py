"""Attempt 20, loadFileCrc: gen_bd315's `vfirst` match (the pad test repeated inside `if (verbose)`) in more natural
spellings: an if/else-if chain, the positive pad test first, the padded arm with the pad log only (no inner compare),
the pad condition in a `padded` flag (int or BOOL, set before or after the first store) used by both tests.  Both hints
off.  Runs on src as of a0108d6d."""
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

LOGS = {
    # pad test negated first
    'neg_nest': '''	if (verbose) {
		if (!COND)
			B
		else {
			if (size != e->size)
				P
			else
				B
		}
	}
''',
    'neg_chain': '''	if (verbose) {
		if (!COND)
			B
		else if (size != e->size)
			P
		else
			B
	}
''',
    'neg_ponly': '''	if (verbose) {
		if (!COND)
			B
		else
			P
	}
''',
    'pos_nest': '''	if (verbose) {
		if (COND) {
			if (size != e->size)
				P
			else
				B
		} else
			B
	}
''',
    'pos_ponly': '''	if (verbose) {
		if (COND)
			P
		else
			B
	}
''',
    'pos_and': '''	if (verbose) {
		if (COND && size != e->size)
			P
		else
			B
	}
''',
}
HEADS = {
    'plain': ('''	e->size = size;
	if (pad && (size & 15))
		e->size = align16(size);
''', None),
    'flag_after': ('''	e->size = size;
	padded = pad && (size & 15);
	if (padded)
		e->size = align16(size);
''', 'padded'),
    'flag_before': ('''	padded = pad && (size & 15);
	e->size = size;
	if (padded)
		e->size = align16(size);
''', 'padded'),
}
DECL = '\tFILE *f;\n\tsize_t size;\n\tuint32_t c;\n'


def mk(b, head, logs, ft):
    t = bdhints.off(b, 'exp_verbose', 'pin_e')
    h, flag = HEADS[head]
    if not flag and ft != 'int':
        return None
    cond = flag or 'pad && (size & 15)'
    ncond = '!' + flag if flag else '!pad || !(size & 15)'
    lg = LOGS[logs]
    lg = lg.replace('!COND', ncond).replace('COND', cond if flag or 'COND &&' not in lg else '(pad && (size & 15))')
    lg = lg.replace('(pad && (size & 15)) &&', 'pad && (size & 15) &&')
    lg = lg.replace('P\n', P + '\n').replace('B\n', B + '\n')
    t = bdrun.sub(t, OLD, h + lg)
    if flag:
        t = bdrun.sub(t, 'int loadFileCrc(const char *name, struct fileent *e, int verbose, int pad, uint32_t crc)\n{\n' + DECL,
                      'int loadFileCrc(const char *name, struct fileent *e, int verbose, int pad, uint32_t crc)\n{\n' + DECL + '\t%s padded;\n' % ft)
    return t


def CASES(base):
    out = []
    for c in itertools.product(HEADS, LOGS, ['int', 'BOOL']):
        out.append(('%s %s %s' % c, lambda b, c=c: mk(b, *c)))
    return out


FOCUS = ['_loadFileCrc']
