"""fsGetFile without pin_v: fsFind's match test forms (they set off's frequency against the return value's), the found test, v's test (attempt 13)."""
FOCUS = ['_fsGetFile']
PIN = '	/* code-free hint: fsValid (reused for return 1) in esi, name in edi */\n	__asm__("" : : "S"(v));\n'
M0 = '''		if (fs->ent[i].name[0] && !stricmp(fs->ent[i].name, name)) {
			*size = SWAP32(fs->ent[i].size);
			*block = SWAP16(fs->ent[i].block);
			if (time)
				*time = SWAP32(fs->ent[i].time);
			if (!quiet)
				log_printf(1, "%s found in sector 0x%x size 0x%x...", name, *block, *size);
			return 1;
		}
'''
BODY = '''*size = SWAP32(fs->ent[i].size);
			*block = SWAP16(fs->ent[i].block);
			if (time)
				*time = SWAP32(fs->ent[i].time);
			if (!quiet)
				log_printf(1, "%s found in sector 0x%x size 0x%x...", name, *block, *size);
			return 1;
'''
M = [
 ('and', []),
 ('nest', [(M0, '		if (fs->ent[i].name[0]) {\n			if (!stricmp(fs->ent[i].name, name)) {\n' + BODY + '			}\n		}\n')]),
 ('cont', [(M0, '		if (!fs->ent[i].name[0])\n			continue;\n		if (stricmp(fs->ent[i].name, name))\n			continue;\n' + BODY)]),
 ('cont2', [(M0, '		if (!fs->ent[i].name[0] || stricmp(fs->ent[i].name, name))\n			continue;\n' + BODY)]),
 ('z', [(M0, '		if (fs->ent[i].name[0] != 0 && stricmp(fs->ent[i].name, name) == 0) {\n' + BODY + '		}\n')]),
 ('fl', [(M0, '		int m = fs->ent[i].name[0] && !stricmp(fs->ent[i].name, name);\n		if (m > 0) {\n' + BODY + '		}\n')]),
 ('fl2', [(M0, '		int c = 1;\n		if (fs->ent[i].name[0])\n			c = stricmp(fs->ent[i].name, name);\n		if (c == 0) {\n' + BODY + '		}\n')]),
]
F0 = '	if (!fsFind(name, &block, &len, &t, 1))\n		return 0;\n	off = fsOffset'
F = [
 ('f', []),
 ('fne', [(F0, '	if (fsFind(name, &block, &len, &t, 1) != 1)\n		return 0;\n	off = fsOffset')]),
 ('feq', [(F0, '	if (fsFind(name, &block, &len, &t, 1) == 1) {\n	off = fsOffset'),
          ('	*time = t;\n	return 1;\n}\n\nint findAnchor', '	*time = t;\n	return 1;\n	}\n	return 0;\n}\n\nint findAnchor')]),
 ('fle', [('	int v = fsValid;\n', '	int v = fsValid;\n	int f;\n'), (F0, '	f = fsFind(name, &block, &len, &t, 1);\n	if (f <= 0)\n		return 0;\n	off = fsOffset')]),
 ('fgt', [('	int v = fsValid;\n', '	int v = fsValid;\n	int f;\n'), (F0, '	f = fsFind(name, &block, &len, &t, 1);\n	if (f > 0) {\n	off = fsOffset'),
          ('	*time = t;\n	return 1;\n}\n\nint findAnchor', '	*time = t;\n	return 1;\n	}\n	return 0;\n}\n\nint findAnchor')]),
]
V = [
 ('v', []),
 ('veq', [('	if (v != 1)\n		return 0;\n	if', '	if (v == 1) {} else\n		return 0;\n	if')]),
 ('vfl', [('	if (v != 1)\n		return 0;\n	if', '	int u = v == 1;\n	if (u <= 0)\n		return 0;\n	if')]),
 ('vgl', [('	int v = fsValid;\n', ''), ('	if (v != 1)\n		return 0;\n	if', '	if (fsValid != 1)\n		return 0;\n	if')]),
]
AXES = [[('', [(PIN, '')])], M, F, V]
