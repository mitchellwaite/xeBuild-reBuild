# extractSmcConfig's pin_src and pin_i now that size is an int: spellings of the copy, and of the scans.
FOCUS = ['_extractSmcConfig']
OLD = '''		if (__builtin_expect(size - i >= 0x400, 1)) {
			uint8_t *src = buf + i;

			/* buf live past src: no IRA copy buf-src, so the raw
			   loop's eax doesn't push dst out of eax (tools/wip/README) */
			__asm__("" : "+r"(src) : "r"(buf));
			memcpy(e->data, src, 0x400);
		}
'''
EXP = '__builtin_expect(size - i >= 0x400, 1)'
FORMS = {
    'plain': '''		if (%s)
			memcpy(e->data, buf + i, 0x400);
''',
    'src': '''		if (%s) {
			uint8_t *src = buf + i;

			memcpy(e->data, src, 0x400);
		}
''',
    'dst': '''		if (%s) {
			uint8_t *dst = e->data;

			memcpy(dst, buf + i, 0x400);
		}
''',
    'both': '''		if (%s) {
			uint8_t *dst = e->data, *src = buf + i;

			memcpy(dst, src, 0x400);
		}
''',
}
TESTS = {'e': EXP, 'n': 'size - i >= 0x400', 'c': 'i + 0x400 <= (uint32_t)size', 'r': '(uint32_t)size - i >= 0x400'}
A = [(a + b, [(OLD, f % t)]) for a, f in FORMS.items() for b, t in TESTS.items()]
Q1 = '''		__asm__("" : : "S"(i + 0x200), "D"(buf));
'''
B = [('', []), ('nopin', [(Q1, '')])]
AXES = [A, B]
