"""findAnchor: nesti (gen_ir2) left a v1/ok0 register swap: declarations and shape."""
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
SH = {
    'dup': f'if (ok0) {{\nif (ok1 && v0 < v1) {{\n{S1}\n}}\n{S0}\n}}\nif (ok1) {{\n{S1}\n}}\nreturn 0;\n',
    'nest': f'if (ok0) {{\nif (ok1) {{\nif (v0 < v1) {{\n{S1}\n}}\n}}\n{S0}\n}}\nif (ok1) {{\n{S1}\n}}\nreturn 0;\n',
    'goto': f'if (ok0) {{\nif (ok1 && v0 < v1)\ngoto sel1;\n{S0}\n}}\nif (ok1) {{\nsel1:\n{S1}\n}}\nreturn 0;\n',
    'goton': f'if (ok0) {{\nif (ok1) {{\nif (v0 < v1)\ngoto sel1;\n}}\n{S0}\n}}\nif (ok1) {{\nsel1:\n{S1}\n}}\nreturn 0;\n',
    'ret': f'if (ok0) {{\nif (!ok1 || v0 >= v1) {{\n{S0}\n}}\n}} \nif (ok1) {{\n{S1}\n}}\nreturn 0;\n',
}
D = '	uint32_t v0, v1;\n	uint32_t ok0, ok1;\n'
DS = {
    'd0': D,
    'd1': '	uint32_t ok0, ok1;\n	uint32_t v0, v1;\n',
    'd2': '	uint32_t v0, ok0;\n	uint32_t v1, ok1;\n',
    'd3': '	uint32_t v1, v0;\n	uint32_t ok1, ok0;\n',
    'd4': '	uint32_t ok1, ok0;\n	uint32_t v1, v0;\n',
    'd5': '	uint32_t ok0;\n	uint32_t v1, v0;\n	uint32_t ok1;\n',
    'd6': '	int ok0, ok1;\n	uint32_t v0, v1;\n',
    'd7': '	uint32_t v0, v1;\n	int ok0, ok1;\n',
    'd8': '	int v0, v1;\n	uint32_t ok0, ok1;\n',
}
AXES = [[(k, [(OLD, v)]) for k, v in SH.items()],
        [(k, [(D, v)]) for k, v in DS.items()]]
