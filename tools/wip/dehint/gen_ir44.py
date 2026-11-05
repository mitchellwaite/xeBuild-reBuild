"""parseDump, s3+nobar (one unreachable, no barrier): the last test compares `blk_24 != dst_185`, 2 lines off.  n has a late name (ch), so a test
against n prints dst first: `dst != n`."""
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
T = {
    'blk': '		if (dst != blk && !addRemapP(dst, dst, 0, blk, blocks))\n',
    'n': '		if (dst != n && !addRemapP(dst, dst, 0, blk, blocks))\n',
    'n2': '		if ((uint32_t)dst != n && !addRemapP(dst, dst, 0, blk, blocks))\n',
    'nf': '		if (n != dst && !addRemapP(dst, dst, 0, blk, blocks))\n',
    'nn': '		if (dst != n) {\n if (!addRemapP(dst, dst, 0, blk, blocks))\n return 0;\n}\n if (0)\n',
}
AX0 = [('', [(U1, '			if (blk < blocks) {\n'), (Z, UN + Z), (BAR, '			dst = blk;\n')])]
AX1 = [(k, [(U2, v)]) for k, v in T.items()]
AX2 = [('g', []), ('ng', [('''			if (blk < blocks) {
				log_printf(1, "ECD error at block 0x%x (raw offset 0x%x), block will be remapped\\n", blk, src - raw);
				if (!addRemapP(blk, blk, blk, -1, blocks))
					return 0;
			}
''', '''			log_printf(1, "ECD error at block 0x%x (raw offset 0x%x), block will be remapped\\n", blk, src - raw);
			if (!addRemapP(blk, blk, blk, -1, blocks))
				return 0;
''')])]
AXES = [AX0, AX1, AX2]
