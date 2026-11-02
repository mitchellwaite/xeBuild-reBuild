"""Spellings of the size/alloc code x value-flag shapes: PRE's prephitmp name comes from the free list, its version decides `_x >= prephitmp` vs `prephitmp <= _x`."""
import importlib.util, itertools, os


def load(n):
    spec = importlib.util.spec_from_file_location(n, os.path.join(os.path.dirname(__file__), n + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


g = load('gen_rf14')
g31 = load('gen_rf31')
SIG, R, P0, PS = g31.SIG, g31.R, g31.P0, g31.PS
FRE = g31.FRE
SPR = '	sprintf(path, "%s%s", dir, name);\n'
AL = {
 'a0': '	size = getFileSizeName(path);\n	alloc = size;\n	if (align) {\n		alloc = size + align - 1;\n		alloc &= -align;\n	}\n',
 'a1': '	size = getFileSizeName(path);\n	alloc = size;\n	if (align)\n		alloc = (size + align - 1) & -align;\n',
 'a2': '	size = getFileSizeName(path);\n	if (align)\n		alloc = (size + align - 1) & -align;\n	else\n		alloc = size;\n',
 'a3': '	size = getFileSizeName(path);\n	alloc = align ? (size + align - 1) & -align : size;\n',
 'a4': '	alloc = size = getFileSizeName(path);\n	if (align)\n		alloc = (size + align - 1) & -align;\n',
 'a5': '	alloc = size = getFileSizeName(path);\n	if (align) {\n		alloc += align - 1;\n		alloc &= -align;\n	}\n',
 'a6': '	size = getFileSizeName(path);\n	alloc = size;\n	if (align) {\n		alloc += align - 1;\n		alloc &= -align;\n	}\n',
 'a7': '	size = getFileSizeName(path);\n	alloc = size;\n	if (align) {\n		alloc = alloc + align - 1;\n		alloc &= ~(align - 1);\n	}\n',
 'a8': '	size = getFileSizeName(path);\n	if (align) {\n		alloc = size + align - 1;\n		alloc &= -align;\n	} else\n		alloc = size;\n',
 'a9': '	alloc = getFileSizeName(path);\n	size = alloc;\n	if (align) {\n		alloc = size + align - 1;\n		alloc &= -align;\n	}\n',
 'a10': '	alloc = getFileSizeName(path);\n	size = alloc;\n	if (align)\n		alloc = (alloc + align - 1) & -align;\n',
 'a11': '	long fsize = getFileSizeName(path);\n	size = fsize;\n	alloc = fsize;\n	if (align) {\n		alloc = size + align - 1;\n		alloc &= -align;\n	}\n',
}
BODY = {
 'val': '	if (buf == NULL) {\n		LOG\nP0	} else {\n		int ok = R == size;\nPS		if (!ok) {\nFRE		}\n	}\n',
 'dec': '	if (buf) {\n		int ok = R == size;\nPS		if (!ok) {\nFRE		}\n	} else {\n		LOG\nP0	}\n',
 'set': '	if (buf == NULL) {\n		LOG\nP0	} else {\n		int ok = 0;\n		if (R == size)\n			ok = 1;\nPS		if (!ok) {\nFRE		}\n	}\n',
}
PICK = ('nest', 'cce3', 'ccn', 'cc', 'nestn')


def variants():
    for (an, al), (bn, b), pn, order in itertools.product(AL.items(), BODY.items(), PICK, ['sa', 'ds']):
        decl = '\tvoid *buf = NULL;\n\tsize_t size, alloc;\n\n' if order == 'sa' else '\tsize_t size, alloc;\n\tvoid *buf = NULL;\n\n'
        body = b.replace('LOG', g.LOG).replace('P0', P0).replace('PS', PS[pn]).replace('FRE', FRE).replace('R ==', R + ' ==')
        s = SIG + decl + '\tif (dir && name) {\n\t\tchar path[1024];\n\n' + SPR + al + '	buf = calloc(alloc, 1);\n' + body + '\t}\n\treturn buf;\n}\n'
        yield '|'.join([an, bn, pn, order]), s
