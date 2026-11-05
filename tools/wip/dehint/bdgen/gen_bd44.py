# patchBlsBlmod without no-early-inlining: conversions of findFile's result and the size param's type.
REMOVE = ['nei_blmod']
FOCUS = ['_patchBlsBlmod']
S = 'void patchBlsBlmod(const void *blmod, int size)'
D = '	int cd = findFile(7), cbb = findFile(6), pt = findFile(23);\n'
AXES = [
    [('', []), ('uall', [(D, '	uint32_t cd = findFile(7), cbb = findFile(6), pt = findFile(23);\n')]),
     ('ucb', [(D, '	int cd = findFile(7);\n	uint32_t cbb = findFile(6);\n	int pt = findFile(23);\n')]),
     ('upt', [(D, '	int cd = findFile(7), cbb = findFile(6);\n	uint32_t pt = findFile(23);\n')]),
     ('ucd', [(D, '	uint32_t cd = findFile(7);\n	int cbb = findFile(6), pt = findFile(23);\n')]),
     ('ucc', [(D, '	uint32_t cd = findFile(7), cbb = findFile(6);\n	int pt = findFile(23);\n')])],
    [('', []), ('su', [(S, 'void patchBlsBlmod(const void *blmod, uint32_t size)')])],
]
