"""loadFileCrc with pin_e off (and exp_verbose on or off): neutral shapes crossed: helpers for the reading log, the crc part and the load part; locals for padded size and data."""
import itertools, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdtricks

a = '''	e->size = size;
	if (pad && (size & 15))
		e->size = (size + 15) & ~15;
'''
LOGOLD = '''	/* hints: the "bytes" log must be hot enough for bb-reorder's second round
	   (build.sh's expect probability, 92-99); the pin sets e's register in the
	   out-of-line copy only (callers with pad == 0 drop this block) */
	if (__builtin_expect(verbose, 1)) {
		if (size != e->size) {
			log_printf(1, "reading %s (0x%x b pad 0x%x b)", name, size, (size + 15) & ~15);
			__asm__("" : : "S"(e));
		} else
			log_printf(1, "reading %s (0x%x bytes)", name, size);
	}
'''
def lg(v, padded='e->size'):
    t = 'verbose' if v else '__builtin_expect(verbose, 1)'
    return '	if (%s) {\n		if (size != %s)\n			log_printf(1, "reading %%s (0x%%x b pad 0x%%x b)", name, size, (size + 15) & ~15);\n		else\n			log_printf(1, "reading %%s (0x%%x bytes)", name, size);\n	}\n' % (t, padded)

LOGH = '''static void logReading(const char *name, size_t size, uint32_t padded)
{
	if (size != padded)
		log_printf(1, "reading %s (0x%x b pad 0x%x b)", name, size, (size + 15) & ~15);
	else
		log_printf(1, "reading %s (0x%x bytes)", name, size);
}

'''
LOGH2 = '''static void logReading(const char *name, size_t size, uint32_t padded, int verbose)
{
	if (verbose) {
		if (size != padded)
			log_printf(1, "reading %s (0x%x b pad 0x%x b)", name, size, (size + 15) & ~15);
		else
			log_printf(1, "reading %s (0x%x bytes)", name, size);
	}
}

'''
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
}
'''
CRCH = '''static int checkCrc(const char *name, const uint8_t *data, size_t size, uint32_t crc)
{
	uint32_t c;

	if (!crc) {
		log_printf(1, "\\n");
		return 0;
	}
	c = crc32(data, size);
	log_printf(1, " (crc32: 0x%08x ini: 0x%08x)\\n", c, crc);
	if (crc != c) {
		log_printf(0, "\\n******WARNING: '%s' crc32: 0x%08x expected: 0x%08x\\n", name, c, crc);
		return 1;
	}
	return 0;
}

'''
HEAD = 'int loadFileCrc(const char *name, struct fileent *e, int verbose, int pad, uint32_t crc)\n{\n'
READ = '''	e->data = calloc(e->size + 0x10000, 1);
	if (!e->data)
		return -2;
	fread(e->data, size, 1, f);
	fclose(f);
'''


def CASES(base):
    out = []
    for vb, lf, cr, pl, rd, decl in itertools.product((0, 1), ('in', 'in0', 'hv', 'h', 'p'), (0, 1), (0, 1), (0, 1), (0, 1, 2)):
        t = base
        pre = ''
        if lf == 'in':
            t = t.replace(LOGOLD, lg(vb))
        elif lf == 'in0':
            t = t.replace(LOGOLD, lg(vb, 'e->size').replace('size != e->size', 'e->size != size'))
        elif lf == 'hv':
            if vb:
                continue
            pre += LOGH2
            t = t.replace(LOGOLD, '	logReading(name, size, e->size, verbose);\n')
        elif lf == 'h':
            pre += LOGH
            t = t.replace(LOGOLD, '	if (%s)\n		logReading(name, size, e->size);\n' % ('verbose' if vb else '__builtin_expect(verbose, 1)'))
        else:
            t = t.replace(LOGOLD, lg(vb, 'padded'))
            t = t.replace(a, '	padded = size;\n	if (pad && (size & 15))\n		padded = (size + 15) & ~15;\n	e->size = padded;\n')
        if cr:
            pre += CRCH
            t = t.replace(TAIL, '	return checkCrc(name, e->data, size, crc);\n}\n')
        if pl:
            t = t.replace(a, '	e->size = pad && (size & 15) ? (size + 15) & ~15 : size;\n')
        if rd:
            t = t.replace(READ, '	data = calloc(e->size + 0x10000, 1);\n	e->data = data;\n	if (!data)\n		return -2;\n	fread(data, size, 1, f);\n	fclose(f);\n')
        d = '	FILE *f;\n	size_t size;\n	uint32_t c;\n'
        extra = ('	uint32_t padded;\n' if lf == 'p' else '') + ('	uint8_t *data;\n' if rd else '')
        if decl == 1:
            d2 = '	size_t size;\n	uint32_t c;\n	FILE *f;\n'
        elif decl == 2:
            d2 = '	uint32_t c;\n	size_t size;\n	FILE *f;\n'
        else:
            d2 = d
        t = t.replace(HEAD + d, pre + HEAD + d2 + extra)
        out.append(('v%d %s crc%d pl%d rd%d decl%d' % (vb, lf, cr, pl, rd, decl), t))
    return out
