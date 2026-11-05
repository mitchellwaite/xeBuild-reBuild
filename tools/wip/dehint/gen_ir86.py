"""getImageSmc with its optimize attribute gone (6 loose lines): where the remaining hints go so that ce1 doesn't hoist.  Moving a hint isn't a gain by itself; losing the attribute is."""
FOCUS = ['_getImageSmc']
BASE = 'src/image_read.c'
ATTR = '__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc'
SHOT = '''		shot: __attribute__((hot));
		if (addr == 0x800) {
			size = 0x3800;
'''
S8 = '''			size = 0x3800;
'''
PINE = '''	} else
		__asm__("" : "+D"(addr));
'''
J = '	if (__builtin_expect(addr < 528 * xb.dumpPages, 0)) {\n'
T = '	if (size != 0x3000 && size != 0x3800) {\n'
A0 = [('', [(ATTR, 'void getImageSmc')])]
AS = [
    ('sk', []),
    ('s8', [(SHOT, '		if (addr == 0x800) {\n			shot: __attribute__((hot));\n			size = 0x3800;\n')]),
    ('s0', [(SHOT, '		if (addr == 0x800) {\n			size = 0x3800;\n')]),
    ('se', [(SHOT, '		if (addr == 0x800) {\n			size = 0x3800;\n'), (PINE, '	} else {\n		shot: __attribute__((hot));\n		__asm__("" : "+D"(addr));\n	}\n')]),
    ('s00', [(SHOT, '		if (addr == 0x800) {\n			size = 0x3800;\n'), ('			size = 0x3000;\n', '			shot: __attribute__((hot));\n			size = 0x3000;\n')]),
    ('st', [(SHOT, '		if (addr == 0x800) {\n			size = 0x3800;\n'), (T, '	if (__builtin_expect(size != 0x3000 && size != 0x3800, 1)) {\n')]),
    ('sn', [(SHOT, '		if (addr == 0x800) {\n			size = 0x3800;\n'), (T, '	if (size != 0x3000) {\n	if (size != 0x3800) {\n'), ('''	} else
		__asm__("" : "+D"(addr));
	if (__builtin''', '''	}
	} else
		__asm__("" : "+D"(addr));
	if (__builtin''')]),
]
AP = [
    ('pk', []),
    ('pi', [(PINE, '	} else\n		__asm__("" : : "D"(addr));\n')]),
    ('pj', [(PINE, '	}\n'), (J, '	__asm__("" : "+D"(addr));\n' + J)]),
    ('pt', [(PINE, '	}\n'), (T, '	__asm__("" : "+D"(addr));\n' + T)]),
    ('p2', [(PINE, '	}\n'), ('bback:\n', 'bback:\n	__asm__("" : "+D"(addr));\n')]),
]
AU = [
    ('uk', []),
    ('u8', [('''			if (!h)
				__builtin_unreachable();
''', ''), (S8, S8 + '			if (!h)\n				__builtin_unreachable();\n')]),
]
AXES = [A0, AS, AP, AU]
