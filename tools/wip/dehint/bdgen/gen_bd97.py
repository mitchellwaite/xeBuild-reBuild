"""The xell room check with its warning as a helper shared by addBlsToImage and addUpdateBls."""
OLD1 = '''		} else if (type == 25 && __builtin_expect(type != 24, 1) && e->offset < imgSize()) {
			log_printf(0, "***** WARNING: skipping xell, there doesn't appear to be enough room!\\n");
			continue;
		}
'''
OLD2 = '''		if (type == 25 && e->offset < imgSize()) {
			log_printf(0, "***** WARNING: skipping xell, there doesn't appear to be enough room!\\n");
			continue;
		}
'''
H = {
    'fits': '''static int xellFits(const struct fileent *e)
{
	if (e->offset < imgSize()) {
		log_printf(0, "***** WARNING: skipping xell, there doesn't appear to be enough room!\\n");
		return 0;
	}
	return 1;
}

''',
    'fits2': '''static int xellFits(const struct fileent *e)
{
	if (e->offset >= imgSize())
		return 1;
	log_printf(0, "***** WARNING: skipping xell, there doesn't appear to be enough room!\\n");
	return 0;
}

''',
}
NOROOM = '''static int xellNoRoom(const struct fileent *e)
{
	if (e->offset < imgSize()) {
		log_printf(0, "***** WARNING: skipping xell, there doesn't appear to be enough room!\\n");
		return 1;
	}
	return 0;
}

'''
ANCH = 'void addBlsToImage(void)\n'


def CASES(base):
    out = []
    for hn, h in list(H.items()) + [('noroom', NOROOM)]:
        call = '!xellFits(e)' if hn != 'noroom' else 'xellNoRoom(e)'
        for w in ('1', '12'):
            for form in ('and', 'nest'):
                t = base.replace(ANCH, h + ANCH)
                if form == 'and':
                    t = t.replace(OLD1, '		} else if (type == 25 && %s)\n			continue;\n' % call)
                    if '2' in w:
                        t = t.replace(OLD2, '		if (type == 25 && %s)\n			continue;\n' % call)
                else:
                    t = t.replace(OLD1, '		} else if (type == 25) {\n			if (%s)\n				continue;\n		}\n' % call)
                    if '2' in w:
                        t = t.replace(OLD2, '		if (type == 25) {\n			if (%s)\n				continue;\n		}\n' % call)
                out.append(('%s %s %s' % (hn, w, form), t))
    return out
