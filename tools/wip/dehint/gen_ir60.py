"""parseDump rj: dce2 deletes _135, _100, dest.43_98 (site 2, then site 1's two) and n pops _100: site 1 leaving one statement fewer gives n _135.  Param types of addRemapP that do that."""
FOCUS = ['_parseDump']
BASE = 'build/ir/a3/rj.c'
SIG = 'static int addRemapP(int block, int ablock, int cb, int dest, int numBlocks)\n'
V1 = '	int valid = dest == -1 || (uint32_t)dest < numBlocks;\n'
AX1 = [('', []),
       ('du', [(SIG, 'static int addRemapP(int block, int ablock, int cb, uint32_t dest, int numBlocks)\n')]),
       ('dun', [(SIG, 'static int addRemapP(int block, int ablock, int cb, uint32_t dest, uint32_t numBlocks)\n')]),
       ('nu', [(SIG, 'static int addRemapP(int block, int ablock, int cb, int dest, uint32_t numBlocks)\n')]),
       ]
AXV = [('', []),
       ('v2', [(V1, '	int valid = (uint32_t)dest < numBlocks || dest == -1;\n')]),
       ('v8', [(V1, '	int valid = 1;\n\n	if (dest != -1)\n		valid = (uint32_t)dest < numBlocks;\n')]),
       ('v9', [(V1, '	int valid = (uint32_t)dest < numBlocks;\n\n	if (dest == -1)\n		valid = 1;\n')]),
       ('v10', [(V1, '	uint32_t d = dest;\n	int valid = d < numBlocks || d == -1;\n')]),
       ]
AXB = [('', []),
       ('bu', [('static int addRemapP(int block,', 'static int addRemapP(uint32_t block,')]),
       ]
AXS = [('', []),
       ('s1', [('if (!addRemapP(b2, blk, 0, dst, blocks))', 'if (!addRemapP(b2, blk, 0, (uint32_t)dst, blocks))')]),
       ]
AXES = [AX1, AXV, AXB]
