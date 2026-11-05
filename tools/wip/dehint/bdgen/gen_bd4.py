"""isUpdateBl: its expect only sets the layout of addUpdateBls' first test"""
Q = 'return __builtin_expect(type == 23 || type == 15, 0) || type == 16 || type == 9 || type == 10 || type == 24 || type == 25;'
C = '''		if (!isUpdateBl(type))
			continue;
		if (e->offset != 0xffffffff)
			off = e->offset;
		if (!strnicmp(e->name, "none", 4) && !e->crc)
			continue;
		if (type == 9)
			off = imgCfOffset();
		else if (type == 23) {
			off = imgCfOffset() + imgCfSize();
			if (xb.glitch2mfg)
				off += 0x60;
			else
				off += 0x10;
		}
		if (type == 25 && e->offset < imgSize()) {'''
FOCUS = ['_addUpdateBls', '_isUpdateBl']
L = 'type == 15 || type == 16 || type == 9 || type == 10 || type == 24 || type == 25'
A = [
    ('or', [(Q, 'return type == 23 || type == 15 || type == 16 || type == 9 || type == 10 || type == 24 || type == 25;')]),
    ('if2', [(Q, 'if (type == 23 || type == 15)\n\t\treturn 1;\n\tif (type == 16 || type == 9 || type == 10 || type == 24 || type == 25)\n\t\treturn 1;\n\treturn 0;')]),
    ('flag', [(Q, 'int r = 0;\n\n\tif (type == 23 || type == 15)\n\t\tr = 1;\n\telse if (type == 16 || type == 9 || type == 10 || type == 24 || type == 25)\n\t\tr = 1;\n\treturn r;')]),
    ('nest', [(Q, 'if (type == 23 || type == 15)\n\t\treturn 1;\n\telse if (type == 16 || type == 9 || type == 10 || type == 24 || type == 25)\n\t\treturn 1;\n\telse\n\t\treturn 0;')]),
    ('sw', [(Q, 'switch (type) {\n\tcase 23: case 15:\n\t\treturn 1;\n\tdefault:\n\t\treturn type == 16 || type == 9 || type == 10 || type == 24 || type == 25;\n\t}')]),
]
B = [
    ('cont', []),
    ('nz', [('if (!isUpdateBl(type))', 'if (isUpdateBl(type) == 0)')]),
    ('else', [('''		if (!isUpdateBl(type))
			continue;
		if (e->offset != 0xffffffff)''', '''		if (!isUpdateBl(type)) {
			continue;
		} else if (e->offset != 0xffffffff)''')]),
    ('gt', [('if (!isUpdateBl(type))', 'if (isUpdateBl(type) <= 0)')]),
]
AXES = [A, B]
