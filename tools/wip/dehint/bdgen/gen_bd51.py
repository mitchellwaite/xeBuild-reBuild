"""loadFileCrc without the verbose expect: the "bytes" log needs >= 2000.  P(verbose) * P(size == e->size) >= about 25%.
Forms of the verbose test, the equal test and the pad test."""
REMOVE = []
FOCUS = ['_loadFileCrc']
OLD = '''	if (__builtin_expect(verbose, 1)) {
		if (size != e->size) {
			log_printf(1, "reading %s (0x%x b pad 0x%x b)", name, size, (size + 15) & ~15);
			__asm__("" : : "S"(e));
		} else
			log_printf(1, "reading %s (0x%x bytes)", name, size);
	}
'''
PAD = '''		log_printf(1, "reading %s (0x%x b pad 0x%x b)", name, size, (size + 15) & ~15);
'''
BYTES = '''		log_printf(1, "reading %s (0x%x bytes)", name, size);
'''


def body(eq):
    if eq == 'ne':
        return '\t\tif (size != e->size) {\n\t' + PAD + '\t\t} else\n\t' + BYTES
    if eq == 'eq':
        return '\t\tif (size == e->size) {\n\t' + BYTES + '\t\t} else {\n\t' + PAD + '\t\t}\n'
    if eq == 'pin':
        return '\t\tif (size != e->size) {\n\t' + PAD + '\t\t\t__asm__("" : : "S"(e));\n\t\t} else\n\t' + BYTES
    if eq == 'eqgoto':
        return '\t\tif (size == e->size) {\n\t' + BYTES + '\t\t\tgoto logged;\n\t\t}\n\t' + PAD
    if eq == 'negoto':
        return '\t\tif (size != e->size) {\n\t' + PAD + '\t\t\tgoto logged;\n\t\t}\n\t' + BYTES
    if eq == 'sep':
        return '\t\tif (size != e->size)\n\t' + PAD + '\t\tif (size == e->size)\n\t' + BYTES


VS = {
    'v': 'if (verbose) {\n%s\t}\n',
    'gt': 'if (verbose > 0) {\n%s\t}\n',
    'ge1': 'if (verbose >= 1) {\n%s\t}\n',
    'eq1': 'if (verbose == 1) {\n%s\t}\n',
    'ne0': 'if (verbose != 0) {\n%s\t}\n',
}

ax1 = []
for v, vs in VS.items():
    for eq in ('ne', 'eq', 'pin', 'eqgoto', 'negoto', 'sep'):
        new = '\t' + vs % body(eq)
        if 'goto logged' in new:
            new += 'logged:\n'
        ax1.append(('%s-%s' % (v, eq), [(OLD, new)]))
for eq in ('ne', 'eq', 'pin', 'eqgoto', 'negoto', 'sep'):
    for t in ('!verbose', 'verbose <= 0', 'verbose < 1'):
        new = '\tif (%s)\n\t\tgoto logged;\n' % t + body(eq).replace('\t\t', '\t', 99).replace('\n\t\t', '\n\t\t') + 'logged:\n'
        ax1.append(('goto(%s)-%s' % (t, eq), [(OLD, new)]))
ax2 = [
    ('', []),
    ('nest', [('''	if (pad && (size & 15))
		e->size = (size + 15) & ~15;
''', '''	if (pad) {
		if (size & 15)
			e->size = (size + 15) & ~15;
	}
''')]),
]
AXES = [ax1, ax2]
