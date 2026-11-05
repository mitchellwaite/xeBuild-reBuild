"""parseDump do-while with an exit test on blk itself (IV base 0): guess-loop-iv-compare then gives
`blk == 0` its 0% as in the for loop (expr_coherent_p of the IV bases), so spareLbaOk stays out."""
FOCUS = ['_parseDump']
BASE = 'build/ir/gen_ir24_best.c'
LOOP0 = '''	for (n = 0; (int)n < blocks; n++) {
		blk = n;
		src = raw + blk * 528 * ppb;
'''
END = '''next:
		;
	}
	log_printf(1, "done!\\n");
'''
HEAD = [
    ('gt', '''	blk = 0;
	if (blocks > 0) do {
		src = raw + blk * 528 * ppb;
'''),
    ('ne', '''	blk = 0;
	if (blocks) do {
		src = raw + blk * 528 * ppb;
'''),
]
TAIL = [
    ('pp<', '''next:
		;
	} while (blk++ < blocks - 1);
	log_printf(1, "done!\\n");
'''),
    ('pp!=', '''next:
		;
	} while (blk++ != blocks - 1);
	log_printf(1, "done!\\n");
'''),
    ('lastv', '''next:
		;
	} while (blk++ < last);
	log_printf(1, "done!\\n");
'''),
]
AX1 = [(h[0], [(LOOP0, h[1])]) for h in HEAD]
AX2 = [(t[0], [(END, t[1])]) for t in TAIL]
AX3 = [('', [('int blk, dst, p, b2;', 'int blk, dst, p, b2, last = blocks - 1;')])]
AX4 = [('', []), ('nohot', [('rem: __attribute__((hot));\n', '')])]
AXES = [AX1, AX2, AX3, AX4]
