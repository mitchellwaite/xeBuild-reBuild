"""checkBl without pin_m: m and the test's temporary swap eax and edx.  Types of m through blMagic, its uses, helper forms."""
REMOVE = ['pin_m']
FOCUS = ['_checkBl']
BM = 'static void blMagic(const uint8_t *bl, int *m)\n{\n	*m = bl[0];\n}\n\n'
DECL = '	uint32_t blsize, c;\n	int m;\n'
CALL = '	blMagic(bl, &m);\n'
TEST = '	if ((m & 0x43) != 0x43)\n		goto magic;\n'
LOG = 'failed!\\n", bl[0], bl[1], type);'
T = [('int', []),
     ('u8', [(BM, BM.replace('int *m', 'uint8_t *m')), (DECL, '	uint32_t blsize, c;\n	uint8_t m;\n')]),
     ('u32', [(BM, BM.replace('int *m', 'uint32_t *m')), (DECL, '	uint32_t blsize, c, m;\n')]),
     ('ch', [(BM, BM.replace('int *m', 'char *m')), (DECL, '	uint32_t blsize, c;\n	char m;\n')]),
     ('u16', [(BM, BM.replace('int *m', 'uint16_t *m')), (DECL, '	uint32_t blsize, c;\n	uint16_t m;\n')]),
     ]
U = [('', []),
     ('logm', [(LOG, 'failed!\\n", m, bl[1], type);')]),
     ]
F = [('', []),
     ('tilde', [(TEST, '	if (~m & 0x43)\n		goto magic;\n')]),
     ('and', [(TEST, '	m &= 0x43;\n	if (m != 0x43)\n		goto magic;\n')]),
     ('mk', [(TEST, '	{\n		int mask = m & 0x43;\n\n		if (mask != 0x43)\n			goto magic;\n	}\n')]),
     ('two', [(TEST, '	if (!(m & 1) || !(m & 2) || !(m & 0x40))\n		goto magic;\n')]),
     ]
AXES = [T, U, F]
