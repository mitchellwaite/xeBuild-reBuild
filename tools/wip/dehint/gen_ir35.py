"""getImageSmc from attempt 2's draft: bad arm inline; which of the optimize options are needed; each hint's cost."""
FOCUS = ['_getImageSmc']
BASE = 'tools/wip/dehint/drafts/image_read_attempt2.c'
B0 = '''	if (addr != 0x800 && addr != 0x1000)
		goto bad;
bback:
'''
BEND = '''	return;
bad:
	bhot: __attribute__((hot));
	log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);
	addr = 0x1000;
	goto bback;
}'''
AX1 = [
    ('bk', []),
    ('bin', [(B0, '''	if (addr != 0x800 && addr != 0x1000) {
		bhot: __attribute__((hot));
		log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);
		addr = 0x1000;
	}
'''), (BEND, '}')]),
    ('bin0', [(B0, '''	if (addr != 0x800 && addr != 0x1000) {
		log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);
		addr = 0x1000;
	}
'''), (BEND, '}')]),
    ('bnh', [('	bhot: __attribute__((hot));\n', '')]),
]
ATTR = '__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc'
AX2 = [('o3', []),
       ('o-i1', [(ATTR, '__attribute__((optimize("no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc')]),
       ('o-i2', [(ATTR, '__attribute__((optimize("no-if-conversion", "no-tree-tail-merge"))) void getImageSmc')]),
       ('o-tm', [(ATTR, '__attribute__((optimize("no-if-conversion", "no-if-conversion2"))) void getImageSmc')]),
       ('oi1', [(ATTR, '__attribute__((optimize("no-if-conversion"))) void getImageSmc')]),
       ('oi2', [(ATTR, '__attribute__((optimize("no-if-conversion2"))) void getImageSmc')]),
       ('otm', [(ATTR, '__attribute__((optimize("no-tree-tail-merge"))) void getImageSmc')]),
       ('o0', [(ATTR, 'void getImageSmc')]),
       ]
V = '''	} else {
		vhot: __attribute__((hot));
	}
'''
AX3 = [('vk', []), ('v0', [(V, '	}\n')])]
AX4 = [('sk', []), ('s0', [('		shot: __attribute__((hot));\n', '')])]
AXES = [AX1, AX2, AX3, AX4]
