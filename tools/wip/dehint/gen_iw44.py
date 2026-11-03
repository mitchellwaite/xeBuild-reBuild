# attempt 3: `pad == 1 && tail` gets every iv compare in writeFsTable right but changes the CFG (514 lines): it spends a few more names.  Forms around the
# memset that spend names without changing the CFG, on the near removal sets of gen_iw43.
import importlib.util, os
_s = importlib.util.spec_from_file_location('g43', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_iw43.py'))
_m = importlib.util.module_from_spec(_s)
_s.loader.exec_module(_m)
OLD = '	if (pad == 1) if (tail)\n		memset(xb.hdr + off + len, 0, ((off + len + 0x3fff) & ~0x3fff) - (off + len));\n'
MS = '		memset(xb.hdr + off + len, 0, ((off + len + 0x3fff) & ~0x3fff) - (off + len));\n'
V = '	uint32_t x, first, rem, tail, blocks, start, p, end, npages, pages;\n'
F = {
 'p0': OLD,
 'p1': '	{ int zero = pad == 1;\n	if (zero) if (tail)\n' + MS + '	}\n',
 'p2': '	if (pad == 1 ? tail != 0 : 0)\n' + MS,
 'p3': '	if (pad != 1) ; else if (tail)\n' + MS,
 'p4': '	if (pad == 1) {\n		if (tail) {\n			uint32_t e = off + len;\n\n			memset(xb.hdr + e, 0, ((e + 0x3fff) & ~0x3fff) - e);\n		}\n	}\n',
 'p5': '	if (pad == 1) {\n		if (tail) {\n			uint8_t *e = xb.hdr + off + len;\n\n			memset(e, 0, ((off + len + 0x3fff) & ~0x3fff) - (off + len));\n		}\n	}\n',
 'p6': '	if (pad == 1) {\n		if (tail) {\n			uint32_t n = ((off + len + 0x3fff) & ~0x3fff) - (off + len);\n\n			memset(xb.hdr + off + len, 0, n);\n		}\n	}\n',
 'p7': '	if (pad == 1) {\n		if (tail) {\n			uint32_t e = (off + len + 0x3fff) & ~0x3fff;\n\n			memset(xb.hdr + off + len, 0, e - (off + len));\n		}\n	}\n',
 'p8': '	if (pad == 1) {\n		if (tail) {\n			uint32_t e = off + len, r = (e + 0x3fff) & ~0x3fff;\n\n			memset(xb.hdr + e, 0, r - e);\n		}\n	}\n',
 'p9': '	if (pad == 1) if (tail != 0)\n' + MS,
 'pa': '	if ((pad == 1) != 0) if (tail)\n' + MS,
 'pb': '	if (pad == 1) if (tail)\n		memset(xb.hdr + off + len, 0, 0x4000 - ((off + len) & 0x3fff));\n',
 'pc': '	if (pad == 1) if (tail)\n		memset(&xb.hdr[off + len], 0, ((off + len + 0x3fff) & ~0x3fff) - (off + len));\n',
 'pd': '	if (pad == 1) if (tail)\n		memset((xb.hdr + off) + len, 0, ((len + off + 0x3fff) & ~0x3fff) - (len + off));\n',
}
AXES = [_m.SETS, [(k, [(OLD, v)] if k != 'p0' else []) for k, v in F.items()]]
