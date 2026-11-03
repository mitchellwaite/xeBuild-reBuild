# writeFsTable without optimize("no-tree-scev-cprop"): body forms
BASE = 'tools/wip/dehint/drafts/image_write.c'
FOCUS = ['_writeFsTable']
A = '__attribute__((optimize("no-tree-scev-cprop"))) void writeFsTable'
LOOP = '''	p = buf;
	for (i = 0; i < 16; i++) {
		memcpy(p, (uint8_t *)fsTable + i * 0x200, 0x200);
		p += 0x200;
		memcpy(p, (uint8_t *)fsFiles + i * 0x200, 0x200);
		p += 0x200;
	}
'''
CALLS = '''	if (!xb.bigBlock)
		goto small;
	imgAdd(off, buf, i * 0x400, 0x2c, 0x1ffe, 0);
	goto done;
small:
	imgAdd(off, buf, i * 0x400, 0x30, 0x1ffd, 0);
done:
'''
LOG = '''	log_printf(1, "offset 0x%x len 0x4000 (end 0x%x)...", off, off + 0x4000);
'''
loops = {
    'l0': LOOP,
    'l1': '''	p = buf;
	for (i = 0; i < 16; i++) {
		memcpy(p, (uint8_t *)fsTable + i * 0x200, 0x200);
		memcpy(p + 0x200, (uint8_t *)fsFiles + i * 0x200, 0x200);
		p += 0x400;
	}
''',
    'l2': '''	p = buf;
	i = 0;
	while (i < 16) {
		memcpy(p, (uint8_t *)fsTable + i * 0x200, 0x200);
		p += 0x200;
		memcpy(p, (uint8_t *)fsFiles + i * 0x200, 0x200);
		p += 0x200;
		i++;
	}
''',
    'l3': '''	p = buf;
	for (i = 0; i != 16; i++) {
		memcpy(p, (uint8_t *)fsTable + i * 0x200, 0x200);
		p += 0x200;
		memcpy(p, (uint8_t *)fsFiles + i * 0x200, 0x200);
		p += 0x200;
	}
''',
    'l4': '''	p = buf;
	for (i = 0; i < 16; i++) {
		memcpy(p, (uint8_t *)fsTable + i * 0x200, 0x200);
		memcpy(p + 0x200, (uint8_t *)fsFiles + i * 0x200, 0x200);
		p += 0x200 * 2;
	}
''',
    'l5': '''	for (i = 0, p = buf; i < 16; i++, p += 0x400) {
		memcpy(p, (uint8_t *)fsTable + i * 0x200, 0x200);
		memcpy(p + 0x200, (uint8_t *)fsFiles + i * 0x200, 0x200);
	}
''',
    'l6': '''	p = buf;
	for (i = 0; i < 16; i++) {
		memcpy(p, (uint8_t *)fsTable + i * 0x200, 0x200);
		p += 0x200;
		memcpy(p, (uint8_t *)fsFiles + i * 0x200, 0x200);
		p += 0x200;
	}
	len = i * 0x400;
''',
}
calls = {
    'c0': CALLS,
    'c1': CALLS.replace('i * 0x400', 'len') ,
    'c2': CALLS.replace('	imgAdd(off, buf, i * 0x400, 0x2c', '	imgAdd(off, buf, i << 10, 0x2c').replace('	imgAdd(off, buf, i * 0x400, 0x30', '	imgAdd(off, buf, i << 10, 0x30'),
    'c3': CALLS.replace('i * 0x400', '(uint32_t)(p - buf)'),
}
log = {
    'g0': LOG,
    'g1': '	log_printf(1, "offset 0x%x len 0x4000 (end 0x%x)...", off, off + i * 0x400);\n',
}
axis = []
for l in loops:
    for c in calls:
        for g in log:
            ed = [(A, 'void writeFsTable'), (LOOP, loops[l]), (CALLS, calls[c]), (LOG, log[g])]
            if c == 'c1' or l == 'l6':
                if l != 'l6' or c != 'c1':
                    continue
                ed.append(('	int i;\n\n	blk = off >> 14;', '	int i;\n	uint32_t len;\n\n	blk = off >> 14;'))
            axis.append((l + c + g, ed))
AXES = [axis]
