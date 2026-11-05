"""checkBl after crcSame: the size error's hot label and blMagic: size in [1000, 2000).  Helpers for the size error, with and without blMagic."""
SZLOG = '	log_printf(0, "\\n\\n***** ERROR: BL size (0x%x) is bigger than the file (0x%x) read in!\\n", blsize, size);\n'
SZ = 'toobig: __attribute__((hot));\n' + SZLOG + '	return -3;\n'
HEAD = '__attribute__((optimize("no-early-inlining")))\nint checkBl('
SI = 'static int blTooBig(uint32_t blsize, uint32_t size)\n{\n' + SZLOG + '	return -3;\n}\n\n'
SV = 'static void blTooBig(uint32_t blsize, uint32_t size)\n{\n' + SZLOG + '}\n\n'
BM = 'static void blMagic(const uint8_t *bl, int *m)\n{\n	*m = bl[0];\n}\n\n'
S = [
    ('hot', []),
    ('plain', [(SZ, 'toobig:\n' + SZLOG + '	return -3;\n')]),
    ('help', [(SZ, 'toobig:\n	return blTooBig(blsize, size);\n'), (HEAD, SI + HEAD)]),
    ('void', [(SZ, 'toobig:\n	blTooBig(blsize, size);\n	return -3;\n'), (HEAD, SV + HEAD)]),
    ('rflag', [(SZ, 'toobig:\n	m = blTooBig(blsize, size);\n	return m;\n'), (HEAD, SI + HEAD)]),
]
M = [
    ('bm', []),
    ('nom', [('	blMagic(bl, &m);\n', '	m = bl[0];\n'), (BM, '')]),
]
AXES = [S, M]
FOCUS = ['_checkBl']
