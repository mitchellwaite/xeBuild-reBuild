"""patchBlsBlmod without no-early-inlining.  Spill order follows the partition numbers: pt's partition holds i_20 (a freed low
SSA name reused for the third findFile's i) where the reference's has i_130, and cd's has _68.  Neutral statement shapes
that free one name more or less, singly and in pairs and triples."""
import itertools

E = {
    'off0dec': [('uint32_t off, addr, len, i, max, end, t;', 'uint32_t off = 0, addr, len, i, max, end, t;'), ('	log_printf(1, "Patching BLs...");\n	off = 0;\n', '	log_printf(1, "Patching BLs...");\n')],
    'nlate': [('	int n = 0;\n\n	log_printf(1, "Patching BLs...");\n', '	int n;\n\n	log_printf(1, "Patching BLs...");\n	n = 0;\n')],
    'for': [('	off = 0;\n	while (off < p->size) {\n		if (n != 2) {\n			addr =', '	for (off = 0; off < p->size;) {\n		if (n != 2) {\n			addr =')],
    'plate': [('	struct fileent *p = &xb.files[pt];\n	uint8_t *d = p->data;\n', '	struct fileent *p;\n	uint8_t *d;\n'), ('	log_printf(1, "Patching BLs...");\n', '	p = &xb.files[pt];\n	d = p->data;\n	log_printf(1, "Patching BLs...");\n')],
    'dlate': [('	uint8_t *d = p->data;\n', '	uint8_t *d;\n'), ('	log_printf(1, "Patching BLs...");\n', '	log_printf(1, "Patching BLs...");\n	d = p->data;\n')],
    'split': [('	int cd = findFile(7), cbb = findFile(6), pt = findFile(23);\n', '	int cd = findFile(7);\n	int cbb = findFile(6);\n	int pt = findFile(23);\n')],
    'pinline': [('	struct fileent *p = &xb.files[pt];\n	uint8_t *d = p->data;\n', '	struct fileent *p = &xb.files[findFile(23)];\n	uint8_t *d = p->data;\n'), (', pt = findFile(23);', ';')],
    'addrend': [('		i = end - xb.files[cbb].size;\n		xb.hdr[0x49] = i >> 8;\n		xb.hdr[0x4a] = i;\n', '		xb.hdr[0x49] = (end - xb.files[cbb].size) >> 8;\n		xb.hdr[0x4a] = end - xb.files[cbb].size;\n')],
    'nest': [('	if (blmod && size) {\n', '	if (blmod) {\n	if (size) {\n'), ('		setBeU32(end, xb.files[cbb].data + 12);\n	}\n	log_printf(1, "Done!\\n");\n}\n\nvoid fixupPatchSet', '		setBeU32(end, xb.files[cbb].data + 12);\n	}\n	}\n	log_printf(1, "Done!\\n");\n}\n\nvoid fixupPatchSet')],
    'tinl': [('			t = off + 4;\n			if (addr != 0xffffffff) {\n				len = getBeU32(d + t) * 4;\n', '			t = off + 4;\n			if (addr != 0xffffffff) {\n				len = getBeU32(d + off + 4) * 4;\n')],
    'lenscope': [('uint32_t off, addr, len, i, max, end, t;', 'uint32_t off, addr, i, max, end, t;'), ('				len = getBeU32(d + t) * 4;\n', '				uint32_t len = getBeU32(d + t) * 4;\n\n')],
    'addrscope': [('uint32_t off, addr, len, i, max, end, t;', 'uint32_t off, len, i, max, end, t;'), ('			addr = getBeU32(d + off);\n', '			uint32_t addr = getBeU32(d + off);\n\n')],
    'tscope': [('uint32_t off, addr, len, i, max, end, t;', 'uint32_t off, addr, len, i, max, end;'), ('			addr = getBeU32(d + off);\n			t = off + 4;\n', '			uint32_t t;\n\n			addr = getBeU32(d + off);\n			t = off + 4;\n')],
    'iscope': [('			for (i = 0; i < p->size - off; i++)\n				p->data[i] = p->data[off + i];\n', '			{\n			uint32_t j;\n\n			for (j = 0; j < p->size - off; j++)\n				p->data[j] = p->data[off + j];\n			}\n')],
    'max': [('		max = xb.cbb ? 0xc000 : 0x10000;\n', '		max = 0x10000;\n		if (xb.cbb)\n			max = 0xc000;\n')],
    'size': [('	if (blmod && size) {\n', '	if (size && blmod) {\n')],
    'd': [('				p->data[i] = p->data[off + i];\n', '				d[i] = d[off + i];\n')],
    'psize': [('			p->size -= off;\n			off = p->size;\n', '			off = p->size -= off;\n')],
    'files': [('			for (i = 0; i < p->size - off; i++)\n				p->data[i] = p->data[off + i];\n			p->size -= off;\n			off = p->size;\n', '			for (i = 0; i < xb.files[pt].size - off; i++)\n				xb.files[pt].data[i] = xb.files[pt].data[off + i];\n			xb.files[pt].size -= off;\n			off = xb.files[pt].size;\n')],
}


def CASES(base):
    out = []
    names = list(E)

    def mk(c):
        def f(t):
            for n in c:
                for a, b in E[n]:
                    if a not in t:
                        return None
                    t = t.replace(a, b)
            return t
        return f
    for k in (1, 2, 3):
        for c in itertools.combinations(names, k):
            out.append(('nei_blmod', '+'.join(c), mk(c)))
    return out
