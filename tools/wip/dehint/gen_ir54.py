"""parseDump rj: n's name in ch2 = top of the free list = dce2's last deletion, in rj site 1's dead `dest.43_98 = -1` (VRP made dst -1).  Literal -1 at site 1 frees it earlier; other
arguments and the first test's spellings for the same."""
FOCUS = ['_parseDump']
BASE = 'build/ir/a3/rj.c'
S1 = 'if (!addRemapP(b2, blk, 0, dst, blocks))'
AX1 = [('', []),
       ('m1', [(S1, 'if (!addRemapP(b2, blk, 0, -1, blocks))')]),
       ]
V1 = '	int valid = dest == -1 || (uint32_t)dest < numBlocks;\n'
AXV = [('v1', []),
       ('v2', [(V1, '	int valid = (uint32_t)dest < numBlocks || dest == -1;\n')]),
       ('v4', [(V1, '	int valid = dest != -1 ? (uint32_t)dest < numBlocks : 1;\n')]),
       ('v8', [(V1, '	int valid = 1;\n\n	if (dest != -1)\n		valid = (uint32_t)dest < numBlocks;\n')]),
       ('v9', [(V1, '	int valid = 1;\n\n	if (dest != -1 && (uint32_t)dest >= numBlocks)\n		valid = 0;\n')]),
       ]
S2 = 'if (!addRemapP(blk, blk, blk, -1, blocks))'
AX2 = [('', []),
       ('s2', [(S2, 'if (!addRemapP(blk, blk, n, -1, blocks))')]),
       ('s2b', [(S2, 'if (!addRemapP(n, blk, blk, -1, blocks))')]),
       ('s2c', [(S2, 'if (!addRemapP(blk, n, blk, -1, blocks))')]),
       ('s2d', [(S2, 'if (!addRemapP(n, n, n, -1, blocks))')]),
       ]
S3 = 'if (dst != blk && !addRemapP(dst, dst, 0, blk, blocks))'
AX3 = [('', []),
       ('s3', [(S3, 'if (dst != blk && !addRemapP(dst, dst, 0, n, blocks))')]),
       ]
AXES = [AX1, AXV, AX2, AX3]
