"""parseDump: blk a real statement in the body so ch doesn't rename it, signed for VRP1: counter from 1,
blk = n - 1 (does VRP fold blk < blocks from n <= blocks?)."""
FOCUS = ['_parseDump']
BASE = 'build/ir/gen_ir24_best.c'
LOOP0 = '''	for (n = 0; (int)n < blocks; n++) {
		blk = n;
		src = raw + blk * 528 * ppb;
'''
AX1 = [
    ('n1', [(LOOP0, '''	for (n = 1; n <= blocks; n++) {
		blk = n - 1;
		src = raw + blk * 528 * ppb;
''')]),
    ('m1', [(LOOP0, '''	for (m = 0; m < blocks; m++) {
		blk = blocks - 1 - m;
		src = raw + blk * 528 * ppb;
''')]),
]
AX2 = [('s', [('uint32_t n;', 'int n, m;')])]
AX3 = [('z', []), ('z1', [('if (blk == 0) {', 'if (n == 1) {')])]
AXES = [AX1, AX2, AX3]
