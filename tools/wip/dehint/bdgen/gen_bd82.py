"""extractSmcConfig: the struct copy of gen_bd81 without the helper, with a named struct at file scope."""
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
ST = '/* a whole smc config */\nstruct smcConfigData {\n	uint8_t b[0x400];\n};\n\n'
LOG = '	log_printf(1, "extracting config\\n");\n'
COPY = '*(struct smcConfigData *)e->data = *(const struct smcConfigData *)(buf + i);\n'
A = [
    ('inplace', [(OLD, LOG.replace('\t', '\t\t') + '		if (size - i >= 0x400)\n			' + COPY), (HEAD, ST + HEAD)]),
    ('inplace-e', [(OLD, LOG.replace('\t', '\t\t') + '		if (__builtin_expect(size - i >= 0x400, 1))\n			' + COPY), (HEAD, ST + HEAD)]),
    ('helper', [(OLD, '		copySmcConfig(e, buf, i, size);\n'), (HEAD, ST + 'static void copySmcConfig(struct fileent *e, const uint8_t *buf, uint32_t i, int size)\n{\n' + LOG + '	if (size - i >= 0x400)\n		' + COPY + '}\n\n' + HEAD)]),
    ('helper-nolog', [(OLD, LOG.replace('\t', '\t\t') + '		if (size - i >= 0x400)\n			copySmcConfig(e, buf + i);\n'), (HEAD, ST + 'static void copySmcConfig(struct fileent *e, const uint8_t *src)\n{\n	*(struct smcConfigData *)e->data = *(const struct smcConfigData *)src;\n}\n\n' + HEAD)]),
]
AXES = [A]
FOCUS = ['_extractSmcConfig']
