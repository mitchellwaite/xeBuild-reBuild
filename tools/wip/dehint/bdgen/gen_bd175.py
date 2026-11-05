"""exp_upd: the exported isUpdateBl's mask has bit 23 and addUpdateBls' copy doesn't.  So perhaps the loop tests 23 itself before calling it, and the call's own 23 folds."""
import itertools

OLD = 'return __builtin_expect(type == 23 || type == 15, 0) || type == 16 || type == 9 || type == 10 || type == 24 || type == 25;'
PLAIN = {
    'o': 'return type == 23 || type == 15 || type == 16 || type == 9 || type == 10 || type == 24 || type == 25;',
    'e': 'return type == 9 || type == 10 || type == 15 || type == 16 || type == 23 || type == 24 || type == 25;',
}
LOOP = '''		if (!isUpdateBl(type))
			continue;
		if (e->offset != 0xffffffff)
			off = e->offset;
		if (!strnicmp(e->name, "none", 4) && !e->crc)
			continue;
'''
F = {
    'and': '		if (type != 23 && !isUpdateBl(type))\n			continue;\n',
    'or': '		if (!(type == 23 || isUpdateBl(type)))\n			continue;\n',
    'then': '		if (type == 23)\n			;\n		else if (!isUpdateBl(type))\n			continue;\n',
    'nest': '		if (type != 23) {\n			if (!isUpdateBl(type))\n				continue;\n		}\n',
}
REST = LOOP[LOOP.index('		if (e->offset'):]


def CASES(base):
    out = []
    for p, f in itertools.product(PLAIN, F):
        t = base.replace(OLD, PLAIN[p])
        if LOOP not in t:
            raise ValueError('loop')
        out.append(('%s %s' % (p, f), t.replace(LOOP, F[f] + REST)))
    return out


FOCUS = ['_addUpdateBls', '_isUpdateBl']
