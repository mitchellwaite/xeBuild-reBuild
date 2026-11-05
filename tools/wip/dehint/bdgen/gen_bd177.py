"""exp_verbose, pin_e: the log tests per pad arm once more (gen_bd132 was 68 and up), now reading what's left, with align16 in, and forms where the pad arm's log tests size first."""
import itertools

PADL = 'log_printf(1, "reading %s (0x%x b pad 0x%x b)", name, size, align16(size));\n'
BYTL = 'log_printf(1, "reading %s (0x%x bytes)", name, size);\n'
START = '	e->size = size;\n	if (pad && (size & 15))\n'
END = '	e->data = calloc(e->size + 0x10000, 1);\n'
BODY = {
    'two': '	e->size = size;\n	if (pad && (size & 15)) {\n		e->size = align16(size);\n		if (verbose) {\n			if (size != e->size)\n				' + PADL + '			else\n				' + BYTL + '		}\n	} else if (verbose)\n		' + BYTL,
    'twoeq': '	e->size = size;\n	if (pad && (size & 15)) {\n		e->size = align16(size);\n		if (verbose) {\n			if (size == e->size)\n				' + BYTL + '			else\n				' + PADL + '		}\n	} else if (verbose)\n		' + BYTL,
    'first': '	e->size = size;\n	if (!pad || !(size & 15)) {\n		if (verbose)\n			' + BYTL + '	} else {\n		e->size = align16(size);\n		if (verbose) {\n			if (size != e->size)\n				' + PADL + '			else\n				' + BYTL + '		}\n	}\n',
    'nested': '	e->size = size;\n	if (pad) {\n		if (size & 15) {\n			e->size = align16(size);\n			if (verbose) {\n				if (size != e->size)\n					' + PADL + '				else\n					' + BYTL + '			}\n		} else if (verbose)\n			' + BYTL + '	} else if (verbose)\n		' + BYTL,
    'nest2': '	e->size = size;\n	if (pad && (size & 15))\n		e->size = align16(size);\n	if (verbose) {\n		if (size == e->size)\n			' + BYTL + '		else\n			' + PADL + '	}\n',
    'r': '	e->size = size;\n	if (pad && (size & 15))\n		e->size = align16(size);\n	if (!verbose)\n		;\n	else if (size != e->size)\n		' + PADL + '	else\n		' + BYTL,
}


def CASES(base):
    i = base.index(START)
    j = base.index(END, i)
    return [(k, base[:i] + v + base[j:]) for k, v in BODY.items()]


FOCUS = ['_loadFileCrc']
