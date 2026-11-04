"""findAnchor: nest shape plus `> 0` spellings (opcode-positive predictor on a test that later
folds to != 0): IRA pops v0 before ok0 only if P(ok0) is above even (spill cost v0 7915 vs ok0 10000)."""
FOCUS = ['_findAnchor']
OLD = '''	if (__builtin_expect(ok0, 1) && (__builtin_expect(!ok1, 1) || v0 >= v1)) {
		log_printf(1, "anchor block v %d at 0x2fe8000 is selected\\n", v0);
		memcpy(anchor, xb.dump + 0x2fe8000, 0x200);
		return 1;
	}
	if (__builtin_expect(ok1, 1)) {
		log_printf(1, "anchor block v %d at 0x2fec000 is selected\\n", v1);
		memcpy(anchor, xb.dump + 0x2fec000, 0x200);
		return 1;
	}
	return 0;
'''
S0 = '''log_printf(1, "anchor block v %d at 0x2fe8000 is selected\\n", v0);
		memcpy(anchor, xb.dump + 0x2fe8000, 0x200);
		return 1;'''
S1 = '''log_printf(1, "anchor block v %d at 0x2fec000 is selected\\n", v1);
		memcpy(anchor, xb.dump + 0x2fec000, 0x200);
		return 1;'''
A0, B0 = '@@A@@', '@@B@@'
SH = f'{A0}if (ok1) {{\nif (v0 < v1) {{\n{S1}\n}}\n}}\n{S0}\n}}\n{B0}{S1}\n}}\nreturn 0;\n'
F0 = '	if (ok0)\n		log_printf(1, "anchor block v %d at 0x2fe8000 is valid'
F1 = '	if (ok1)\n		log_printf(1, "anchor block v %d at 0x2fec000 is valid'
R0 = {'o': 'ok0', 'p': 'ok0 > 0', 'g': 'ok0 >= 1', 'e': 'ok0 != 0'}
R1 = {'o': 'ok1', 'p': 'ok1 > 0', 'g': 'ok1 >= 1'}
AX0 = [('f0' + k, [(F0, F0.replace('(ok0)', '(' + v + ')'))]) for k, v in R0.items()]
AX1 = [('f1' + k, [(F1, F1.replace('(ok1)', '(' + v + ')'))]) for k, v in R1.items()]
AX2 = [('a' + k + 'b' + l, [(OLD, SH.replace(A0, 'if (' + v + ') {\n').replace(B0, 'if (' + w + ') {\n'))])
       for k, v in R0.items() for l, w in R1.items()]
AX3 = [('', []), ('int', [('	uint32_t ok0, ok1;\n', '	int ok0, ok1;\n')])]
AXES = [AX0, AX1, AX2, AX3]
