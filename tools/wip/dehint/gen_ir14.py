"""parseDump with HEAD's unsigned n (blk's cast gives it the SSA name the compares want): the two
__builtin_unreachable only remove `dest < numBlocks` and `blk < blocks`; drop those tests."""
FOCUS = ['_parseDump']
BASE = 'tools/wip/dehint/drafts/image_read_attempt1.c'
AX1 = [('', [
    ('static int addRemapP(int block, int ablock, int cb, int dest, int numBlocks)', 'static int addRemapP(int block, int ablock, int cb, int dest)'),
    ('xb.badBlocks[i] == block && xb.badRemap[i] == -1 && dest < numBlocks', 'xb.badBlocks[i] == block && xb.badRemap[i] == -1'),
    ('addRemapP(b2, blk, 0, dst, blocks)', 'addRemapP(b2, blk, 0, dst)'),
    ('addRemapP(dst, dst, 0, blk, blocks)', 'addRemapP(dst, dst, 0, blk)'),
    ('''		if (blk >= blocks)
			__builtin_unreachable();
		if (dst != blk &&''', '''		if (dst != blk &&'''),
])]
AX2 = [
    ('g1', [('''			if (blk >= blocks)
				__builtin_unreachable();
			if (blk < blocks) {
				log_printf(1, "ECD error at block 0x%x (raw offset 0x%x), block will be remapped\\n", blk, src - raw);
				if (!addRemapP(blk, blk, blk, -1, blocks))
					return 0;
			}
''', '''			log_printf(1, "ECD error at block 0x%x (raw offset 0x%x), block will be remapped\\n", blk, src - raw);
			if (!addRemapP(blk, blk, blk, -1))
				return 0;
''')]),
]
AX3 = [('bk', []), ('b', [('''			__asm__("");
			dst = blk;
''', '''			dst = blk;
''')])]
AX4 = [('ck', []), ('c', [('''	__asm__("" : : "ri"(cb), "ri"(cb), "ri"(cb), "ri"(cb));
''', '')])]
AX5 = [('pk', []), ('p', [('''			__asm__("" : "+r"(b2));
''', '')])]
AXES = [AX1, AX2, AX3, AX4, AX5]
