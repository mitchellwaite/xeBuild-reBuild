"""parseDump, unsigned loop: one hint doing the work of several: one __builtin_unreachable placed earlier instead of two; the b2 asm also
carrying pin_cb's extra uses; the guard at site 2 kept or not."""
FOCUS = ['_parseDump']
BASE = 'tools/wip/dehint/drafts/image_read_attempt2.c'
U1 = '''			if (blk >= blocks)
				__builtin_unreachable();
			if (blk < blocks) {
'''
U2 = '''		if (blk >= blocks)
			__builtin_unreachable();
		if (dst != blk &&'''
TOP = '''		blk = n;
		src = raw + blk * 528 * ppb;
'''
AFTER = '''		dst = checkBlock(src, blk, blocks);
'''
Z = '''		if (blk == 0) {
			if (!notZeropair()) {'''
UN = '''		if (blk >= blocks)
			__builtin_unreachable();
'''
AX1 = [
    ('k', []),
    ('top', [(U1, '			if (blk < blocks) {\n'), (U2, '		if (dst != blk &&'), (TOP, '		blk = n;\n' + UN + '		src = raw + blk * 528 * ppb;\n')]),
    ('aft', [(U1, '			if (blk < blocks) {\n'), (U2, '		if (dst != blk &&'), (AFTER, AFTER + UN)]),
    ('z', [(U1, '			if (blk < blocks) {\n'), (U2, '		if (dst != blk &&'), (Z, UN + Z)]),
    ('s1', [(U2, '		if (dst != blk &&')]),
    ('s2', [(U1, '			if (blk < blocks) {\n')]),
    ('z2', [(U1, '			if (blk < blocks) {\n'), (Z, UN + Z)]),
]
AX2 = [('gk', []), ('g0', [('''			if (blk < blocks) {
				log_printf(1, "ECD error at block 0x%x (raw offset 0x%x), block will be remapped\\n", blk, src - raw);
				if (!addRemapP(blk, blk, blk, -1, blocks))
					return 0;
			}
''', '''			log_printf(1, "ECD error at block 0x%x (raw offset 0x%x), block will be remapped\\n", blk, src - raw);
			if (!addRemapP(blk, blk, blk, -1, blocks))
				return 0;
''')])]
CB = '''	__asm__("" : : "ri"(cb), "ri"(cb), "ri"(cb), "ri"(cb));
'''
B2 = '''			__asm__("" : "+r"(b2));
'''
AX3 = [('ck', []),
       ('c0', [(CB, '')]),
       ('c1', [(CB, ''), (B2, '			__asm__("" : "+r"(b2) : "ri"(blk), "ri"(blk));\n')]),
       ('c2', [(CB, ''), (B2, '			__asm__("" : "+r"(b2) : "m"(blk));\n')]),
       ('c3', [(CB, ''), (B2, '			__asm__("" : "+r"(b2) : "ri"(blk), "ri"(blk), "ri"(blk), "ri"(blk), "ri"(blk), "ri"(blk), "ri"(blk), "ri"(blk));\n')]),
]
AX4 = [('bk', []), ('b0', [('''			__asm__("");
			dst = blk;
''', '''			dst = blk;
''')])]
AXES = [AX1, AX2, AX3, AX4]
