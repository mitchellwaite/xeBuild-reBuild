"""loadFileCrc with no expect and no pin: the ternary form (gen_bd106 pl1) makes the bytes log hot enough on its own, but it sinks the first e->size store.  Forms with the two stores."""
import itertools
A = '''	e->size = size;
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
L = """	if (__builtin_expect(verbose, 1)) {
		if (%s) {
			log_printf(1, "reading %%s (0x%%x b pad 0x%%x b)", name, size, (size + 15) & ~15);
		} else
			log_printf(1, "reading %%s (0x%%x bytes)", name, size);
	}
"""
PADS = {
    'orig': (A, 'size != e->size', ''),
    'ternary': ('	e->size = pad && (size & 15) ? (size + 15) & ~15 : size;\n', 'size != e->size', ''),
    'ptern': ('	e->size = size;\n	padded = pad && (size & 15) ? (size + 15) & ~15 : size;\n	e->size = padded;\n', 'size != padded', '	uint32_t padded;\n'),
    'ptern2': ('	e->size = size;\n	padded = pad && (size & 15) ? (size + 15) & ~15 : size;\n	if (padded != size)\n		e->size = padded;\n', 'size != padded', '	uint32_t padded;\n'),
    'p3': ('	e->size = size;\n	padded = size;\n	if (pad && (size & 15)) {\n		padded = (size + 15) & ~15;\n		e->size = padded;\n	}\n', 'size != padded', '	uint32_t padded;\n'),
    'p4': ('	e->size = size;\n	if (pad && (size & 15))\n		e->size = (size + 15) & ~15;\n	padded = e->size;\n', 'size != padded', '	uint32_t padded;\n'),
    'flag': ('	e->size = size;\n	padded = 0;\n	if (pad && (size & 15)) {\n		e->size = (size + 15) & ~15;\n		padded = 1;\n	}\n', 'padded', '	uint32_t padded;\n'),
    'nest': ('	e->size = size;\n	if (pad) {\n		if (size & 15)\n			e->size = (size + 15) & ~15;\n	}\n', 'size != e->size', ''),
    'rem': ('	e->size = size;\n	if (pad && (size % 16))\n		e->size = (size + 15) & ~15;\n', 'size != e->size', ''),
    'neq': ('	e->size = size;\n	if (pad && (size & 15) != 0)\n		e->size = (size + 15) & ~15;\n', 'e->size != size', ''),
    'q1': ('	e->size = size;\n	e->size = pad && (size & 15) ? (size + 15) & ~15 : e->size;\n', 'size != e->size', ''),
    'q2': ('	e->size = size;\n	if (pad)\n		e->size = (size & 15) ? (size + 15) & ~15 : size;\n', 'size != e->size', ''),
    'q3': ('	e->size = size;\n	if (pad)\n		e->size = (size + 15) & ~15;\n', 'size != e->size', ''),
}
HEAD = 'int loadFileCrc(const char *name, struct fileent *e, int verbose, int pad, uint32_t crc)\n{\n	FILE *f;\n	size_t size;\n	uint32_t c;\n'


def CASES(base):
    out = []
    for k, (p, test, d) in PADS.items():
        t = base.replace(A, p).replace(LOGOLD, L % test).replace(HEAD, HEAD + d)
        out.append((k, t))
    return out
