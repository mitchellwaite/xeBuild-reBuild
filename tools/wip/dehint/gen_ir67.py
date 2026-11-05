"""parseDump: signed `for (blk...)` and the real addRemap (dest < numBlocks folds by VRP at site 3), addRemapP gone."""
FOCUS = ['_parseDump', '_addRemap']
S1 = 'if (!addRemapP(b2, blk, 0, dst, blocks))'
S2 = 'if (!addRemapP(blk, blk, blk, -1, blocks))'
S3 = 'if (dst != blk && !addRemapP(dst, dst, 0, blk, blocks))'
PIN = '''			b2 = blk;
			__asm__("" : "+r"(b2));
'''
LOOP = '''	for (n = 0; n < blocks; n++) {
		blk = n;
'''
UNR = '''			if (blk >= blocks)
				__builtin_unreachable();
'''
REMOVE = []
AX0 = [('real', [(S1, 'if (!addRemap(blk, dst, blocks))'), (S2, 'if (!addRemap(blk, -1, blocks))'), (S3, 'if (dst != blk && !addRemap(dst, blk, blocks))'), (PIN, '')])]
AX1 = [('sfor', [(LOOP, '	for (blk = 0; blk < blocks; blk++) {\n')]),
       ('ufor', [])]
AX2 = [('', []), ('nolab', [('rem: __attribute__((hot));\n', '')])]
AX3 = [('', []), ('nou', [(UNR, '')])]
AX4 = [('', []),
       ('rj', [('''			dst = blk;
		}
rem: __attribute__((hot));
		if (dst != blk) {''', '''			dst = blk;
		} else
		if (dst != blk) {''')]) if False else ('', []),
       ]
AX5 = [('', []), ('ib', [('int addRemap(uint32_t block, int dest, int numBlocks)\n', 'int addRemap(int block, int dest, int numBlocks)\n'),
                         ('int addRemap(uint32_t block, int dest, int numBlocks);', 'int addRemap(int block, int dest, int numBlocks);')])]
AX6 = [('', []), ('inob', [('	uint32_t b = block;	/* unused; puts block before the loads in compares */\n', '')])]
AXES = [AX0, AX1, AX2, AX3, AX5, AX6]
