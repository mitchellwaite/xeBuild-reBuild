"""extractSmcConfig's copy: pin on src/buf and the expect on the room test"""
FOCUS = ['_extractSmcConfig']
Q = '''		if (__builtin_expect(size - i >= 0x400, 1)) {
			uint8_t *src = buf + i;

			/* buf live past src: no IRA copy buf-src, so the raw
			   loop's eax doesn't push dst out of eax (tools/wip/README) */
			__asm__("" : "+r"(src) : "r"(buf));
			memcpy(e->data, src, 0x400);
		}
'''


def v(s):
    return [(Q, s)]


T = ['size - i >= 0x400', 'size - i > 0x3ff', '0x400 <= size - i', 'i + 0x400 <= size', 'size >= i + 0x400']
B = [
    ('direct', '			memcpy(e->data, buf + i, 0x400);\n'),
    ('src', '			uint8_t *src = buf + i;\n\n			memcpy(e->data, src, 0x400);\n'),
    ('dst', '			uint8_t *dst = e->data;\n\n			memcpy(dst, buf + i, 0x400);\n'),
    ('both', '			uint8_t *src = buf + i, *dst = e->data;\n\n			memcpy(dst, src, 0x400);\n'),
    ('dstfirst', '			uint8_t *dst = e->data, *src = buf + i;\n\n			memcpy(dst, src, 0x400);\n'),
    ('void', '			void *src = buf + i;\n\n			memcpy(e->data, src, 0x400);\n'),
    ('const', '			const uint8_t *src = buf + i;\n\n			memcpy(e->data, src, 0x400);\n'),
]
shapes = []
for ti, t in enumerate(T):
    for bn, b in B:
        shapes.append(('t%d%s' % (ti, bn), v('		if (%s) {\n%s		}\n' % (t, b))))
        shapes.append(('e%d%s' % (ti, bn), v('		if (__builtin_expect(%s, 1)) {\n%s		}\n' % (t, b))))
        shapes.append(('g%d%s' % (ti, bn), v('		if (!(%s))\n			goto copied;\n		{\n%s		}\ncopied:\n' % (t, b))))
AXES = [shapes]
