"""loadConsoleBlFiles: the update-fallback in error-variable forms, checkBl only if r is clear, with exp_t9 and the cold label off."""
import itertools

OLD = '''				if (r) {
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
				r = checkBl(e->data, e->size, type, e->crc);
				break;
'''
F = {
    'cur': OLD.replace('__builtin_expect(type == 9, 0)', 'type == 9'),
    'ifnot': '''				if (r) {
					if (type == 9) {
						if (suGetCF(&e->data, &e->size))
							r = 0;
					} else if (type == 10) {
						if (suGetCG(&e->data, &e->size))
							r = 0;
					}
				}
				if (!r)
					r = checkBl(e->data, e->size, type, e->crc);
				break;
''',
    'and': '''				if (r && type == 9) {
					if (suGetCF(&e->data, &e->size))
						r = 0;
				} else if (r && type == 10) {
					if (suGetCG(&e->data, &e->size))
						r = 0;
				}
				if (!r)
					r = checkBl(e->data, e->size, type, e->crc);
				break;
''',
    'and2': '''				if (r && type == 9 && suGetCF(&e->data, &e->size))
					r = 0;
				if (r && type == 10 && suGetCG(&e->data, &e->size))
					r = 0;
				if (!r)
					r = checkBl(e->data, e->size, type, e->crc);
				break;
''',
    'and3': '''				if (r && type == 9 && suGetCF(&e->data, &e->size))
					r = 0;
				else if (r && type == 10 && suGetCG(&e->data, &e->size))
					r = 0;
				if (!r)
					r = checkBl(e->data, e->size, type, e->crc);
				break;
''',
    'seq': '''				if (r) {
					if (type == 9 && suGetCF(&e->data, &e->size))
						r = 0;
					else if (type == 10 && suGetCG(&e->data, &e->size))
						r = 0;
				}
				if (!r)
					r = checkBl(e->data, e->size, type, e->crc);
				break;
''',
    'seq2': '''				if (r) {
					if (type == 9 && suGetCF(&e->data, &e->size))
						r = 0;
					else if (type == 10 && suGetCG(&e->data, &e->size))
						r = 0;
					if (r)
						break;
				}
				r = checkBl(e->data, e->size, type, e->crc);
				break;
''',
    'else': '''				if (!r)
					r = checkBl(e->data, e->size, type, e->crc);
				else if (type == 9) {
					if (suGetCF(&e->data, &e->size))
						r = checkBl(e->data, e->size, type, e->crc);
				} else if (type == 10) {
					if (suGetCG(&e->data, &e->size))
						r = checkBl(e->data, e->size, type, e->crc);
				}
				break;
''',
}
PRECHECK = '''	/* the cold label gives the shrink-wrapped return 0 frequency 0, so
	   bb-reorder lays it out last */
	if ((uint32_t)xb.nFiles <= 1)
		goto none;
'''
COLD = 'none: __attribute__((cold));\n\treturn 0;\n'


def CASES(base):
    out = []
    for f, c in itertools.product(F, ('cold', 'plain', 'nolabel')):
        t = base.replace(OLD, F[f])
        if c == 'plain':
            t = t.replace(COLD, 'none:\n\treturn 0;\n')
        elif c == 'nolabel':
            t = t.replace(PRECHECK, '').replace(COLD, '')
            t = t.replace('	return 0;\n	return 0;\n', '	return 0;\n')
        out.append(('%s %s' % (f, c), t))
    return out
