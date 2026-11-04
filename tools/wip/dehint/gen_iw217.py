# attempt 14: the pad test. `pad == 1 && tail` (FE folds it to one `&` branch, 2-3 more names) flips the big copy's compare but costs imgAdd's two branches. Forms that spend names and keep the two branches.
import os
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_near13.c')
OLD = '	if (pad == 1) if (tail)\n		memset(xb.hdr + off + len, 0, ((off + len + 0x3fff) & ~0x3fff) - (off + len));\n'
MS = '		memset(xb.hdr + off + len, 0, ((off + len + 0x3fff) & ~0x3fff) - (off + len));\n'
F = {
 '': None,
 'tp': '	if (tail) if (pad == 1)\n' + MS,
 'q1': '	if (pad == 1 ? tail != 0 : 0)\n' + MS,
 'q2': '	if (tail ? pad == 1 : 0)\n' + MS,
 'q3': '	if (pad != 1 ? 0 : tail)\n' + MS,
 'q4': '	if (!tail ? 0 : pad == 1)\n' + MS,
 'v1': '	{\n		int zero = pad == 1;\n\n		if (zero) if (tail)\n' + MS + '	}\n',
 'v2': '	{\n		int zero = tail != 0;\n\n		if (pad == 1) if (zero)\n' + MS + '	}\n',
 'v3': '	{\n		int zero = 0;\n\n		if (pad == 1) if (tail) zero = 1;\n		if (zero)\n' + MS + '	}\n',
 'v4': '	{\n		int zero = 0;\n\n		if (tail) zero = pad == 1;\n		if (zero)\n' + MS + '	}\n',
 'v5': '	{\n		int zero = 0;\n\n		if (pad == 1) zero = tail != 0;\n		if (zero)\n' + MS + '	}\n',
 'n1': '	if (pad == 1 && ((off + len) & 0x3fff))\n' + MS,
 'n2': '	if (((off + len) & 0x3fff) && pad == 1)\n' + MS,
 'n3': '	if (pad == 1 && (len + off) % 0x4000)\n' + MS,
 'n4': '	if (tail && (pad == 1) && 1)\n' + MS,
 's1': '	if (pad == 1) if (tail) {\n		uint32_t e = off + len, n = 0x4000 - (e & 0x3fff);\n\n		memset(xb.hdr + e, 0, n);\n	}\n',
 's2': '	if (pad == 1) if (tail) {\n		uint32_t e = off + len, n = ((e + 0x3fff) & ~0x3fff) - e;\n\n		memset(xb.hdr + e, 0, n);\n	}\n',
 's3': '	if (pad == 1) if (tail) {\n		uint32_t e = off + len;\n		uint8_t *d = xb.hdr + e;\n\n		memset(d, 0, ((e + 0x3fff) & ~0x3fff) - e);\n	}\n',
 's4': '	if (pad == 1) if (tail) {\n		uint32_t e = (off + len) & 0x3fff;\n\n		if (e)\n			memset(xb.hdr + off + len, 0, 0x4000 - e);\n	}\n',
}
AXES = [[(k, [(OLD, v)] if v else []) for k, v in F.items()]]
FLAGS = []
