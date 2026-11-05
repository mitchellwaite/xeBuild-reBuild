"""loadFileCrc: the log tests written per pad arm, so the bytes log comes from two places with its own call prediction (29% of 75%, over bb-reorder's 2000).  With the pin or not."""
import itertools

PADL = 'log_printf(1, "reading %s (0x%x b pad 0x%x b)", name, size, (size + 15) & ~15);\n'
BYTL = 'log_printf(1, "reading %s (0x%x bytes)", name, size);\n'
OLD = '''	e->size = size;
	if (pad && (size & 15))
		e->size = (size + 15) & ~15;
	/* hints: the "bytes" log must be hot enough for bb-reorder's second round
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
PIN = '\t__asm__("" : : "S"(e));\n'


def forms(pin):
    p = '\t\t\t\t' + PIN if pin else ''
    yield 'two', '\te->size = size;\n\tif (pad && (size & 15)) {\n\t\te->size = (size + 15) & ~15;\n\t\tif (verbose) {\n\t\t\tif (size != e->size) {\n\t\t\t\t' + PADL + p + '\t\t\t} else\n\t\t\t\t' + BYTL + '\t\t}\n\t} else if (verbose)\n\t\t' + BYTL
    p = '\t\t\t' + PIN if pin else ''
    yield 'one', '\te->size = size;\n\tif (pad && (size & 15)) {\n\t\te->size = (size + 15) & ~15;\n\t\tif (verbose) {\n\t\t\t' + PADL + p + '\t\t}\n\t} else if (verbose)\n\t\t' + BYTL
    yield 'gotobyt', '\te->size = size;\n\tif (pad && (size & 15)) {\n\t\te->size = (size + 15) & ~15;\n\t\tif (verbose) {\n\t\t\tif (size == e->size)\n\t\t\t\tgoto bytes;\n\t\t\t' + PADL + p + '\t\t}\n\t} else if (verbose) {\nbytes:\n\t\t' + BYTL + '\t}\n'
    yield 'nsz', '\tif (pad && (size & 15)) {\n\t\te->size = (size + 15) & ~15;\n\t\tif (verbose) {\n\t\t\tif (size != e->size) {\n\t\t\t\t' + PADL + '\t\t\t} else\n\t\t\t\t' + BYTL + '\t\t}\n\t} else {\n\t\te->size = size;\n\t\tif (verbose)\n\t\t\t' + BYTL + '\t}\n'


def CASES(base):
    out = []
    for pin in (0, 1):
        for n, s in forms(pin):
            out.append(('%s pin%d' % (n, pin), base.replace(OLD, s)))
    return out
