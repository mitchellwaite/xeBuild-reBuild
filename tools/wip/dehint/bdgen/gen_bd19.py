"""loadFileCrc: the verbose expect and the e pin"""
FOCUS = ['_loadFileCrc', '_loadBaseFile', '_loadBaseFileMeta', '_loadCommonFile', '_loadInputFile', '_loadBinFile', '_loadLocalFile']
Q = '''	if (__builtin_expect(verbose, 1)) {
		if (size != e->size) {
			log_printf(1, "reading %s (0x%x b pad 0x%x b)", name, size, (size + 15) & ~15);
			__asm__("" : : "S"(e));
		} else
			log_printf(1, "reading %s (0x%x bytes)", name, size);
	}
'''
P = '			__asm__("" : : "S"(e));\n'
L1 = 'log_printf(1, "reading %s (0x%x b pad 0x%x b)", name, size, (size + 15) & ~15);'
L2 = 'log_printf(1, "reading %s (0x%x bytes)", name, size);'
S = []
for pin in (1, 0):
    p = P if pin else ''
    t = '' if pin else '-p'
    S += [
        ('gt' + t, [(Q, '	if (verbose > 0) {\n		if (size != e->size) {\n			' + L1 + '\n' + p + '		} else\n			' + L2 + '\n	}\n')]),
        ('eq1' + t, [(Q, '	if (verbose == 1) {\n		if (size != e->size) {\n			' + L1 + '\n' + p + '		} else\n			' + L2 + '\n	}\n')]),
        ('ne0' + t, [(Q, '	if (verbose != 0) {\n		if (size != e->size) {\n			' + L1 + '\n' + p + '		} else\n			' + L2 + '\n	}\n')]),
        ('ne' + t, [(Q, '	if (verbose) {\n		if (size == e->size)\n			' + L2 + '\n		else {\n			' + L1 + '\n' + p + '		}\n	}\n')]),
        ('and' + t, [(Q, '	if (verbose && size != e->size) {\n		' + L1 + '\n' + p + '	} else if (verbose)\n		' + L2 + '\n')]),
        ('ret' + t, [(Q, '	if (!verbose)\n		goto quiet;\n	if (size != e->size) {\n		' + L1 + '\n' + p + '	} else\n		' + L2 + '\nquiet:\n')]),
    ]
AXES = [S]
