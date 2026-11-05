"""loadFileCrc: the two reading logs with their own verbose tests, in orders that raise the bytes log's frequency without an expect."""
import itertools

PADL = 'log_printf(1, "reading %s (0x%x b pad 0x%x b)", name, size, (size + 15) & ~15);\n'
BYTL = 'log_printf(1, "reading %s (0x%x bytes)", name, size);\n'
OLD = '''	/* hints: the "bytes" log must be hot enough for bb-reorder's second round
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
F = {
    'and': 'if (verbose && size != e->size)\n' + PADL + 'else if (verbose)\n' + BYTL,
    'and2': 'if (size != e->size && verbose)\n' + PADL + 'else if (verbose)\n' + BYTL,
    'eq': 'if (verbose && size == e->size)\n' + BYTL + 'else if (verbose)\n' + PADL,
    'eqn': 'if (verbose) {\nif (size == e->size)\n' + BYTL + 'else\n' + PADL + '}\n',
    'sep': 'if (verbose && size != e->size)\n' + PADL + 'if (verbose && size == e->size)\n' + BYTL,
    'sep2': 'if (verbose && size == e->size)\n' + BYTL + 'if (verbose && size != e->size)\n' + PADL,
    'sz': 'if (size != e->size) {\nif (verbose)\n' + PADL + '} else if (verbose)\n' + BYTL,
    'ret': 'if (!verbose)\ngoto noverb;\nif (size != e->size)\n' + PADL + 'else\n' + BYTL + 'noverb:\n',
}


def CASES(base):
    return [(k, base.replace(OLD, v)) for k, v in F.items()]
