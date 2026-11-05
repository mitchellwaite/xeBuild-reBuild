"""findAnchor, all 3 expects gone (gen_ir4's nest shape): P(ok0) of the FIRST test above 50% without `> 0`.
A user `goto` is predicted unlikely (PRED_GOTO), which is plain control flow in the invalid arm."""
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
}
F0 = '''	if (ok0)
		log_printf(1, "anchor block v %d at 0x2fe8000 is valid\\n", v0);
	else {
		log_printf(1, "anchor block at 0x2fe8000 is invalid\\n");
		/* code-free: emits these two (threaded copies, expanded last) in the original's order */
		__asm__("" : : "i"("anchor block v %d at 0x2fec000 is valid\\n"), "i"("anchor block v %d at 0x2fec000 is selected\\n"));
	}
'''
AS = '''		/* code-free: emits these two (threaded copies, expanded last) in the original's order */
		__asm__("" : : "i"("anchor block v %d at 0x2fec000 is valid\\n"), "i"("anchor block v %d at 0x2fec000 is selected\\n"));
'''
FS = {
    'k': F0,
    'g1': '''	if (ok0)
		log_printf(1, "anchor block v %d at 0x2fe8000 is valid\\n", v0);
	else {
		log_printf(1, "anchor block at 0x2fe8000 is invalid\\n");
''' + AS + '''		goto second;
	}
second:
''',
    'g2': '''	if (!ok0) {
		log_printf(1, "anchor block at 0x2fe8000 is invalid\\n");
''' + AS + '''		goto second;
	}
	log_printf(1, "anchor block v %d at 0x2fe8000 is valid\\n", v0);
second:
''',
    'g3': '''	if (ok0)
		goto valid;
	log_printf(1, "anchor block at 0x2fe8000 is invalid\\n");
''' + AS + '''	goto second;
valid:
	log_printf(1, "anchor block v %d at 0x2fe8000 is valid\\n", v0);
second:
''',
}
AX0 = [(k, [(F0, v)] if v != F0 else []) for k, v in FS.items()]
AX1 = [(k, [(OLD, v)]) for k, v in SH.items()]
AXES = [AX0, AX1]
