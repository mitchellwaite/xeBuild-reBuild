"""findAnchor: exp_ok1 + exp_nok1 go at 7 lines, only bb10's alignment: the threaded `ok1_46 != 0` edge ends at 0%
(update_profile clips it), so bb10's frequency is 0 and compute_alignments skips it.  The reference has 16.9%.
Spellings of the two final tests, exp_ok0 kept."""
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
    'nest': 'if (%s) {\nif (!ok1 || v0 >= v1) {\n%s}\n}\n' % (E, S0),
    'nest2': 'if (%s) {\nif (v0 >= v1 || !ok1) {\n%s}\n}\n' % (E, S0),
    'nest3': 'if (%s) {\nif (ok1 && v0 < v1) {\n} else {\n%s}\n}\n' % (E, S0),
    'nest4': 'if (%s) {\nif (!(ok1 && v0 < v1)) {\n%s}\n}\n' % (E, S0),
    'cnt': 'if (%s && (ok1 == 0 || v0 >= v1)) {\n%s}\n' % (E, S0),
    'nest5': 'if (%s) {\nif (!ok1) {\n%s}\nif (v0 >= v1) {\n%s}\n}\n' % (E, S0, S0),
}
SECOND = {
    'if': 'if (ok1) {\n%s}\nreturn 0;\n' % S1,
    'rev': 'if (!ok1)\nreturn 0;\n%s' % S1,
    'ne': 'if (ok1 != 0) {\n%s}\nreturn 0;\n' % S1,
}
AX1 = [(a + '.' + b, [(OLD, FIRST[a] + SECOND[b])]) for a in FIRST for b in SECOND]
AX2 = [('u', []), ('i', [('	uint32_t ok0, ok1;\n', '	uint32_t ok0;\n	int ok1;\n')])]
AXES = [AX1, AX2]
