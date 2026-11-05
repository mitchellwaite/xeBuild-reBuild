"""patchBlsBlmod without no-early-inlining: forms of findFile itself (its copies decide which SSA names survive)."""
OLD = '''	int i;

	for (i = 0; i < xb.nFiles; i++)
		if (xb.files[i].type == type)
			return i;
	return 0;
'''
FORMS = {
    'r': '''	int i, r = 0;

	for (i = 0; i < xb.nFiles; i++)
		if (xb.files[i].type == type)
			return i;
	return r;
''',
    'break': '''	int i;

	for (i = 0; i < xb.nFiles; i++)
		if (xb.files[i].type == type)
			break;
	if (i < xb.nFiles)
		return i;
	return 0;
''',
    'break2': '''	int i, r = 0;

	for (i = 0; i < xb.nFiles; i++)
		if (xb.files[i].type == type) {
			r = i;
			break;
		}
	return r;
''',
    'scope': '''	for (int i = 0; i < xb.nFiles; i++)
		if (xb.files[i].type == type)
			return i;
	return 0;
''',
    'brace': '''	int i;

	for (i = 0; i < xb.nFiles; i++) {
		if (xb.files[i].type == type)
			return i;
	}
	return 0;
''',
    'while': '''	int i = 0;

	while (i < xb.nFiles) {
		if (xb.files[i].type == type)
			return i;
		i++;
	}
	return 0;
''',
    'ne': '''	int i;

	for (i = 0; i < xb.nFiles; i++) {
		if (xb.files[i].type != type)
			continue;
		return i;
	}
	return 0;
''',
    'ptr': '''	int i;
	struct fileent *e = xb.files;

	for (i = 0; i < xb.nFiles; i++, e++)
		if (e->type == type)
			return i;
	return 0;
''',
    'ptr2': '''	int i;

	for (i = 0; i < xb.nFiles; i++) {
		struct fileent *e = &xb.files[i];

		if (e->type == type)
			return i;
	}
	return 0;
''',
    'uint': '''	uint32_t i;

	for (i = 0; i < xb.nFiles; i++)
		if (xb.files[i].type == type)
			return i;
	return 0;
''',
    'last': '''	int i;

	i = 0;
	for (; i < xb.nFiles; i++)
		if (xb.files[i].type == type)
			return i;
	i = 0;
	return i;
''',
}


def CASES(base):
    out = []

    def mk(new):
        def f(t):
            a = t.index('int findFile(int type)\n{')
            b = t.index(OLD, a)
            return t[:b] + new + t[b + len(OLD):]
        return f
    for off in ('', 'nei_blmod'):
        for k, v in FORMS.items():
            out.append((off, k, mk(v)))
    return out
