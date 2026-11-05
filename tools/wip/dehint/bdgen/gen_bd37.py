# extractSmcConfig without (void)&size: only the second scan's bound test keeps the wrong operand order (cmp ebp,esi).
REMOVE = ['addr_size']
FOCUS = ['_extractSmcConfig']
Q2 = '''		for (i = 0; __builtin_expect(i + 0x210 <= size, 1); i += 0x210)
			if ((found = smcConfigOk(buf + i)) == 1)
				break;
'''
E = '__builtin_expect(%s, 1)'
A = [
    ('', []),
    ('ge', [(Q2, Q2.replace('i + 0x210 <= size', 'size >= i + 0x210'))]),
    ('next', [('	uint32_t i, j;\n', '	uint32_t i, j, next;\n'), (Q2, '''		for (i = 0; next = i + 0x210, __builtin_expect(next <= size, 1); i = next)
			if ((found = smcConfigOk(buf + i)) == 1)
				break;
''')]),
    ('next2', [('	uint32_t i, j;\n', '	uint32_t i, j, next;\n'), (Q2, '''		for (i = 0, next = 0x210; __builtin_expect(next <= size, 1); i = next, next += 0x210)
			if ((found = smcConfigOk(buf + i)) == 1)
				break;
''')]),
    ('while', [(Q2, '''		i = 0;
		while (__builtin_expect(i + 0x210 <= size, 1)) {
			if ((found = smcConfigOk(buf + i)) == 1)
				break;
			i += 0x210;
		}
''')]),
    ('brk', [(Q2, '''		for (i = 0; ; i += 0x210) {
			if (__builtin_expect(i + 0x210 > size, 0))
				break;
			if ((found = smcConfigOk(buf + i)) == 1)
				break;
		}
''')]),
    ('neg', [(Q2, Q2.replace('__builtin_expect(i + 0x210 <= size, 1)', '!__builtin_expect(i + 0x210 > size, 0)'))]),
    ('lt', [(Q2, Q2.replace('i + 0x210 <= size', 'i + 0x20f < size'))]),
    ('sub', [(Q2, Q2.replace('i + 0x210 <= size', 'size - i >= 0x210'))]),
]
AXES = [A]
