"""parseDump, no barrier, arm rejoining before `if (dst != blk)` (gen_ir52 rj: 2 lines): only site 2's `n_100 == _125` (need n's name above the load's).  ch2 takes n's name
from the free list, whose top comes from dce2's deletions, so the shape of addRemapP's `valid` etc. decide it."""
FOCUS = ['_parseDump']
BASE = 'build/ir/a3/rj.c'
V1 = '	int valid = dest == -1 || (uint32_t)dest < numBlocks;\n'
AXV = [('v1', []),
       ('v2', [(V1, '	int valid = (uint32_t)dest < numBlocks || dest == -1;\n')]),
       ('v3', [(V1, '	int valid = dest < 0 || (uint32_t)dest < numBlocks;\n')]),
       ('v3b', [(V1, '	int valid = (uint32_t)dest < numBlocks || dest < 0;\n')]),
       ('v4', [(V1, '	int valid = dest != -1 ? (uint32_t)dest < numBlocks : 1;\n')]),
       ('v5', [(V1, '	int valid = dest == -1 ? 1 : (uint32_t)dest < numBlocks;\n')]),
       ('v6', [(V1, '	uint32_t limit = numBlocks;\n	int valid = dest == -1 || (uint32_t)dest < limit;\n')]),
       ('v7', [(V1, '	uint32_t d = dest;\n	int valid = dest == -1 || d < numBlocks;\n')]),
       ('v8', [(V1, '	int valid = 1;\n\n	if (dest != -1)\n		valid = (uint32_t)dest < numBlocks;\n')]),
       ('v9', [(V1, '	int valid = 1;\n\n	if (dest != -1 && (uint32_t)dest >= numBlocks)\n		valid = 0;\n')]),
       ('v10', [(V1, '	int valid = 0;\n\n	if (dest == -1 || (uint32_t)dest < numBlocks)\n		valid = 1;\n')]),
       ]
DCL = '	int i;\n	int found = 0;\n'
AXD = [('', []),
       ('di', [(DCL, '	int found = 0;\n	int i;\n')]),
       ]
AXC = [('', []),
       ('b2', [('			b2 = blk;\n			__asm__("" : "+r"(b2));\n			if (!addRemapP(b2, blk, 0, dst, blocks))', '			b2 = blk;\n			__asm__("" : "+r"(b2));\n			if (!addRemapP(b2, b2, 0, dst, blocks))')]),
       ]
AXES = [AXV, AXD, AXC]
