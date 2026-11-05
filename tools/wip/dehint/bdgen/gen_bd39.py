# extractSmcConfig and loadFileCrc: declaration types with hints off, read for the focus functions (use BDFOCUS).
import os
which = os.environ.get('BDFOCUS', 'x')
if which == 'x':
    REMOVE = ['pin_i', 'exp_200', 'exp_210', 'pin_src', 'exp_400']
    FOCUS = ['_extractSmcConfig']
    D = '	uint32_t i, j;\n	int found;\n'
    SIG = 'int extractSmcConfig(struct fileent *e, uint8_t *buf, int size)'
    AXES = [
        [('', []), ('ii', [(D, '	int i, j;\n	int found;\n')]), ('ij', [(D, '	uint32_t i;\n	int j;\n	int found;\n')]),
         ('si', [(D, '	size_t i, j;\n	int found;\n')])],
        [('', []), ('fu', [('	int found;\n', '	uint32_t found;\n')])],
        [('', []), ('bv', [(SIG, SIG.replace('uint8_t *buf', 'void *buf'))]), ('bc', [(SIG, SIG.replace('uint8_t *buf', 'const uint8_t *buf'))])],
    ]
else:
    REMOVE = ['exp_verbose', 'pin_e']
    FOCUS = ['_loadFileCrc']
    SIG = 'int loadFileCrc(const char *name, struct fileent *e, int verbose, int pad, uint32_t crc)'
    SIGP = SIG + ';\n'
    B = [(SIG + '\n{', None)]
    D = '	FILE *f;\n	size_t size;\n	uint32_t c;\n'
    AXES = [
        [('', []), ('su', [(D, '	FILE *f;\n	uint32_t size;\n	uint32_t c;\n')]), ('si', [(D, '	FILE *f;\n	int size;\n	uint32_t c;\n')])],
        [('', []), ('nest', [('''	if (verbose) {
		if (size != e->size) {
			log_printf(1, "reading %s (0x%x b pad 0x%x b)", name, size, (size + 15) & ~15);
		} else
			log_printf(1, "reading %s (0x%x bytes)", name, size);
	}
''', '''	if (verbose) {
		if (size == e->size)
			log_printf(1, "reading %s (0x%x bytes)", name, size);
		else
			log_printf(1, "reading %s (0x%x b pad 0x%x b)", name, size, (size + 15) & ~15);
	}
''')])],
        [('', []), ('gt', [('	if (verbose) {\n		if (size', '	if (verbose > 0) {\n		if (size')]),
         ('ne', [('	if (verbose) {\n		if (size', '	if (verbose == 1) {\n		if (size')])],
    ]
