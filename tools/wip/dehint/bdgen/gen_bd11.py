"""extractSmcConfig without noinline: only the bound tests' operand order is left"""
REMOVE = ['noinline']
FOCUS = ['_extractSmcConfig']
Q1 = '''	for (i = 0; __builtin_expect(i + 0x200 <= size, 1); i += 0x200) {
		__asm__("" : : "S"(i + 0x200), "D"(buf));
		if ((found = smcConfigOk(buf + i)) == 1)
			break;
	}
'''
Q2 = '''		for (i = 0; __builtin_expect(i + 0x210 <= size, 1); i += 0x210)
			if ((found = smcConfigOk(buf + i)) == 1)
				break;
'''
AS = '	(void)&size;\n'
A = [
    ('', []),
    ('noaddr', [(AS, '')]),
    ('addr2', [(AS, ''), ('	found = 0;\n	for (i = 0; __builtin_expect(i + 0x200', '	found = 0;\n	(void)&size;\n	for (i = 0; __builtin_expect(i + 0x200')]),
]
B = [
    ('', []),
    ('ge', [(Q1, Q1.replace('i + 0x200 <= size', 'size >= i + 0x200')), (Q2, Q2.replace('i + 0x210 <= size', 'size >= i + 0x210'))]),
]
C = [
    ('', []),
    ('ulen', [('int extractSmcConfig(struct fileent *e, uint8_t *buf, uint32_t size)\n{\n	uint32_t i, j;', 'int extractSmcConfig(struct fileent *e, uint8_t *buf, uint32_t size)\n{\n	uint32_t j, i;')]),
    ('copy', [('	uint32_t i, j;\n	int found;\n', '	uint32_t i, j, len = size;\n	int found;\n'), ('i + 0x200 <= size', 'i + 0x200 <= len'), ('i + 0x210 <= size', 'i + 0x210 <= len')]),
]
AXES = [A, C]
