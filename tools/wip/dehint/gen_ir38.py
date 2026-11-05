"""findAnchor: source order that expands ec valid, ec selected, ec invalid, e8 selected, so lit_anchor can go, with the barrier kept
and expects in any combination.  Spellings of the selection inside `if (ok1)`."""
FOCUS = ['_findAnchor']
LIT = '''		/* code-free: emits these two (threaded copies, expanded last) in the original's order */
		__asm__("" : : "i"("anchor block v %d at 0x2fec000 is valid\\n"), "i"("anchor block v %d at 0x2fec000 is selected\\n"));
'''
OLD = '''	if (ok1)
		log_printf(1, "anchor block v %d at 0x2fec000 is valid\\n", v1);
	else {
		log_printf(1, "anchor block at 0x2fec000 is invalid\\n");
		__asm__("");	/* dom3 doesn't thread this copy: one log, ok0 tested after it */
	}
	if (__builtin_expect(ok0, 1) && (__builtin_expect(!ok1, 1) || v0 >= v1)) {
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
VAL = 'log_printf(1, "anchor block v %d at 0x2fec000 is valid\\n", v1);\n'
INV = 'log_printf(1, "anchor block at 0x2fec000 is invalid\\n");\n'
S0 = '''log_printf(1, "anchor block v %d at 0x2fe8000 is selected\\n", v0);
memcpy(anchor, xb.dump + 0x2fe8000, 0x200);
return 1;
'''
S1 = '''log_printf(1, "anchor block v %d at 0x2fec000 is selected\\n", v1);
memcpy(anchor, xb.dump + 0x2fec000, 0x200);
return 1;
'''
BAR = '__asm__("");\n'
V = []
for en, e0 in (('e0', 'ok0'), ('e1', '__builtin_expect(ok0, 1)')):
    for bn, b in (('b', BAR), ('n', '')):
        V.append((f'or.{en}.{bn}', f'if (ok1) {{\n{VAL}if (!{e0} || v0 < v1) {{\n{S1}}}\n}} else {{\n{INV}{b}}}\nif ({e0}) {{\n{S0}}}\nreturn 0;\n'))
        V.append((f'or2.{en}.{bn}', f'if (ok1) {{\n{VAL}if (!{e0}) {{\n{S1}}}\nif (v0 < v1) {{\n{S1}}}\n}} else {{\n{INV}{b}}}\nif ({e0}) {{\n{S0}}}\nreturn 0;\n'))
        V.append((f'or3.{en}.{bn}', f'if (ok1) {{\n{VAL}if ({e0} && v0 >= v1) {{\n}} else {{\n{S1}}}\n}} else {{\n{INV}{b}}}\nif ({e0}) {{\n{S0}}}\nreturn 0;\n'))
        V.append((f'or4.{en}.{bn}', f'if (ok1) {{\n{VAL}if (v0 < v1 || !{e0}) {{\n{S1}}}\n}} else {{\n{INV}{b}}}\nif (!{e0})\nreturn 0;\n{S0}'))
AXES = [[('', [(LIT, '')])], [(k, [(OLD, v)]) for k, v in V]]
