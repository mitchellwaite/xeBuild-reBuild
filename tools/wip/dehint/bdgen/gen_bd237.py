"""loadFileCrc (attempt 12): gen_bd231's `goto` form (layout right, name and crc swap registers: IRA pops by thread
frequency, and name must beat crc for edi) crossed with forms of the crc tail, which change crc's frequency.  No expect,
no pin."""
import itertools, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdhints, bdrun
import gen_bd231 as g

TAIL = '''	if (crc) {
		c = crc32(e->data, size);
		log_printf(1, " (crc32: 0x%08x ini: 0x%08x)\\n", c, crc);
		if (crc != c) {
			log_printf(0, "\\n******WARNING: '%s' crc32: 0x%08x expected: 0x%08x\\n", name, c, crc);
			return 1;
		}
	} else
		log_printf(1, "\\n");
	return 0;
'''
TAILS = {
    'src': TAIL,
    'early': '''	if (!crc) {
		log_printf(1, "\\n");
		return 0;
	}
	c = crc32(e->data, size);
	log_printf(1, " (crc32: 0x%08x ini: 0x%08x)\\n", c, crc);
	if (crc != c) {
		log_printf(0, "\\n******WARNING: '%s' crc32: 0x%08x expected: 0x%08x\\n", name, c, crc);
		return 1;
	}
	return 0;
''',
    'ceq': TAIL.replace('crc != c', 'c != crc'),
    'r': '''	r = 0;
	if (crc) {
		c = crc32(e->data, size);
		log_printf(1, " (crc32: 0x%08x ini: 0x%08x)\\n", c, crc);
		if (crc != c) {
			log_printf(0, "\\n******WARNING: '%s' crc32: 0x%08x expected: 0x%08x\\n", name, c, crc);
			r = 1;
		}
	} else
		log_printf(1, "\\n");
	return r;
''',
    'eqok': '''	if (crc) {
		c = crc32(e->data, size);
		log_printf(1, " (crc32: 0x%08x ini: 0x%08x)\\n", c, crc);
		if (crc == c)
			return 0;
		log_printf(0, "\\n******WARNING: '%s' crc32: 0x%08x expected: 0x%08x\\n", name, c, crc);
		return 1;
	}
	log_printf(1, "\\n");
	return 0;
''',
}


def CASES(base):
    t0 = bdhints.off(base, 'exp_verbose', 'pin_e')
    out = []
    for fk, tk in itertools.product(['src', 'goto'], TAILS):
        t = t0
        if fk == 'goto':
            t = bdrun.sub(t, g.OLD, g.FORMS['goto'].replace('P\n', g.P + '\n').replace('B\n', g.B + '\n'))
        t = bdrun.sub(t, TAIL, TAILS[tk], 1)
        if tk == 'r':
            t = bdrun.sub(t, '	size_t size;\n	uint32_t c;\n\n	f = fopen(name, "rb");', '	size_t size;\n	uint32_t c;\n	int r;\n\n	f = fopen(name, "rb");')
        out.append(('%s %s' % (fk, tk), t))
    return out


FOCUS = g.FOCUS
