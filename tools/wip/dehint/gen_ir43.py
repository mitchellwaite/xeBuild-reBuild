"""parseDump: gen_ir42's z leaves two PHIs for dst (the -4 arm threads past the unreachable's test: dst_185 joins dst_1 and blk, a late name,
so `blk != dst_185` has blk first; HEAD's barrier keeps one PHI, dst_1).  Unreachable(s) elsewhere; label says how many tricks stay."""
FOCUS = ['_parseDump']
BASE = 'tools/wip/dehint/drafts/image_read_attempt2.c'
U1 = '''			if (blk >= blocks)
				__builtin_unreachable();
			if (blk < blocks) {
'''
U2 = '''		if (blk >= blocks)
			__builtin_unreachable();
		if (dst != blk && !addRemapP(dst, dst, 0, blk, blocks))
'''
Z = '''		if (blk == 0) {
			if (!notZeropair()) {'''
UN = '''		if (blk >= blocks)
			__builtin_unreachable();
'''
BAR = '''			__asm__("");
			dst = blk;
'''
ELSE = '''rem: __attribute__((hot));
'''
E2 = '''					dst = blk;
				}
			}
		}
		if (blk == 0) {'''
A4 = '''		if (dst == -4) {
'''
F = '''		for (p = 0; p < ppb; p++) {
			memcpy(xb.dump + (dst * ppb + p)'''
NOU1 = (U1, '			if (blk < blocks) {\n')
NOU2 = (U2, '		if (dst != blk && !addRemapP(dst, dst, 0, blk, blocks))\n')
AX1 = [
    ('etop', [NOU1, NOU2, (ELSE, ELSE + UN)]),
    ('eend', [NOU1, NOU2, (E2, '''					dst = blk;
				}
			}
''' + UN + '''		}
		if (blk == 0) {''')]),
    ('a4', [NOU1, NOU2, (A4, UN + A4)]),
    ('a4i', [NOU1, NOU2, (A4, A4 + UN)]),
    ('a4e', [NOU1, NOU2, (BAR, '			dst = blk;\n' + UN)]),
    ('u1z', [NOU2, (Z, UN + Z)]),
    ('u1e', [NOU2, (ELSE, ELSE + UN)]),
    ('u1f', [NOU2, (F, UN + F)]),
    ('s1', [NOU2]),
    ('s2', [NOU1]),
    ('s3', [NOU1, NOU2, (Z, UN + Z)]),
    ('s4', [NOU1, NOU2, (F, UN + F)]),
    ('k', []),
]
AX2 = [('bar', []), ('nobar', [(BAR, '			dst = blk;\n')])]
AX3 = [('g', []), ('ng', [('''			if (blk < blocks) {
				log_printf(1, "ECD error at block 0x%x (raw offset 0x%x), block will be remapped\\n", blk, src - raw);
				if (!addRemapP(blk, blk, blk, -1, blocks))
					return 0;
			}
''', '''			log_printf(1, "ECD error at block 0x%x (raw offset 0x%x), block will be remapped\\n", blk, src - raw);
			if (!addRemapP(blk, blk, blk, -1, blocks))
				return 0;
''')])]
AXES = [AX1, AX2, AX3]
