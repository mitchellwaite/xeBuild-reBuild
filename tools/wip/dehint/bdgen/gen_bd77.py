"""patchBlsBlmod without no-early-inlining: the spill order follows partition numbers.  Parts of it as static functions, called once and not
early inlined (they hold calls), number their SSA names apart."""
REMOVE = ['nei_blmod']
FOCUS = ['_patchBlsBlmod']
HEAD = 'void patchBlsBlmod(const void *blmod, int size)\n{'
TAIL = '''	if (blmod && size) {
		log_printf(1, "Done!\\n");
		if (!xb.cbb)
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
	}
'''
BODY = TAIL[TAIL.index('\t\tif (!xb.cbb)'):TAIL.rindex('\t}\n')].replace('\n\t\t', '\n\t').replace('\t\t', '\t', 1)
F1 = 'static void addBlmod(const void *blmod, int size, int cd, int cbb)\n{\n	uint32_t off, max, end, i;\n\n' + BODY + '}\n\n'
F2 = 'static void addBlmod(const void *blmod, int size, int cbb)\n{\n	uint32_t off, max, end, i;\n\n' + BODY.replace('	if (!xb.cbb)\n		cbb = cd;\n', '') + '}\n\n'
WALK0 = TAIL
A = [
    ('t1', [(TAIL, '	if (blmod && size) {\n		log_printf(1, "Done!\\n");\n		addBlmod(blmod, size, cd, cbb);\n	}\n'), (HEAD, F1 + HEAD),
            ('uint32_t off, addr, len, i, max, end, t;', 'uint32_t off, addr, len, i, t;')]),
    ('t2', [(TAIL, '	if (blmod && size) {\n		log_printf(1, "Done!\\n");\n		addBlmod(blmod, size, xb.cbb ? cbb : cd);\n	}\n'), (HEAD, F2 + HEAD),
            ('uint32_t off, addr, len, i, max, end, t;', 'uint32_t off, addr, len, i, t;')]),
    ('t3', [(TAIL, '	if (blmod && size) {\n		log_printf(1, "Done!\\n");\n		if (!xb.cbb)\n			cbb = cd;\n		addBlmod(blmod, size, cbb);\n	}\n'), (HEAD, F2 + HEAD),
            ('uint32_t off, addr, len, i, max, end, t;', 'uint32_t off, addr, len, i, t;')]),
]
AXES = [A]
