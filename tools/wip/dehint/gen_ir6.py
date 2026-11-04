"""findAnchor: nest shape with one expect on a single ok0/ok1 test."""
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
E0 = '__builtin_expect(ok0, 1)'
E1 = '__builtin_expect(ok1, 1)'
SH = {
    'test2_ok0': f'if ({E0}) {{\nif (ok1 && v0 < v1) {{\n{S1}\n}}\n{S0}\n}}\nif (ok1) {{\n{S1}\n}}\nreturn 0;\n',
    'test2_ok1a': f'if (ok0) {{\nif ({E1} && v0 < v1) {{\n{S1}\n}}\n{S0}\n}}\nif (ok1) {{\n{S1}\n}}\nreturn 0;\n',
    'test2_ok1b': f'if (ok0) {{\nif (ok1 && v0 < v1) {{\n{S1}\n}}\n{S0}\n}}\nif ({E1}) {{\n{S1}\n}}\nreturn 0;\n',
}
F0 = '	if (ok0)\n		log_printf(1, "anchor block v %d at 0x2fe8000 is valid'
F1 = '	if (ok1)\n		log_printf(1, "anchor block v %d at 0x2fec000 is valid'
NEST = SH['test2_ok0'].replace(E0, 'ok0')
AXES = [[(k, [(OLD, v)]) for k, v in SH.items()] +
        [('first0', [(OLD, NEST), (F0, F0.replace('(ok0)', '(__builtin_expect(ok0, 1))'))]),
         ('first1', [(OLD, NEST), (F1, F1.replace('(ok1)', '(__builtin_expect(ok1, 1))'))])]]
