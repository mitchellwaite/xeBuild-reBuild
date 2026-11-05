"""extractSmcConfig: gen_bd80's form e (18 lines, the pin_src difference), spellings of the copy inside it."""
OLD = '''		log_printf(1, "extracting config\\n");
		if (__builtin_expect(size - i >= 0x400, 1)) {
			uint8_t *src = buf + i;

			/* buf live past src: no IRA copy buf-src, so the raw
			   loop's eax doesn't push dst out of eax (tools/wip/README) */
			__asm__("" : "+r"(src) : "r"(buf));
			memcpy(e->data, src, 0x400);
		}
'''
HEAD = 'int extractSmcConfig(struct fileent *e, uint8_t *buf, int size)\n{'
LOG = '	log_printf(1, "extracting config\\n");\n'
PARAMS = {
    'p1': ('struct fileent *e, const uint8_t *buf, uint32_t i, int size', 'e, buf, i, size'),
    'p2': ('struct fileent *e, uint8_t *buf, uint32_t i, int size', 'e, buf, i, size'),
    'p3': ('struct fileent *e, uint8_t *buf, int size, uint32_t i', 'e, buf, size, i'),
    'p4': ('uint8_t *buf, int size, uint32_t i, struct fileent *e', 'buf, size, i, e'),
}
BODIES = {
    'plain': LOG + '	if (size - i >= 0x400)\n		memcpy(e->data, buf + i, 0x400);\n',
    'src': LOG + '	if (size - i >= 0x400) {\n		const uint8_t *src = buf + i;\n\n		memcpy(e->data, src, 0x400);\n	}\n',
    'dst': LOG + '	if (size - i >= 0x400) {\n		uint8_t *dst = e->data;\n\n		memcpy(dst, buf + i, 0x400);\n	}\n',
    'both': LOG + '	if (size - i >= 0x400) {\n		uint8_t *dst = e->data;\n		const uint8_t *src = buf + i;\n\n		memcpy(dst, src, 0x400);\n	}\n',
    'early': LOG + '	if (size - i < 0x400)\n		return;\n	memcpy(e->data, buf + i, 0x400);\n',
    'addr': LOG + '	if (size - i >= 0x400)\n		memcpy(e->data, &buf[i], 0x400);\n',
    'avail': '	int avail = size - i;\n\n' + LOG + '	if (avail >= 0x400)\n		memcpy(e->data, buf + i, 0x400);\n',
    'uavail': '	uint32_t avail = size - i;\n\n' + LOG + '	if (avail >= 0x400)\n		memcpy(e->data, buf + i, 0x400);\n',
    'struct': LOG + '	if (size - i >= 0x400) {\n		struct cfgblk { uint8_t b[0x400]; };\n\n		*(struct cfgblk *)e->data = *(const struct cfgblk *)(buf + i);\n	}\n',
}
A = []
for pk, (pd, pc) in PARAMS.items():
    for bk, b in BODIES.items():
        q = pd if 'const' not in pd or bk != 'struct' else pd
        A.append((pk + '-' + bk, [(OLD, '		copySmcConfig(%s);\n' % pc), (HEAD, 'static void copySmcConfig(%s)\n{\n' % q + b + '}\n\n' + HEAD)]))
AXES = [A]
FOCUS = ['_extractSmcConfig']
