"""extractSmcConfig after findSmcConfig: the plain copy as a static function (its src is then a parameter, and buf isn't live across);
exp_400 and pin_src off.  Also each scan loop in a helper of its own."""
import itertools
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
H = {
    'a': ('static void copySmcConfig(struct fileent *e, const uint8_t *src, uint32_t avail)\n{\n' + LOG + '	if (avail >= 0x400)\n		memcpy(e->data, src, 0x400);\n}\n\n',
          '		copySmcConfig(e, buf + i, size - i);\n'),
    'b': ('static void copySmcConfig(uint8_t *dst, const uint8_t *src, uint32_t avail)\n{\n' + LOG + '	if (avail >= 0x400)\n		memcpy(dst, src, 0x400);\n}\n\n',
          '		copySmcConfig(e->data, buf + i, size - i);\n'),
    'c': ('static void copySmcConfig(struct fileent *e, const uint8_t *src)\n{\n	memcpy(e->data, src, 0x400);\n}\n\n',
          '		log_printf(1, "extracting config\\n");\n		if (size - i >= 0x400)\n			copySmcConfig(e, buf + i);\n'),
    'd': ('', '		log_printf(1, "extracting config\\n");\n		if (size - i >= 0x400)\n			memcpy(e->data, buf + i, 0x400);\n'),
    'e': ('static void copySmcConfig(struct fileent *e, const uint8_t *buf, uint32_t i, int size)\n{\n' + LOG + '	if (size - i >= 0x400)\n		memcpy(e->data, buf + i, 0x400);\n}\n\n',
          '		copySmcConfig(e, buf, i, size);\n'),
}
A = [(k, [(OLD, c), (HEAD, d + HEAD)]) for k, (d, c) in H.items()]
AXES = [A]
FOCUS = ['_extractSmcConfig']
