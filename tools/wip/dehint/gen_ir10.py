"""detectController: drop pin_found and/or pin_lo2, keeping pin_lo."""
FOCUS = ['_detectController']
BASE = 'tools/wip/dehint/drafts/image_read_attempt1.c'
D = '''	int i, n;
	uint32_t found;
'''
A = '''		n = size / 16896;
		log_printf(1, "\\tNAND dump is from a small block machine\\n");
		xb.dumpBigBlock = 0;
		xb.muChecked = 1;
		found = 0;
		/* code-free hints: found in eax outside the loop (one head-merged xor
		   for both found = 0 edges), i in ebx */
		if (n > 1)
			__asm__("" : "+a"(found));
'''
B = '''		n = size / 16896;
		log_printf(1, "\\tNAND dump is from a small block machine\\n");
		%s
		xb.dumpBigBlock = 0;
		%s
		xb.muChecked = 1;
		%s
'''
L2 = '''				int lo2 = b[512];

				/* lo kept live past its add, so the sum takes hi's
				   register (ebp) */
				__asm__("" : : "a"(lo));
				if (lo2 + (b[513] & 0xf) * 256 == i) {
					__asm__("" : : "d"(lo2));
'''
P = '''				__asm__("" : : "a"(lo));
'''
AX1 = [('keepf', [])]
for k, t in (('u', ['found = 0;', '', '']), ('v', ['', 'found = 0;', '']), ('w', ['', '', 'found = 0;'])):
    AX1.append(('f' + k, [(A, B % tuple(t))]))
    AX1.append(('g' + k, [(A, B % tuple(t) + '		if (n <= 1)\n			return found;\n')]))
AX1.append(('ret0', [(A, B % ('', '', 'found = 0;') + '		if (n <= 1)\n			return 0;\n')]))
AX2 = [('keepl', []),
       ('l1', [(L2, '''				int lo2 = b[512];

'''+P+'''				if (lo2 + (b[513] & 0xf) * 256 == i) {
''')]),
       ('l2', [(L2, P + '''				if (b[512] + (b[513] & 0xf) * 256 == i) {
''')]),
       ('l3', [(L2, '''				uint8_t lo2 = b[512];

'''+P+'''				if (lo2 + (b[513] & 0xf) * 256 == i) {
''')]),
       ('l4', [(L2, P + '''				if ((b[513] & 0xf) * 256 + b[512] == i) {
''')]),
       ('l5', [(L2, '''				int hi2 = (b[513] & 0xf) * 256;

'''+P+'''				if (hi2 + b[512] == i) {
''')]),
       ('l6', [(L2, '''				int hi2 = (b[513] & 0xf) * 256;

'''+P+'''				if (b[512] + hi2 == i) {
''')]),
       ('l7', [(L2, '''				int lo2 = b[512], hi2 = (b[513] & 0xf) * 256;

'''+P+'''				if (lo2 + hi2 == i) {
''')]),
       ('l8', [(L2, '''				uint32_t lo2 = b[512];

'''+P+'''				if (lo2 + (b[513] & 0xf) * 256 == i) {
''')]),
       ]
AX3 = [('', []), ('fi', [(D, '	int i, n;\n	int found;\n')])]
AXES = [AX1, AX2, AX3]
