"""fsGetFile without the "S"(v) pin."""
FOCUS = ['_fsGetFile']
BASE = 'tools/wip/dehint/drafts/image_read_attempt1.c'
H = '''	uint32_t block, len, t, off, left, done;
	uint8_t *p;
	int v = fsValid;

	/* code-free hint: fsValid (reused for return 1) in esi, name in edi */
	__asm__("" : : "S"(v));
	if (v != 1)
		return 0;
	if (!fsFind(name, &block, &len, &t, 1))
		return 0;
'''
R = '''	*time = t;
	return 1;
'''
D = {
 'a': ('uint32_t block, len, t, off, left, done;\n	uint8_t *p;\n	int v = fsValid;\n\n'),
 'b': ('int v = fsValid;\n	uint32_t block, len, t, off, left, done;\n	uint8_t *p;\n\n'),
 'c': ('uint32_t block, len, t, off, left, done;\n	uint8_t *p;\n	uint32_t v = fsValid;\n\n'),
}
T = {
 'if2': 'if (v != 1)\n		return 0;\n	if (!fsFind(name, &block, &len, &t, 1))\n		return 0;\n',
 'nest': 'if (v == 1) {\n	if (!fsFind(name, &block, &len, &t, 1))\n		return 0;\n	} else\n		return 0;\n',
 'and': 'if (v != 1 || !fsFind(name, &block, &len, &t, 1))\n		return 0;\n',
 'zero': 'if (v != 1)\n		return 0;\n	v = fsFind(name, &block, &len, &t, 1);\n	if (!v)\n		return 0;\n',
 'zero2': 'if (v != 1)\n		return 0;\n	if (!fsFind(name, &block, &len, &t, 1))\n		return 0;\n',
}
RR = {'r1': R, 'rv': '	*time = t;\n	return v;\n'}
AXES = [[(f'{dk}.{tk}.{rk}', [(H, '	' + d + '	' + t), (R, r)])
         for dk, d in D.items() for tk, t in T.items() for rk, r in RR.items()]]
