"""loadConsoleBlFiles without the cold label: r = 1 must out-rank the no-files return (15 vs 20)"""
FOCUS = ['_loadConsoleBlFiles']
H = '''	if ((uint32_t)xb.nFiles <= 1)
		goto none;
	for (i = 1; i < (uint32_t)xb.nFiles; i++) {
'''
T = '''			return -1;
		}
	}
	return 0;
none: __attribute__((cold));
	return 0;
}
'''
TP = '''			return -1;
		}
	}
	return 0;
}
'''
Q = '''				if (!xb.glitch2mfg || (!loadBaseFile(e->name, e) && e->size == 0x60))
					break;
				e->data = malloc(0x60);
				if (!e->data) {
					r = 1;
					break;
				}
				{
					uint8_t *p = e->data;

					/* p's points-to unknown: the size store may alias the
					   copy, so sched2 keeps it before the rep movsd setup */
					__asm__("" : "+r"(p));
					e->size = 0x60;
					memcpy(__builtin_assume_aligned(p, 4), defBl60, 0x60);
				}
				break;
'''
K = '''					uint8_t *p = e->data;

					__asm__("" : "+r"(p));
					e->size = 0x60;
					memcpy(__builtin_assume_aligned(p, 4), defBl60, 0x60);
'''
A = [
    ('', []),
    ('nest', [(Q, '''				if (xb.glitch2mfg) {
					if (loadBaseFile(e->name, e) || e->size != 0x60) {
						e->data = malloc(0x60);
						if (!e->data) {
							r = 1;
							break;
						}
						{
''' + K + '''						}
					}
				}
				break;
''')]),
    ('and', [(Q, '''				if (xb.glitch2mfg && (loadBaseFile(e->name, e) || e->size != 0x60)) {
					e->data = malloc(0x60);
					if (!e->data) {
						r = 1;
						break;
					}
					{
''' + K + '''					}
				}
				break;
''')]),
    ('else', [(Q, '''				if (!xb.glitch2mfg || (!loadBaseFile(e->name, e) && e->size == 0x60))
					break;
				e->data = malloc(0x60);
				if (e->data) {
''' + K + '''				} else
					r = 1;
				break;
''')]),
    ('two', [(Q, '''				if (!xb.glitch2mfg)
					break;
				if (!loadBaseFile(e->name, e) && e->size == 0x60)
					break;
				e->data = malloc(0x60);
				if (!e->data) {
					r = 1;
					break;
				}
				{
''' + K + '''				}
				break;
''')]),
    ('three', [(Q, '''				if (!xb.glitch2mfg)
					break;
				if (!loadBaseFile(e->name, e)) {
					if (e->size == 0x60)
						break;
				}
				e->data = malloc(0x60);
				if (!e->data) {
					r = 1;
					break;
				}
				{
''' + K + '''				}
				break;
''')]),
]
B = [
    ('plain', [(H, '	for (i = 1; i < (uint32_t)xb.nFiles; i++) {\n'), (T, TP)]),
    ('while', [(H, '	i = 1;\n	while (i < (uint32_t)xb.nFiles) {\n'), (T, '''			return -1;
		}
		i++;
	}
	return 0;
}
''')]),
]
AXES = [A, B]
