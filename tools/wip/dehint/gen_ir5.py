"""findAnchor: early returns predict paths as unlikely (lowering v0's spill cost below ok0's);
try a single exit, and else arms, with HEAD's two asms kept."""
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
'''
S1 = '''log_printf(1, "anchor block v %d at 0x2fec000 is selected\\n", v1);
		memcpy(anchor, xb.dump + 0x2fec000, 0x200);
'''
D = '	uint32_t ok0, ok1;\n'
RET = D + '	int ret = 0;\n'
SEL = '''	int sel = -1;
'''
SH = {
    'ret_nest': f'if (ok0) {{\nif (ok1 && v0 < v1) {{\n{S1}\n}} else {{\n{S0}\n}}\nret = 1;\n}} else if (ok1) {{\n{S1}\nret = 1;\n}}\nreturn ret;\n',
    'ret_nest2': f'if (ok0) {{\nif (ok1 && v0 < v1) {{\n{S1}\nret = 1;\n}} else {{\n{S0}\nret = 1;\n}}\n}} else if (ok1) {{\n{S1}\nret = 1;\n}}\nreturn ret;\n',
    'ret_two': f'if (ok0 && (!ok1 || v0 >= v1)) {{\n{S0}\nret = 1;\n}} else if (ok1) {{\n{S1}\nret = 1;\n}}\nreturn ret;\n',
    'ret_two2': f'if (ok0 && (!ok1 || v0 >= v1)) {{\n{S0}\nreturn 1;\n}} else if (ok1) {{\n{S1}\nret = 1;\n}}\nreturn ret;\n',
    'ret_nestg': f'if (ok0) {{\nif (ok1) {{\nif (v0 < v1) {{\n{S1}\n}} else {{\n{S0}\n}}\n}} else {{\n{S0}\n}}\nret = 1;\n}} else if (ok1) {{\n{S1}\nret = 1;\n}}\nreturn ret;\n',
    'ret_ge': f'if (ok0) {{\nif (!ok1 || v0 >= v1) {{\n{S0}\n}} else {{\n{S1}\n}}\nret = 1;\n}} else if (ok1) {{\n{S1}\nret = 1;\n}}\nreturn ret;\n',
    'ret_gen': f'if (ok0) {{\nif (ok1) {{\nif (v0 >= v1) {{\n{S0}\n}} else {{\n{S1}\n}}\n}} else {{\n{S0}\n}}\nreturn 1;\n}} else if (ok1) {{\n{S1}\nreturn 1;\n}}\nreturn 0;\n',
    'ret_else': f'if (ok0) {{\nif (ok1 && v0 < v1) {{\n{S1}\n}} else {{\n{S0}\n}}\nreturn 1;\n}}\nif (ok1) {{\n{S1}\nreturn 1;\n}}\nreturn 0;\n',
    'ret_else2': f'if (!ok0) {{\nif (ok1) {{\n{S1}\nreturn 1;\n}}\nreturn 0;\n}}\nif (ok1 && v0 < v1) {{\n{S1}\n}} else {{\n{S0}\n}}\nreturn 1;\n',
    'ret_else3': f'if (ok0) {{\nif (ok1 && v0 < v1) {{\n{S1}\nreturn 1;\n}} else {{\n{S0}\nreturn 1;\n}}\n}} else if (ok1) {{\n{S1}\nreturn 1;\n}} else\nreturn 0;\n',
}
AXES = [[(k, [(OLD, v), (D, RET)]) for k, v in SH.items()]]
