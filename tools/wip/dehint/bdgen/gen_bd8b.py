"""patchBlsBlmod without its no-early-inlining: spill order, second try"""
REMOVE = ['nei_blmod']
FOCUS = ['_patchBlsBlmod']
Bp = '''				if (!n) {
					if (addr + len > xb.files[cbb].size) {
						xb.files[cbb].size = (addr + len + 15) & ~15;
						setBeU32(xb.files[cbb].size, xb.files[cbb].data + 12);
					}
					for (i = 0; i < len; i++)
						xb.files[cbb].data[addr + i] = d[off + i];
				} else {
					if (addr + len > xb.files[cd].size) {
						xb.files[cd].size = (addr + len + 15) & ~15;
						setBeU32(xb.files[cd].size, xb.files[cd].data + 12);
					}
					for (i = 0; i < len; i++)
						xb.files[cd].data[addr + i] = d[off + i];
				}
'''
A = [
    ('', []),
    ('pol', [(Bp, '''				if (n) {
					if (addr + len > xb.files[cd].size) {
						xb.files[cd].size = (addr + len + 15) & ~15;
						setBeU32(xb.files[cd].size, xb.files[cd].data + 12);
					}
					for (i = 0; i < len; i++)
						xb.files[cd].data[addr + i] = d[off + i];
				} else {
					if (addr + len > xb.files[cbb].size) {
						xb.files[cbb].size = (addr + len + 15) & ~15;
						setBeU32(xb.files[cbb].size, xb.files[cbb].data + 12);
					}
					for (i = 0; i < len; i++)
						xb.files[cbb].data[addr + i] = d[off + i];
				}
''')]),
    ('one', [(Bp, '''				{
					int f = n ? cd : cbb;

					if (addr + len > xb.files[f].size) {
						xb.files[f].size = (addr + len + 15) & ~15;
						setBeU32(xb.files[f].size, xb.files[f].data + 12);
					}
					for (i = 0; i < len; i++)
						xb.files[f].data[addr + i] = d[off + i];
				}
''')]),
]
Cc = '''		if (!xb.cbb)
			cbb = cd;
'''
B = [
    ('', []),
    ('tern', [(Cc, '''		cbb = xb.cbb ? cbb : cd;
''')]),
    ('else', [(Cc, '''		if (xb.cbb)
			;
		else
			cbb = cd;
''')]),
]
D0 = 'int cd = findFile(7), cbb = findFile(6), pt = findFile(23);'
C = [
    ('', []),
    ('o1', [(D0, 'int cbb = findFile(6), cd = findFile(7), pt = findFile(23);')]),
    ('o2', [(D0, 'int cd, cbb, pt = findFile(23);\n\n	cd = findFile(7);\n	cbb = findFile(6);\n	{')]),
]
AXES = [A, B]
