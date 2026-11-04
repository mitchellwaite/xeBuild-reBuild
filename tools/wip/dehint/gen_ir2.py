"""findAnchor: keep HEAD's two asm hints, drop the three expects by the shape of the selection."""
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
T1 = 'if (ok1) {\n' + S1 + '\n}\nreturn 0;\n'
T2 = 'if (!ok1)\nreturn 0;\n' + S1 + '\n'
T3 = 'if (ok1) {\n' + S1 + '\n} else\nreturn 0;\n'
HEADS = {
    'and': 'if (ok0 && (!ok1 || v0 >= v1)) {\n' + S0 + '\n}\n',
    'and2': 'if (ok0 && (v0 >= v1 || !ok1)) {\n' + S0 + '\n}\n',
    'nest': 'if (ok0) {\nif (!ok1 || v0 >= v1) {\n' + S0 + '\n}\n}\n',
    'nest2': 'if (ok0) {\nif (v0 >= v1 || !ok1) {\n' + S0 + '\n}\n}\n',
    'nestn': 'if (ok0) {\nif (ok1) {\nif (v0 >= v1) {\n' + S0 + '\n}\n} else {\n' + S0 + '\n}\n}\n',
    'nesti': 'if (ok0) {\nif (ok1 && v0 < v1) {\n' + S1 + '\n}\n' + S0 + '\n}\n',
    'neg': 'if (!ok0 || (ok1 && v0 < v1)) {\n' + T2 + '} else {\n' + S0 + '\n}\n',
    'neg2': 'if (!ok0 || (ok1 && v0 < v1)) {\n' + T1 + '}\n' + S0 + '\n',
}
AXES = [[(k + '.' + tn, [(OLD, v + t if k not in ('neg', 'neg2') else v + ('return 0;\n' if k == 'neg' and 0 else ''))])
         for k, v in HEADS.items() for tn, t in (('t1', T1), ('t2', T2), ('t3', T3))]]
