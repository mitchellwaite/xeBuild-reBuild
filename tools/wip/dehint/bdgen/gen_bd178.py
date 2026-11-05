"""Natural shapes for two landed oddities, using helpers with calls (not early inlined, so their own predictions survive):
case 24's repeated calls as a loadBl60 helper (`c`), and `else if (type)` as a signature helper (`s`)."""
import itertools

HEAD = '/* load the input file e (xb.files[i]) by its type */\n'
A1 = '''			if (loadBaseFile(e->name, e))
				*pr = defaultBl60(e);
			else if (e->size != 0x60)
				*pr = defaultBl60(e);
		}
		if (xb.type == BUILD_DEVGL'''
A2 = '''			*pr = 0;
			if (loadBaseFile(e->name, e))
				*pr = defaultBl60(e);
			else if (e->size != 0x60)
				*pr = defaultBl60(e);
'''
A3 = '''				if (loadBaseFile(e->name, e))
					r = defaultBl60(e);
				else if (e->size != 0x60)
					r = defaultBl60(e);
'''
H60 = {
    'ret': '''static int loadBl60(struct fileent *e)
{
	if (loadBaseFile(e->name, e))
		return defaultBl60(e);
	if (e->size != 0x60)
		return defaultBl60(e);
	return 0;
}

''',
    'or': '''static int loadBl60(struct fileent *e)
{
	if (loadBaseFile(e->name, e) || e->size != 0x60)
		return defaultBl60(e);
	return 0;
}

''',
    'r': '''static int loadBl60(struct fileent *e)
{
	int r = 0;

	if (loadBaseFile(e->name, e))
		r = defaultBl60(e);
	else if (e->size != 0x60)
		r = defaultBl60(e);
	return r;
}

''',
}
SIG = '''			if (xb.pub1bl) {
				if (!cbVerifySig(e->data, xb.pub1bl)) {
					log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);
					*pr = -1;
				/* Borderline, for review: type is 5, 11 or 17 here, so this test
				   is always true; a plain else costs 54 lines */
				} else if (type)
					log_printf(1, "loaded %s, signature check passed!\\n", e->name);
			} else
				log_printf(1, "loaded %s, could not check signature rsa key not present!\\n", e->name);
'''
HS = {
    'nest': '''static int checkBlSig(struct fileent *e)
{
	if (xb.pub1bl) {
		if (!cbVerifySig(e->data, xb.pub1bl)) {
			log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);
			return -1;
		}
		log_printf(1, "loaded %s, signature check passed!\\n", e->name);
	} else
		log_printf(1, "loaded %s, could not check signature rsa key not present!\\n", e->name);
	return 0;
}

''',
    'r': '''static int checkBlSig(struct fileent *e)
{
	int r = 0;

	if (xb.pub1bl) {
		if (!cbVerifySig(e->data, xb.pub1bl)) {
			log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);
			r = -1;
		} else
			log_printf(1, "loaded %s, signature check passed!\\n", e->name);
	} else
		log_printf(1, "loaded %s, could not check signature rsa key not present!\\n", e->name);
	return r;
}

''',
}


def CASES(base):
    out = []
    for h, m in itertools.product(H60, range(1, 8)):
        def f(t, h=h, m=m):
            if m & 1:
                t = t.replace(A1, '			*pr = loadBl60(e);\n		}\n		if (xb.type == BUILD_DEVGL')
            if m & 2:
                t = t.replace(A2, '			*pr = loadBl60(e);\n')
            if m & 4:
                t = t.replace(A3, '				r = loadBl60(e);\n')
            return t.replace(HEAD, H60[h] + HEAD)
        out.append(('c %s %d' % (h, m), f))
    for h in HS:
        def f(t, h=h):
            if SIG not in t:
                raise ValueError('sig')
            return t.replace(SIG, '			*pr = checkBlSig(e);\n').replace(HEAD, HS[h] + HEAD)
        out.append(('s %s' % h, f))
    return out


FOCUS = ['_loadBlFiles', '_loadConsoleBlFiles']
