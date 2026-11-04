"""parseDump after the signed loop: drop cb/b2/ablock, the dead `blk < blocks`, and try the real
addRemap's types.  BASE = build/ir/p1.c made from gen_ir11 signed+u1+u2+b+c+p."""
FOCUS = ['_parseDump']
BASE = 'build/ir/p1.c'
AX1 = [
    ('', [('int blk, dst, p, b2;', 'int blk, dst, p;'),
          ('''			b2 = blk;
			if (!addRemapP(b2, blk, 0, dst, blocks))''', '''			if (!addRemapP(blk, blk, 0, dst, blocks))''')]),
]
AX2 = [
    ('', [('''			if (blk < blocks) {
				log_printf(1, "ECD error at block 0x%x (raw offset 0x%x), block will be remapped\\n", blk, src - raw);
				if (!addRemapP(blk, blk, blk, -1, blocks))
					return 0;
			}
''', '''			log_printf(1, "ECD error at block 0x%x (raw offset 0x%x), block will be remapped\\n", blk, src - raw);
			if (!addRemapP(blk, blk, blk, -1, blocks))
				return 0;
''')]),
]
AX3 = [('dne', []), ('nedb', [('if (dst != blk) {', 'if (blk != dst) {'),
                              ('if (dst != blk &&', 'if (blk != dst &&')])]
AX4 = [('', []),
       ('d1', [('int blk, dst, p;', 'int dst, blk, p;')]),
       ('d2', [('int blk, dst, p;', 'int p, dst, blk;')])]
LOOP = '''	for (blk = 0; blk < blocks; blk++) {
		src = raw + blk * 528 * ppb;
'''
AX5 = [('', []),
       ('wh', [(LOOP, '''	blk = 0;
	while (blk < blocks) {
		src = raw + blk * 528 * ppb;
''')]),
       ]
AXES = [AX1, AX2, AX3, AX4]
