"""lab_none (attempt 8): loadConsoleBlFiles' precheck as a plain early return instead of `goto none` to a cold label.
The reference lays the r = 1 block [14] before the shrink-wrapped return 0 [20 with a plain for]."""
HEAD = '''	/* the cold label gives the shrink-wrapped return 0 frequency 0, so
	   bb-reorder lays it out last */
	if ((uint32_t)xb.nFiles <= 1)
		goto none;
'''
TAIL = '''	return 0;
none: __attribute__((cold));
	return 0;
}'''
F = {
    'ret': '	if ((uint32_t)xb.nFiles <= 1)\n		return 0;\n',
    'ret2': '	if (xb.nFiles < 2)\n		return 0;\n',
    'ret3': '	if (xb.nFiles <= 1)\n		return 0;\n',
    'none': '',
    'log': '	if ((uint32_t)xb.nFiles <= 1)\n		return 0;\n',
}
TAILS = {
    'plain': '	return 0;\n}',
    'goto': '	return 0;\nnone:\n	return 0;\n}',
}


def CASES(base):
    if HEAD not in base or TAIL not in base:
        raise ValueError('text')
    out = []
    for k, v in F.items():
        out.append((k, base.replace(HEAD, v).replace(TAIL, TAILS['plain'])))
    out.append(('gotonone', base.replace(TAIL, TAILS['goto'])))
    return out


FOCUS = ['_loadConsoleBlFiles']
