"""parseDump: ch copies the for loop's header, so blk gets a late SSA name and compares print dst
first.  Loop forms that aren't copied (continue stays: it goes to the do-while's test)."""
FOCUS = ['_parseDump']
BASE = 'build/ir/gen_ir12_best.c'
LOOP = '''	for (blk = 0; blk < blocks; blk++) {
		src = raw + blk * 528 * ppb;
'''
END = '''next:
		;
	}
	log_printf(1, "done!\\n");
'''
AX1 = [
    ('dowhile', [(LOOP, '''	blk = 0;
	if (blocks > 0) do {
		src = raw + blk * 528 * ppb;
'''), (END, '''next:
		;
	} while (++blk < blocks);
	log_printf(1, "done!\\n");
''')]),
    ('dowhile2', [(LOOP, '''	if (blocks) {
	blk = 0;
	do {
		src = raw + blk * 528 * ppb;
'''), (END, '''next:
		;
	} while (++blk < blocks);
	}
	log_printf(1, "done!\\n");
''')]),
    ('dowhile3', [(LOOP, '''	if (blocks) {
	blk = 0;
	do {
		src = raw + blk * 528 * ppb;
'''), (END, '''next:
		;
	} while (++blk != blocks);
	}
	log_printf(1, "done!\\n");
''')]),
    ('copy', [(LOOP, '''	for (n = 0; n < blocks; n++) {
		blk = n;
		src = raw + blk * 528 * ppb;
'''), ('int blk, dst, p;', 'int n, blk, dst, p;')]),
]
AXES = [AX1]
