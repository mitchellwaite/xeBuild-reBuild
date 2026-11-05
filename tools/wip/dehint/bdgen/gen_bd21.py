# The 0x60 copies: two copies of the default-copy code, one for "load failed" and one for
# "wrong size".  RTL crossjump merges them and drops the rep_mov's MEM_EXPR (merge_memattrs),
# so sched2 sees a dependence with the size store.  No pin, no assume_aligned.
REMOVE = ['pin_p60', 'aa_60', 'pin_p', 'aa_p']
OLD60 = '''	if (loadBaseFile(e->name, e) || e->size != 0x60) {
		e->data = malloc(0x60);
		if (!e->data)
			return 1;
		{
		uint8_t *p = e->data;

		e->size = 0x60;
		memcpy(p, defBl60, 0x60);
		}
	}
	return 0;
'''
COPY = '''		e->data = malloc(0x60);
		if (!e->data)
			return 1;
		e->size = 0x60;
		memcpy(e->data, defBl60, 0x60);
'''
A60 = [
    ('a0', [(OLD60, '''	if (loadBaseFile(e->name, e)) {
''' + COPY + '''	} else if (e->size != 0x60) {
''' + COPY + '''	}
	return 0;
''')]),
    ('a1', [(OLD60, '''	if (!loadBaseFile(e->name, e)) {
		if (e->size != 0x60) {
''' + COPY.replace('\t\t', '\t\t\t') + '''		}
	} else {
''' + COPY + '''	}
	return 0;
''')]),
    ('a2', [(OLD60, '''	if (!loadBaseFile(e->name, e)) {
		if (e->size == 0x60)
			return 0;
''' + COPY + '''		return 0;
	}
''' + COPY + '''	return 0;
''')]),
]
OLDC = '''				if (!xb.glitch2mfg || (!loadBaseFile(e->name, e) && e->size == 0x60))
					break;
				e->data = malloc(0x60);
				if (!e->data) {
					r = 1;
					break;
				}
				{
					uint8_t *p = e->data;

					/* p's points-to unknown: the size store may alias the
					   copy, so sched2 keeps it before the rep movsd setup */
					e->size = 0x60;
					memcpy(p, defBl60, 0x60);
				}
				break;
'''
CC ='''e->data = malloc(0x60);
if (!e->data) {
	r = 1;
	break;
}
e->size = 0x60;
memcpy(e->data, defBl60, 0x60);
'''


def ind(s, n):
    return ''.join('\t' * n + l + '\n' for l in s.splitlines())


AC = [
    ('c0', [(OLDC, '''				if (!xb.glitch2mfg)
					break;
				if (loadBaseFile(e->name, e)) {
''' + ind(CC, 5) + '''				} else if (e->size != 0x60) {
''' + ind(CC, 5) + '''				}
				break;
''')]),
    ('c1', [(OLDC, '''				if (xb.glitch2mfg) {
					if (!loadBaseFile(e->name, e)) {
						if (e->size == 0x60)
							break;
''' + ind(CC, 6) + '''					} else {
''' + ind(CC, 6) + '''					}
				}
				break;
''')]),
    ('c2', [(OLDC, '''				if (!xb.glitch2mfg)
					break;
				if (!loadBaseFile(e->name, e)) {
					if (e->size == 0x60)
						break;
''' + ind(CC, 5) + '''					break;
				}
''' + ind(CC, 4) + '''				break;
''')]),
]
AXES = [A60, AC]
