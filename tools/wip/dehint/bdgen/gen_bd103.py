"""loadConsoleBlFiles without the cold label: forms of the empty-list case; and of defaultBl60's malloc failure, which is the block that must come before the return."""
import itertools
HEAD = '''	/* the cold label gives the shrink-wrapped return 0 frequency 0, so
	   bb-reorder lays it out last */
	if ((uint32_t)xb.nFiles <= 1)
		goto none;
	for (i = 1; i < (uint32_t)xb.nFiles; i++) {
		e = &xb.files[i];
		r = 0;
		if (strnicmp(e->name, "none", 4) || e->crc) {
			int type = e->type;
'''
TAIL = '''none: __attribute__((cold));
	return 0;
'''
LOOP = HEAD[HEAD.index('	for (i'):]
HF = {
    'plain': (LOOP, '	return 0;\n'),
    'ret': ('	if ((uint32_t)xb.nFiles <= 1)\n		return 0;\n' + LOOP, '	return 0;\n'),
    'ret2': ('	if ((uint32_t)xb.nFiles < 2)\n		return 0;\n' + LOOP, '	return 0;\n'),
    'goto': ('	if ((uint32_t)xb.nFiles <= 1)\n		goto none;\n' + LOOP, 'none:\n	return 0;\n'),
    'dowhile': ('	if ((uint32_t)xb.nFiles <= 1)\n		return 0;\n	i = 1;\n	do {\n' + LOOP.split('\n', 1)[1], None),
    'ge': (LOOP.replace('i < (uint32_t)xb.nFiles', '(int)i < xb.nFiles'), '	return 0;\n'),
    'ne': (LOOP.replace('i < (uint32_t)xb.nFiles', 'i != (uint32_t)xb.nFiles'), '	return 0;\n'),
}
D60 = '''	e->data = malloc(0x60);
	if (!e->data)
		return 1;
	e->size = 0x60;
	memcpy(e->data, defBl60, 0x60);
	return 0;
'''
DF = {
    'keep': D60,
    'p': '	uint8_t *p = malloc(0x60);\n\n	e->data = p;\n	if (!p)\n		return 1;\n	e->size = 0x60;\n	memcpy(p, defBl60, 0x60);\n	return 0;\n',
    'nest': '	e->data = malloc(0x60);\n	if (e->data) {\n		e->size = 0x60;\n		memcpy(e->data, defBl60, 0x60);\n		return 0;\n	}\n	return 1;\n',
    'r': '	int r = 1;\n\n	e->data = malloc(0x60);\n	if (e->data) {\n		e->size = 0x60;\n		memcpy(e->data, defBl60, 0x60);\n		r = 0;\n	}\n	return r;\n',
}


def CASES(base):
    out = []
    for (hn, (h, tl)), (dn, d) in itertools.product(HF.items(), DF.items()):
        t = base.replace(D60, d)
        if hn == 'dowhile':
            t = t.replace(HEAD, h)
            a = t.index('int loadConsoleBlFiles(void)')
            x = t.index('			return -1;\n		}\n	}\n	return 0;\nnone: __attribute__((cold));\n	return 0;\n', a)
            t = t[:x] + '			return -1;\n		}\n	} while (++i < (uint32_t)xb.nFiles);\n	return 0;\n' + t[x + len('			return -1;\n		}\n	}\n	return 0;\nnone: __attribute__((cold));\n	return 0;\n'):]
        else:
            t = t.replace(HEAD, h).replace('	return 0;\n' + TAIL, tl)
        out.append(('%s %s' % (hn, dn), t))
    return out
