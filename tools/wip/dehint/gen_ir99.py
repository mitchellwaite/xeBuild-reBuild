"""detectController without pin_found: where `found` is set and how it is returned, its type, a guard around the loop; `xor eax,eax` in the reference is before `cmp edi,1`.
Linux build: same xor before cmp, found in eax."""
FOCUS = ['_detectController']
D = '''	int i, n;
	uint32_t found;
'''
A = '''		log_printf(1, "\\tNAND dump is from a small block machine\\n");
		xb.dumpBigBlock = 0;
		xb.muChecked = 1;
		found = 0;
		/* code-free hints: found in eax outside the loop (one head-merged xor
		   for both found = 0 edges), i in ebx */
		if (n > 1)
			__asm__("" : "+a"(found));
		for (i = 1; i < n; i++) {
'''
R = '''		return found;
	}
	log_printf(0, "***** WARNING: NAND dump does not appear'''
LOG = '''		log_printf(1, "\\tNAND dump is from a small block machine\\n");
		xb.dumpBigBlock = 0;
		xb.muChecked = 1;
'''
FOR = '		for (i = 1; i < n; i++) {\n'
TY = [('u', []), ('i', [(D, '	int i, n;\n	int found;\n')]), ('l', [(D, '	int i, n;\n	unsigned long found;\n')])]
PL = [
    ('a', [(A, LOG + '		found = 0;\n' + FOR)]),
    ('b', [(A, '		found = 0;\n' + LOG + FOR)]),
    ('c', [(A, LOG + '		for (found = 0, i = 1; i < n; i++) {\n')]),
    ('d', [(A, LOG + '		found = 0;\n		i = 1;\n		while (i < n) {\n')]),
    ('e', [(A, LOG + '		if (n <= 1)\n			return 0;\n		found = 0;\n' + FOR)]),
    ('f', [(A, '		n = size / 16896;\n' + LOG.replace('', '', 0) + '		found = 0;\n' + FOR)]),
]
AXES = [TY, PL[:3] + PL[4:5]]
