"""vol_fail: loadBl's fail block needs to stay a block of its own.  Plain C in place of the empty asm: a pointer test folded after ipa-inline (pr
is &r in the one caller), or the -1 as a helper with a call."""
OLD = '''fail:
	__asm__ __volatile__("");
	*pr = -1;
'''
A = [
    ('pr', [(OLD, 'fail:\n	if (pr)\n		*pr = -1;\n')]),
    ('prn', [(OLD, 'fail:\n	if (pr != NULL)\n		*pr = -1;\n')]),
    ('e', [(OLD, 'fail:\n	if (e)\n		*pr = -1;\n')]),
    ('ret', [(OLD, 'fail:\n	if (!pr)\n		return;\n	*pr = -1;\n')]),
]
AXES = [A]
