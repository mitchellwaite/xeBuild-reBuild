"""patchBlsBlmod without its no-early-inlining: 2 lines, spill order"""
REMOVE = ['nei_blmod']
FOCUS = ['_patchBlsBlmod']
H = '''	int cd = findFile(7), cbb = findFile(6), pt = findFile(23);
	struct fileent *p = &xb.files[pt];
	uint8_t *d = p->data;
	uint32_t off, addr, len, i, max, end, t;
	int n = 0;
'''
A = [
    ('', []),
    ('sepdecl', [(H, '''	int cd = findFile(7);
	int cbb = findFile(6);
	int pt = findFile(23);
	struct fileent *p = &xb.files[pt];
	uint8_t *d = p->data;
	uint32_t off, addr, len, i, max, end, t;
	int n = 0;
''')]),
    ('assign', [(H, '''	int cd, cbb, pt;
	struct fileent *p;
	uint8_t *d;
	uint32_t off, addr, len, i, max, end, t;
	int n = 0;

	cd = findFile(7);
	cbb = findFile(6);
	pt = findFile(23);
	p = &xb.files[pt];
	d = p->data;
''')]),
    ('addp', [(H, '''	int cd = findFile(7), cbb = findFile(6);
	struct fileent *p = xb.files + findFile(23);
	uint8_t *d = p->data;
	uint32_t off, addr, len, i, max, end, t;
	int n = 0;
''')]),
    ('addp2', [(H, '''	int cd = findFile(7), cbb = findFile(6);
	struct fileent *p = &xb.files[findFile(23)];
	uint8_t *d = p->data;
	uint32_t off, addr, len, i, max, end, t;
	int n = 0;
''')]),
    ('n0', [(H, '''	int n = 0;
	int cd = findFile(7), cbb = findFile(6), pt = findFile(23);
	struct fileent *p = &xb.files[pt];
	uint8_t *d = p->data;
	uint32_t off, addr, len, i, max, end, t;
''')]),
    ('uint', [(H, '''	uint32_t cd = findFile(7), cbb = findFile(6), pt = findFile(23);
	struct fileent *p = &xb.files[pt];
	uint8_t *d = p->data;
	uint32_t off, addr, len, i, max, end, t;
	int n = 0;
''')]),
]
Bp = '''				if (!n) {
					if (addr + len > xb.files[cbb].size) {
						xb.files[cbb].size = (addr + len + 15) & ~15;
						setBeU32(xb.files[cbb].size, xb.files[cbb].data + 12);
					}
					for (i = 0; i < len; i++)
						xb.files[cbb].data[addr + i] = d[off + i];
				} else {'''
B = [
    ('', []),
    ('sw', [(Bp, '''				if (n == 0) {
					if (addr + len > xb.files[cbb].size) {
						xb.files[cbb].size = (addr + len + 15) & ~15;
						setBeU32(xb.files[cbb].size, xb.files[cbb].data + 12);
					}
					for (i = 0; i < len; i++)
						xb.files[cbb].data[addr + i] = d[off + i];
				} else {''')]),
]
C = [
    ('', []),
    ('sc', [('uint32_t off, addr, len, i, max, end, t;\n	int n = 0;', 'uint32_t off, i, max, end;\n	int n = 0;'),
            ('''			addr = getBeU32(d + off);
			t = off + 4;''', '''			uint32_t addr = getBeU32(d + off), t = off + 4;
'''),
            ('				len = getBeU32(d + t) * 4;', '				uint32_t len = getBeU32(d + t) * 4;\n')]),
]
AXES = [A, B, C]
