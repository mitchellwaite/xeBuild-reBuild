# loadBl's case 24 with the two conditions written as separate arms, each with its own inlined
# loadBl60: the copies have the same successor, so RTL crossjump merges them (dropping the
# rep_mov's MEM_EXPR) and sched2 keeps the size store first.  Console side: gen_bd21's c0.
REMOVE = ['pin_p60', 'aa_60', 'pin_p', 'aa_p']
OLD60 = '''		e->data = malloc(0x60);
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
NEW60 = '''		e->data = malloc(0x60);
		if (!e->data)
			return 1;
		e->size = 0x60;
		memcpy(e->data, defBl60, 0x60);
	}
	return 0;
'''
OLD24 = '''		if (xb.type == BUILD_JTAG || xb.glitch2mfg)
			*pr = loadBl60(e);
'''
ARMS = [
    ('elseif', [(OLD24, '''		if (xb.type == BUILD_JTAG)
			*pr = loadBl60(e);
		else if (xb.glitch2mfg)
			*pr = loadBl60(e);
''')]),
    ('rev', [(OLD24, '''		if (xb.glitch2mfg)
			*pr = loadBl60(e);
		else if (xb.type == BUILD_JTAG)
			*pr = loadBl60(e);
''')]),
    ('orig', []),
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
CC = '''e->data = malloc(0x60);
if (!e->data) {
	r = 1;
	break;
}
e->size = 0x60;
memcpy(e->data, defBl60, 0x60);
'''


def ind(s, n):
    return ''.join('\t' * n + l + '\n' for l in s.splitlines())


CONS = [('c0', [(OLDC, '''				if (!xb.glitch2mfg)
					break;
				if (loadBaseFile(e->name, e)) {
''' + ind(CC, 5) + '''				} else if (e->size != 0x60) {
''' + ind(CC, 5) + '''				}
				break;
''')])]
AXES = [[('', [(OLD60, NEW60)])], ARMS, CONS]
