"""exp_upd: 23 stays out of the bit test only while it shares a test with the next type, and that test has to be under 23.8% taken.  Forms of isUpdateBl's return that change the group's predictors
(early return at 39% now), in the original order."""
OLD = 'return __builtin_expect(type == 23 || type == 15, 0) || type == 16 || type == 9 || type == 10 || type == 24 || type == 25;'
EQ = 'type == 23 || type == 15 || type == 16 || type == 9 || type == 10 || type == 24 || type == 25'
NE = 'type != 23 && type != 15 && type != 16 && type != 9 && type != 10 && type != 24 && type != 25'
F = {
    'if1': 'if (' + EQ + ')\n		return 1;\n	return 0;',
    'if0': 'if (' + NE + ')\n		return 0;\n	return 1;',
    'not': 'return !(' + NE + ');',
    'r0': 'int r = 0;\n\n	if (' + EQ + ')\n		r = 1;\n	return r;',
    'r1': 'int r = 1;\n\n	if (' + NE + ')\n		r = 0;\n	return r;',
    'tern': 'return ' + EQ + ' ? 1 : 0;',
    'else': 'if (' + EQ + ')\n		return 1;\n	else\n		return 0;',
    'nest': 'if (type == 23 || type == 15)\n		return 1;\n	if (type == 16 || type == 9)\n		return 1;\n	if (type == 10 || type == 24)\n		return 1;\n	return type == 25;',
    'nest2': 'if (type == 23 || type == 15)\n		return 1;\n	return type == 16 || type == 9 || type == 10 || type == 24 || type == 25;',
    'nest3': 'if (type == 23 || type == 15)\n		return 1;\n	if (type == 16 || type == 9 || type == 10 || type == 24 || type == 25)\n		return 1;\n	return 0;',
    'nz': 'return (type == 23) | (type == 15) | (type == 16) | (type == 9) | (type == 10) | (type == 24) | (type == 25);',
    'bits': 'return type <= 25 && (0x3818600 >> type & 1);',
    'bits2': 'if (type > 25)\n		return 0;\n	return 0x3818600 >> type & 1;',
    'bits3': 'return (uint32_t)type <= 25 && (1 << type & 0x3818600) != 0;',
}


def CASES(base):
    return [(k, base.replace(OLD, v)) for k, v in F.items()]


FOCUS = ['_addUpdateBls', '_isUpdateBl']
