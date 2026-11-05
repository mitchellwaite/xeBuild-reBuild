"""parseDump: one unreachable, no barrier (gen_ir41 z: only `cmp [esp+2c],ebp` vs `cmp ebp,[esp+2c]` left).  Where the unreachable goes and
how the last test is spelled."""
FOCUS = ['_parseDump']
BASE = 'tools/wip/dehint/drafts/image_read_attempt2.c'
U1 = '''			if (blk >= blocks)
				__builtin_unreachable();
			if (blk < blocks) {
'''
U2 = '''		if (blk >= blocks)
			__builtin_unreachable();
		if (dst != blk && !addRemapP(dst, dst, 0, blk, blocks))
			return 0;
'''
Z = '''		if (blk == 0) {
			if (!notZeropair()) {'''
F = '''		for (p = 0; p < ppb; p++) {
			memcpy(xb.dump + (dst * ppb + p)'''
UN = '''		if (blk >= blocks)
			__builtin_unreachable();
'''
BAR = '''			__asm__("");
			dst = blk;
'''
TESTS = {
    'and': 'if (dst != blk && !addRemapP(dst, dst, 0, blk, blocks))\n return 0;\n',
    'rand': 'if (blk != dst && !addRemapP(dst, dst, 0, blk, blocks))\n return 0;\n',
    'nest': 'if (dst != blk) {\nif (!addRemapP(dst, dst, 0, blk, blocks))\nreturn 0;\n}\n',
    'nest2': 'if (dst != blk) {\nint ok = addRemapP(dst, dst, 0, blk, blocks);\nif (!ok)\nreturn 0;\n}\n',
    'eq': 'if (dst == blk)\ncontinue;\nif (!addRemapP(dst, dst, 0, blk, blocks))\nreturn 0;\n',
    'eqg': 'if (dst == blk)\ngoto next;\nif (!addRemapP(dst, dst, 0, blk, blocks))\nreturn 0;\n',
}
POS = {
    'z': lambda t: [(Z, UN + Z), (U2, t)],
    'f': lambda t: [(F, UN + F), (U2, t)],
    'zf': lambda t: [(Z, UN + Z), (F, UN + F), (U2, t)],
    'u2': lambda t: [(U2, UN + t)],
}
AX1 = [(p + '.' + k, [(U1, '			if (blk < blocks) {\n')] + POS[p](v)) for p in POS for k, v in TESTS.items()]
AX2 = [('', [(BAR, '			dst = blk;\n')])]
AX3 = [('d', []), ('n', [('	int blk, dst, p, b2;\n', '	int dst, blk, p, b2;\n')])]
AXES = [AX1, AX2, AX3]
