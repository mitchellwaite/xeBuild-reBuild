"""parseDump do-while: blk keeps a low SSA name (no ch).  Look at what breaks."""
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
AX1 = [
    ('dw', [(LOOP0, '''	blk = 0;
	if (blocks > 0) do {
		src = raw + blk * 528 * ppb;
'''), (END, '''next:
		;
	} while (++blk < blocks);
	log_printf(1, "done!\\n");
''')]),
    ('dw2', [(LOOP0, '''	if (blocks > 0) {
	blk = 0;
	do {
		src = raw + blk * 528 * ppb;
'''), (END, '''next:
		;
		blk++;
	} while (blk < blocks);
	}
	log_printf(1, "done!\\n");
''')]),
    ('dw3', [(LOOP0, '''	blk = 0;
	if (blocks) do {
		src = raw + blk * 528 * ppb;
'''), (END, '''next:
		;
	} while (++blk != blocks);
	log_printf(1, "done!\\n");
''')]),
]
AX2 = [('', []), ('nohot', [('rem: __attribute__((hot));\n', '')])]
AXES = [AX1, AX2]
