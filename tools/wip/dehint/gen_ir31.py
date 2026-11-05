"""findAnchor: as gen_ir29, also spell the ok1 logging test (J): dom3's thread leaves bb10 with 0%, because of
P(J) against the later tests' probabilities."""
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
		return 1;
'''
S1 = '''log_printf(1, "anchor block v %d at 0x2fec000 is selected\\n", v1);
		memcpy(anchor, xb.dump + 0x2fec000, 0x200);
		return 1;
'''
E = '__builtin_expect(ok0, 1)'
FIRST = {
    'and': 'if (%s && (!ok1 || v0 >= v1)) {\n%s}\n' % (E, S0),
    'and2': 'if (%s && (v0 >= v1 || !ok1)) {\n%s}\n' % (E, S0),
    'and3': 'if (%s && !(ok1 && v0 < v1)) {\n%s}\n' % (E, S0),
    'and4': 'if (%s && !(v0 < v1 && ok1)) {\n%s}\n' % (E, S0),
    'gt': 'if (%s && (ok1 <= 0 || v0 >= v1)) {\n%s}\n' % (E, S0),
    'nest': 'if (%s) {\nif (!ok1 || v0 >= v1) {\n%s}\n}\n' % (E, S0),
    'esc': 'if (%s) {\nif (ok1) {\nif (v0 >= v1) {\n%s}\n} else {\n%s}\n}\n' % (E, S0, S0),
}
SECOND = {
    'if': 'if (ok1) {\n%s}\nreturn 0;\n' % S1,
    'gt': 'if (ok1 > 0) {\n%s}\nreturn 0;\n' % S1,
    'rev': 'if (!ok1)\nreturn 0;\n%s' % S1,
}
J = '''	if (ok1)
		log_printf(1, "anchor block v %d at 0x2fec000 is valid\\n", v1);
	else {
		log_printf(1, "anchor block at 0x2fec000 is invalid\\n");
		__asm__("");	/* dom3 doesn't thread this copy: one log, ok0 tested after it */
	}
'''
JS = {
    'j': J,
    'jgt': J.replace('if (ok1)', 'if (ok1 > 0)'),
    'jr': '''	if (!ok1) {
		log_printf(1, "anchor block at 0x2fec000 is invalid\\n");
		__asm__("");
	} else
		log_printf(1, "anchor block v %d at 0x2fec000 is valid\\n", v1);
''',
    'jr2': '''	if (ok1 <= 0) {
		log_printf(1, "anchor block at 0x2fec000 is invalid\\n");
		__asm__("");
	} else
		log_printf(1, "anchor block v %d at 0x2fec000 is valid\\n", v1);
''',
}
AX1 = [(a + '.' + b, [(OLD, FIRST[a] + SECOND[b])]) for a in FIRST for b in SECOND]
AX2 = [(k, [(J, v)] if v != J else []) for k, v in JS.items()]
AX3 = [('i', [('	uint32_t ok0, ok1;\n', '	uint32_t ok0;\n	int ok1;\n')])]
AXES = [AX1, AX2, AX3]
