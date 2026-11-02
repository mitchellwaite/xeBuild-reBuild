"""val|cce3 family: alloc spellings that keep `size + align - 1` from being reassociated (so its name isn't on the free list for PRE)."""
import importlib.util, itertools, os


def load(n):
    spec = importlib.util.spec_from_file_location(n, os.path.join(os.path.dirname(__file__), n + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


g = load('gen_rf14')
g33 = load('gen_rf33')
SIG, R, P0, PS, FRE, SPR = g33.SIG, g33.R, g33.P0, g33.PS, g33.FRE, g33.SPR
GET = '	size = getFileSizeName(path);\n'
AL = {
 'p1': GET + '	alloc = size;\n	if (align) {\n		alloc = size + (align - 1);\n		alloc &= -align;\n	}\n',
 'p2': GET + '	alloc = size;\n	if (align) {\n		size_t mask = align - 1;\n		alloc = size + mask;\n		alloc &= -align;\n	}\n',
 'p3': GET + '	alloc = size;\n	if (align) {\n		size_t mask = align - 1;\n		alloc = (size + mask) & ~mask;\n	}\n',
 'p4': GET + '	alloc = size;\n	if (align)\n		alloc = (size + (align - 1)) & -align;\n',
 'p5': GET + '	alloc = size;\n	if (align) {\n		alloc = align - 1 + size;\n		alloc &= -align;\n	}\n',
 'p6': GET + '	alloc = size;\n	if (align) {\n		alloc = align + size - 1;\n		alloc &= -align;\n	}\n',
 'p7': GET + '	alloc = size;\n	if (align) {\n		alloc += align;\n		alloc--;\n		alloc &= -align;\n	}\n',
 'p8': GET + '	alloc = size;\n	if (align) {\n		alloc = size + align;\n		alloc -= 1;\n		alloc = alloc & -align;\n	}\n',
 'p9': GET + '	alloc = size;\n	if (align) {\n		alloc = size - 1 + align;\n		alloc &= -align;\n	}\n',
}
BODY = g33.BODY


def variants():
    for (an, al), (bn, b), pn in itertools.product(AL.items(), BODY.items(), g33.PICK):
        body = b.replace('LOG', g.LOG).replace('P0', P0).replace('PS', PS[pn]).replace('FRE', FRE).replace('R ==', R + ' ==')
        s = SIG + '\tvoid *buf = NULL;\n\tsize_t size, alloc;\n\n\tif (dir && name) {\n\t\tchar path[1024];\n\n' + SPR + al + '	buf = calloc(alloc, 1);\n' + body + '\t}\n\treturn buf;\n}\n'
        yield '|'.join([an, bn, pn]), s
