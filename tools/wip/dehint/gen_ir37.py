"""fsGetFile without the "S"(v) pin.  IRA (dump): top region pops off (r106) before the return value (r149), off takes esi,
ret edi; name then gets esi.  Reference: ret esi, off edi.  a0 turns colorable before a19, so conflicts decide: shapes of
the copy part after the lookup, which earlier attempts didn't sweep."""
FOCUS = ['_fsGetFile']
PIN = '''	/* code-free hint: fsValid (reused for return 1) in esi, name in edi */
	__asm__("" : : "S"(v));
'''
D = '''	uint32_t block, len, t, off, left, done;
	uint8_t *p;
	int v = fsValid;
'''
B = '''	off = fsOffset + (block << 14);
	p = calloc(len, 1);
	left = len;
	done = 0;
	while (left > 0x4000) {
		memcpy(p + done, xb.dump + off, 0x4000);
		left -= 0x4000;
		done += 0x4000;
		block = SWAP16(fs->map[block]) & 0x1fff;
		off = fsOffset + (block << 14);
	}
	if (left)
		memcpy(p + done, xb.dump + off, left);
	*buf = p;
	*size = len;
	*time = t;
	return 1;
'''
AX0 = [('', [(PIN, '')])]
AXD = [('d', [])]
for k, (types, ext) in {
    'i': ('uint32_t block, len, t, off;\n	int left, done;', ''),
    'o': ('uint32_t block, len, t, left, done;\n	int off;', ''),
    'b': ('int block;\n	uint32_t len, t, off, left, done;', ''),
    'io': ('uint32_t block, len, t;\n	int off, left, done;', ''),
    'dd': ('uint32_t block, len, t, off, left;\n	int done;', ''),
}.items():
    AXD.append((k, [('	uint32_t block, len, t, off, left, done;\n', '	' + types + '\n')]))
SH = {
    'k': B,
    'ld': B.replace('	left = len;\n	done = 0;\n', '	done = 0;\n	left = len;\n'),
    'for': B.replace('	left = len;\n	done = 0;\n	while (left > 0x4000) {', '	done = 0;\n	for (left = len; left > 0x4000; left -= 0x4000) {').replace('		left -= 0x4000;\n', ''),
    'q': B.replace('	p = calloc(len, 1);\n	left = len;\n', '	left = len;\n	p = calloc(left, 1);\n'),
    'off2': B.replace('	off = fsOffset + (block << 14);\n	p = calloc(len, 1);\n', '	p = calloc(len, 1);\n	off = fsOffset + (block << 14);\n'),
    'rv': B.replace('	return 1;\n', '	return v;\n'),
    'noleft': B.replace('	if (left)\n', '	if (left != 0)\n'),
    'ptr': B.replace('	done = 0;\n', '').replace('		done += 0x4000;\n', '		q += 0x4000;\n').replace('p + done', 'q').replace('	left = len;\n', '	left = len;\n	q = p;\n'),
}
AXS = [(k, [(B, v)] if v != B else []) for k, v in SH.items()]
AXQ = [('', [('	uint8_t *p;\n	int v = fsValid;', '	uint8_t *p, *q;\n	int v = fsValid;')])]
AXV = [('vi', []), ('vu', [('	int v = fsValid;\n', '	uint32_t v = fsValid;\n')])]
AXES = [AX0, AXD, AXS, AXQ, AXV]
