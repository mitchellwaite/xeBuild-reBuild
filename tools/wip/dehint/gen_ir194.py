"""getImageSmc: types of addr, size, t, loadSmc's params, the sane test, with the attribute's options and the pin on and off (attempt 13)."""
FOCUS = ['_getImageSmc']
ATTR = '__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc(void)'
PIN = '''	} else {
		__asm__("" : "+D"(addr));
	}
'''
A = [
 ('a3', []),
 ('a0', [(ATTR, 'void getImageSmc(void)')]),
 ('i2', [(ATTR, '__attribute__((optimize("no-if-conversion2"))) void getImageSmc(void)')]),
 ('tm', [(ATTR, '__attribute__((optimize("no-tree-tail-merge"))) void getImageSmc(void)')]),
]
P = [('p', []), ('np', [(PIN, '	}\n')])]
ADDR = [
 ('ai', []),
 ('au', [('	int addr = SWAP32(h->smcBootAddr);\n', '	uint32_t addr = SWAP32(h->smcBootAddr);\n')]),
]
SIZE = [
 ('si', []),
 ('su', [('	int size = SWAP32(h->smcBootSize);\n', '	uint32_t size = SWAP32(h->smcBootSize);\n')]),
]
LP = [
 ('ii', []),
 ('ui', [('static void loadSmc(int addr, int size)', 'static void loadSmc(uint32_t addr, int size)')]),
 ('iu', [('static void loadSmc(int addr, int size)', 'static void loadSmc(int addr, uint32_t size)')]),
 ('uu', [('static void loadSmc(int addr, int size)', 'static void loadSmc(uint32_t addr, uint32_t size)')]),
 ('pp', [('static void loadSmc(int addr, int size)', 'static void loadSmc(uint8_t *src, int addr, int size)'),
         ('memcpy(xb.smc.data, xb.dump + addr, size);', 'memcpy(xb.smc.data, src, size);'),
         ('		loadSmc(addr, size);\n', '		loadSmc(xb.dump + addr, addr, size);\n')]),
]
T = [
 ('t', []),
 ('ti', [('	unsigned t;\n', '	int t;\n')]),
 ('ts', [('	t = addr;\n	if (t != 0x1000) {\n		if (t != 0x800)\n', '	if ((uint32_t)addr != 0x1000) {\n		if ((uint32_t)addr != 0x800)\n')]),
]
L = [
 ('l', []),
 ('lc', [('	if (ok && addr < 528 * xb.dumpPages)', '	if (ok && (uint32_t)addr < 528 * xb.dumpPages)')]),
 ('lu', [('	if (ok && addr < 528 * xb.dumpPages)', '	if (ok && addr / 528 < xb.dumpPages)')]),
]
AXES = [A, P, ADDR, SIZE, LP, T, L]
