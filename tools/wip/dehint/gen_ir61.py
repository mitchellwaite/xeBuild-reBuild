"""parseDump rj: gen_ir60 v9 (`valid = (uint32_t)dest < numBlocks; if (dest == -1) valid = 1;`) moves n's name to _122 with the load at _126: more forms of valid, looking for n above the load."""
FOCUS = ['_parseDump']
BASE = 'build/ir/a3/rj.c'
SIG = 'static int addRemapP(int block, int ablock, int cb, int dest, int numBlocks)\n'
V1 = '	int valid = dest == -1 || (uint32_t)dest < numBlocks;\n'
U = '(uint32_t)dest < numBlocks'
F = {
    'v9': '	int valid = %s;\n\n	if (dest == -1)\n		valid = 1;\n' % U,
    'v9a': '	int valid = %s;\n\n	if (dest < 0)\n		valid = 1;\n' % U,
    'v11': '	int valid;\n\n	if (dest == -1)\n		valid = 1;\n	else\n		valid = %s;\n' % U,
    'v11a': '	int valid;\n\n	if (dest != -1)\n		valid = %s;\n	else\n		valid = 1;\n' % U,
    'v12': '	int valid = 1;\n\n	if ((uint32_t)dest >= numBlocks && dest != -1)\n		valid = 0;\n',
    'v13': '	int valid = 0;\n\n	if (%s)\n		valid = 1;\n	if (dest == -1)\n		valid = 1;\n' % U,
    'v14': '	int valid = 0;\n\n	if (dest == -1)\n		valid = 1;\n	if (%s)\n		valid = 1;\n' % U,
    'v14a': '	int valid;\n\n	if (dest == -1)\n		valid = 1;\n	else if (%s)\n		valid = 1;\n	else\n		valid = 0;\n' % U,
    'v15': '	int valid = %s;\n\n	valid |= dest == -1;\n' % U,
    'v16': '	int valid = dest == -1;\n\n	if (%s)\n		valid = 1;\n' % U,
    'v17': '	int valid = dest == -1;\n\n	valid |= %s;\n' % U,
    'v18': '	int valid = dest == -1;\n\n	if (!valid)\n		valid = %s;\n' % U,
    'v19': '	int valid = %s ? 1 : dest == -1;\n' % U,
    'v20': '	int valid = 1;\n\n	if (dest != -1) {\n		if ((uint32_t)dest >= numBlocks)\n			valid = 0;\n	}\n',
    'v21': '	int valid = 1;\n\n	if ((uint32_t)dest >= numBlocks) {\n		if (dest != -1)\n			valid = 0;\n	}\n',
    'v22': '	int valid = 1;\n\n	if (!(%s))\n		valid = dest == -1;\n' % U,
}
AXV = [(k, [(V1, v)]) for k, v in F.items()]
AX1 = [('', []),
       ('du', [(SIG, 'static int addRemapP(int block, int ablock, int cb, uint32_t dest, int numBlocks)\n')]),
       ('dun', [(SIG, 'static int addRemapP(int block, int ablock, int cb, uint32_t dest, uint32_t numBlocks)\n')]),
       ('nu', [(SIG, 'static int addRemapP(int block, int ablock, int cb, int dest, uint32_t numBlocks)\n')]),
       ]
AXES = [AXV, AX1]
