"""type == 9/10 fallbacks, the expects in loadConsoleBlFiles and loadBl"""
FOCUS = ['_loadConsoleBlFiles', '_loadBlFiles']
C = '''				if (r) {
					if (__builtin_expect(type == 9, 0)) {
						if (suGetCF(&e->data, &e->size))
							r = 0;
					} else if (type == 10) {
						if (suGetCG(&e->data, &e->size))
							r = 0;
					}
					if (r)
						break;
				}
'''
L = '''		if (*pr) {
			if (type == 9) {
				if (!suGetCF(&e->data, &e->size))
					break;
			} else if (__builtin_expect(type == 10, 0)) {
				if (!suGetCG(&e->data, &e->size))
					break;
				goto chk;
			} else
				break;
		}
'''
A = [
    ('', []),
    ('c0', [(C, C.replace('__builtin_expect(type == 9, 0)', 'type == 9'))]),
    ('c10first', [(C, '''				if (r) {
					if (type == 10) {
						if (suGetCG(&e->data, &e->size))
							r = 0;
					} else if (type == 9) {
						if (suGetCF(&e->data, &e->size))
							r = 0;
					}
					if (r)
						break;
				}
''')]),
    ('csw', [(C, '''				if (r) {
					switch (type) {
					case 9:
						if (suGetCF(&e->data, &e->size))
							r = 0;
						break;
					case 10:
						if (suGetCG(&e->data, &e->size))
							r = 0;
						break;
					}
					if (r)
						break;
				}
''')]),
    ('cand', [(C, '''				if (r) {
					if (type == 9 && suGetCF(&e->data, &e->size))
						r = 0;
					else if (type == 10 && suGetCG(&e->data, &e->size))
						r = 0;
					if (r)
						break;
				}
''')]),
    ('csep', [(C, '''				if (r) {
					if (type == 9) {
						if (suGetCF(&e->data, &e->size))
							r = 0;
					}
					if (type == 10) {
						if (suGetCG(&e->data, &e->size))
							r = 0;
					}
					if (r)
						break;
				}
''')]),
    ('cret', [(C, '''				if (r) {
					int got = 0;

					if (type == 9)
						got = suGetCF(&e->data, &e->size);
					else if (type == 10)
						got = suGetCG(&e->data, &e->size);
					if (!got)
						break;
					r = 0;
				}
''')]),
    ('cne', [(C, '''				if (r) {
					if (type != 9) {
						if (type == 10) {
							if (suGetCG(&e->data, &e->size))
								r = 0;
						}
					} else if (suGetCF(&e->data, &e->size))
						r = 0;
					if (r)
						break;
				}
''')]),
]
B = [
    ('', []),
    ('l0', [(L, L.replace('__builtin_expect(type == 10, 0)', 'type == 10'))]),
    ('lne', [(L, '''		if (*pr) {
			if (type == 9) {
				if (!suGetCF(&e->data, &e->size))
					break;
			} else {
				if (type != 10)
					break;
				if (!suGetCG(&e->data, &e->size))
					break;
				goto chk;
			}
		}
''')]),
    ('l10', [(L, '''		if (*pr) {
			if (type == 10) {
				if (!suGetCG(&e->data, &e->size))
					break;
				goto chk;
			}
			if (type != 9)
				break;
			if (!suGetCF(&e->data, &e->size))
				break;
		}
''')]),
    ('lsw', [(L, '''		if (*pr) {
			switch (type) {
			case 9:
				if (!suGetCF(&e->data, &e->size))
					return;
				break;
			case 10:
				if (!suGetCG(&e->data, &e->size))
					return;
				goto chk;
			default:
				return;
			}
		}
''')]),
]
AXES = [A, B]
