"""parseDump, unsigned n: which of the site-2 guard and its unreachable, the asm, b2 and cb can go
while site 3 keeps `dest < numBlocks` and its unreachable."""
FOCUS = ['_parseDump']
BASE = 'tools/wip/dehint/drafts/image_read_attempt1.c'
G = '''			if (blk >= blocks)
				__builtin_unreachable();
			if (blk < blocks) {
				log_printf(1, "ECD error at block 0x%x (raw offset 0x%x), block will be remapped\\n", blk, src - raw);
				if (!addRemapP(blk, blk, blk, -1, blocks))
					return 0;
			}
'''
AX1 = [('gk', []),
       ('g1', [(G, '''			log_printf(1, "ECD error at block 0x%x (raw offset 0x%x), block will be remapped\\n", blk, src - raw);
			if (!addRemapP(blk, blk, blk, -1, blocks))
				return 0;
''')]),
       ('g2', [(G, '''			if (blk < blocks) {
				log_printf(1, "ECD error at block 0x%x (raw offset 0x%x), block will be remapped\\n", blk, src - raw);
				if (!addRemapP(blk, blk, blk, -1, blocks))
					return 0;
			}
''')])]
AX3 = [('bk', []), ('b', [('''			__asm__("");
			dst = blk;
''', '''			dst = blk;
''')])]
AX4 = [('ck', []), ('c', [('''	__asm__("" : : "ri"(cb), "ri"(cb), "ri"(cb), "ri"(cb));
''', '')])]
AX5 = [('pk', []), ('p', [('''			__asm__("" : "+r"(b2));
''', '')])]
AX6 = [('u2k', []), ('u2', [('''		if (blk >= blocks)
			__builtin_unreachable();
		if (dst != blk &&''', '''		if (dst != blk &&''')])]
AXES = [AX1, AX3, AX4, AX5, AX6]
