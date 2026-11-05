"""patchBlsBlmod without its no-early-inlining: spill order of pt and cbb, third try"""
REMOVE = ['nei_blmod']
FOCUS = ['_patchBlsBlmod']
TAIL0 = '''		if (!xb.cbb)
			cbb = cd;
		max = xb.cbb ? 0xc000 : 0x10000;
		off = getBeU32(xb.files[cbb].data + 12);
		end = (off + size + 15) & ~15;
		if (end > max) {
			size -= end - max;
			log_printf(0, "***** WARNING: blmod.bin is 0x%x bytes too large, truncating to 0x%x bytes!\\n", end - max, max - off);
		}
		log_printf(1, "Adding 0x%x bytes blmod.bin data to %s...", size, xb.cbb ? "CBB" : "CD");
		memcpy(xb.files[cbb].data + off, blmod, size);
		end = (off + size + 15) & ~15;
		i = end - xb.files[cbb].size;
		xb.hdr[0x49] = i >> 8;
		xb.hdr[0x4a] = i;
		xb.files[cbb].size = end;
		setBeU32(end, xb.files[cbb].data + 12);
'''
DST = TAIL0.replace('''		if (!xb.cbb)
			cbb = cd;
''', '''		int dst = xb.cbb ? cbb : cd;

''').replace('xb.files[cbb]', 'xb.files[dst]')
DST2 = TAIL0.replace('''		if (!xb.cbb)
			cbb = cd;
''', '''		int dst = cbb;

		if (!xb.cbb)
			dst = cd;
''').replace('xb.files[cbb]', 'xb.files[dst]')
PTR = TAIL0.replace('''		if (!xb.cbb)
			cbb = cd;
''', '''		struct fileent *f = xb.cbb ? &xb.files[cbb] : &xb.files[cd];

''').replace('xb.files[cbb]', 'f->')
PTR = PTR.replace('f->.data', 'f->data').replace('f->.size', 'f->size')
DECL = '''	int cd = findFile(7), cbb = findFile(6), pt = findFile(23);
	struct fileent *p = &xb.files[pt];
	uint8_t *d = p->data;
'''
A = [('', []), ('dst', [(TAIL0, DST)]), ('dst2', [(TAIL0, DST2)]), ('ptr', [(TAIL0, PTR)])]
B = [
    ('', []),
    ('sp', [('''			for (i = 0; i < p->size - off; i++)
				p->data[i] = p->data[off + i];
			p->size -= off;
			off = p->size;
''', '''			for (i = 0; i < p->size - off; i++)
				d[i] = d[off + i];
			p->size -= off;
			off = p->size;
''')]),
    ('pt', [('''			for (i = 0; i < p->size - off; i++)
				p->data[i] = p->data[off + i];
			p->size -= off;
			off = p->size;
''', '''			for (i = 0; i < xb.files[pt].size - off; i++)
				xb.files[pt].data[i] = xb.files[pt].data[off + i];
			xb.files[pt].size -= off;
			off = xb.files[pt].size;
''')]),
]
AXES = [A, B]
