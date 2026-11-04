# attempt 10: pin_hdr's load order, on the expect-75 stand-in for (A) (drafts/image_write_near9_hdr.c, 4 lines; IWB= another base).  The free stack at PRE holds the unrolled spareUsed
# chain from the bbController loop, so spareUsed's form (and how that loop calls it) could change which names PRE pops.  Wanted: IDENTICAL.
import os
SU = '''	int i;

	for (i = 0; i < 16; i++)
		if (s[i] != 0xff)
			return 1;
	return 0;
'''
CALL = '''			if (!spareUsed(xb.spare + i * 16))
				continue;
'''
SF = {
 '': SU,
 'a': '	int i;\n\n	for (i = 0; i < 16; i++)\n		if (s[i] != 0xff)\n			break;\n	return i < 16;\n',
 'b': '	int i;\n\n	for (i = 0; i < 16; i++)\n		if (s[i] != 0xff)\n			break;\n	if (i < 16)\n		return 1;\n	return 0;\n',
 'c': '	int i;\n\n	for (i = 0; i < 16; i++) {\n		if (s[i] == 0xff)\n			continue;\n		return 1;\n	}\n	return 0;\n',
 'd': '	int i, used = 0;\n\n	for (i = 0; i < 16; i++)\n		if (s[i] != 0xff) {\n			used = 1;\n			break;\n		}\n	return used;\n',
 'e': '	int i = 0;\n\n	do {\n		if (s[i] != 0xff)\n			return 1;\n	} while (++i < 16);\n	return 0;\n',
 'f': '	int i = 16;\n\n	while (i--)\n		if (*s++ != 0xff)\n			return 1;\n	return 0;\n',
 'g': '	const uint8_t *e = s + 16;\n\n	for (; s < e; s++)\n		if (*s != 0xff)\n			return 1;\n	return 0;\n',
 'h': '	int i;\n\n	for (i = 0; i < 16; i++)\n		if (s[i] != 0xff)\n			return 1;\n	return i != 16;\n',
}
CF = {
 '': CALL,
 'x': '			if (spareUsed(xb.spare + i * 16) == 0)\n				continue;\n',
 'y': '			uint8_t *sp = xb.spare + i * 16;\n\n			if (!spareUsed(sp))\n				continue;\n',
}
AXES = [
 [(k, [(SU + '}\n\nuint8_t *imageGetBuffer', v + '}\n\nuint8_t *imageGetBuffer')]) for k, v in SF.items()],
 [(k, [(CALL, v)]) for k, v in CF.items() if k != 'y'] + [('y', [('			uint8_t t;\n\n' + CALL, '			uint8_t t;\n			uint8_t *sp = xb.spare + i * 16;\n\n			if (!spareUsed(sp))\n				continue;\n')])],
]
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_near9_hdr.c')
FLAGS = ['--param', 'builtin-expect-probability=75']
