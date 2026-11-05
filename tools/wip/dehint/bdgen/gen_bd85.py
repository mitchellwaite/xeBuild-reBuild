"""exp_t24 off: the xell room test as a static function (two calls inside, not early inlined), in addBlsToImage and optionally addUpdateBls."""
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
HEAD = 'void addBlsToImage(void)\n{'
LOG = '''log_printf(0, "***** WARNING: skipping xell, there doesn't appear to be enough room!\\n");'''
H = {
    'a': 'static int xellNoRoom(struct fileent *e)\n{\n	if (e->offset < imgSize()) {\n		' + LOG + '\n		return 1;\n	}\n	return 0;\n}\n\n',
    'b': 'static int xellFits(struct fileent *e)\n{\n	if (e->offset >= imgSize())\n		return 1;\n	' + LOG + '\n	return 0;\n}\n\n',
    'c': 'static int xellNoRoom(struct fileent *e)\n{\n	int r = 0;\n\n	if (e->offset < imgSize()) {\n		' + LOG + '\n		r = 1;\n	}\n	return r;\n}\n\n',
}
C = {
    'a': ('		} else if (type == 25 && xellNoRoom(e))\n			continue;\n', '		if (type == 25 && xellNoRoom(e))\n			continue;\n'),
    'b': ('		} else if (type == 25 && !xellFits(e))\n			continue;\n', '		if (type == 25 && !xellFits(e))\n			continue;\n'),
    'c': ('		} else if (type == 25 && xellNoRoom(e))\n			continue;\n', '		if (type == 25 && xellNoRoom(e))\n			continue;\n'),
}
A = []
for k in H:
    A.append((k + '1', [(OLD1, C[k][0]), (HEAD, H[k] + HEAD)]))
    A.append((k + '2', [(OLD1, C[k][0]), (OLD2, C[k][1]), (HEAD, H[k] + HEAD)]))
A.append(('nest', [(OLD1, '		} else if (type == 25) {\n			if (e->offset < imgSize()) {\n				' + LOG + '\n				continue;\n			}\n		}\n')]))
AXES = [A]
