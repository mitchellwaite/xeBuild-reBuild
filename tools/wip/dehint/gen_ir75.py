"""base3 (parseDump matches): addRemap's standalone `cmp esi,[mem]`: forms of block's conversion, with parseDump kept."""
BASE = 'tools/wip/dehint/drafts/image_read_attempt4_base3.c'
FOCUS = None
SIG = 'int addRemap(int block, int dest, int numBlocks)'
HEAD = '''	uint32_t i;
	int found = 0;
'''
CMP = 'if (block == xb.badBlocks[i] && xb.badRemap[i] == -1 && dest < numBlocks) {'
STORE = 'xb.badBlocks[xb.numBad] = block;'
A = [('', []),
     ('u', [(SIG + ';', 'int addRemap(uint32_t block, int dest, int numBlocks);'), (SIG + '\n', 'int addRemap(uint32_t block, int dest, int numBlocks)\n')]),
     ]
B = [('', []),
     ('dead', [(HEAD, '	uint32_t i;\n	int found = 0;\n	uint32_t b = block;\n')]),
     ('live', [(HEAD, '	uint32_t i;\n	int found = 0;\n	uint32_t b = block;\n'), (CMP, 'if (b == xb.badBlocks[i] && xb.badRemap[i] == -1 && dest < numBlocks) {')]),
     ('live2', [(HEAD, '	uint32_t i;\n	int found = 0;\n	uint32_t b = block;\n'), (CMP, 'if (b == xb.badBlocks[i] && xb.badRemap[i] == -1 && dest < numBlocks) {'), (STORE, 'xb.badBlocks[xb.numBad] = b;')]),
     ('dead2', [(HEAD, '	uint32_t b = block;\n	uint32_t i;\n	int found = 0;\n')]),
     ('rev', [(CMP, 'if (xb.badBlocks[i] == block && xb.badRemap[i] == -1 && dest < numBlocks) {')]),
     ('cast', [(CMP, 'if ((uint32_t)block == xb.badBlocks[i] && xb.badRemap[i] == -1 && dest < numBlocks) {')]),
     ('icast', [(CMP, 'if (block == (int)xb.badBlocks[i] && xb.badRemap[i] == -1 && dest < numBlocks) {')]),
     ('irev', [(CMP, 'if ((int)xb.badBlocks[i] == block && xb.badRemap[i] == -1 && dest < numBlocks) {')]),
     ('nest', [(CMP, 'if (block == xb.badBlocks[i])\n			if (xb.badRemap[i] == -1 && dest < numBlocks) {')]),
     ('p', [(CMP, 'if (block == *(xb.badBlocks + i) && xb.badRemap[i] == -1 && dest < numBlocks) {')]),
     ]
C = [('', []),
     ('f', [('	uint32_t i;\n	int found = 0;\n', '	int found = 0;\n	uint32_t i;\n')])]
D = [('', []),
     ('d1', [('int found = 0;\n', 'int found;\n'), ('	for (i = 0; i < xb.numBad; i++) {\n		if (block', '	found = 0;\n	for (i = 0; i < xb.numBad; i++) {\n		if (block')])]
AXES = [A, B, C]
