# loadBl's first case-24 arm with its own pair of copies (written out, or in a helper), the second arm plain.
# Base: gen_bd22's orig+c0.
BASE = 'build/bd/gen_bd22_best.c'
OLD24 = '''		if (xb.type == BUILD_JTAG || xb.glitch2mfg)
			*pr = loadBl60(e);
'''
C1 = '''e->data = malloc(0x60);
if (!e->data)
	*pr = 1;
else {
	e->size = 0x60;
	memcpy(e->data, defBl60, 0x60);
}
'''
C2 = '''e->data = malloc(0x60);
if (e->data) {
	e->size = 0x60;
	memcpy(e->data, defBl60, 0x60);
} else
	*pr = 1;
'''


def ind(s, n):
    return ''.join('\t' * n + l + '\n' for l in s.splitlines())


def nest(c):
    return '''		if (xb.type == BUILD_JTAG || xb.glitch2mfg) {
			if (loadBaseFile(e->name, e)) {
''' + ind(c, 4) + '''			} else if (e->size != 0x60) {
''' + ind(c, 4) + '''			}
		}
'''


def rev(c):
    return '''		if (xb.type == BUILD_JTAG || xb.glitch2mfg) {
			if (!loadBaseFile(e->name, e)) {
				if (e->size != 0x60) {
''' + ind(c, 5) + '''				}
			} else {
''' + ind(c, 4) + '''			}
		}
'''


HELP = '''/* load the input file e (xb.files[i]) by its type */
static void loadBl('''
HELPER = '''static int loadBl60b(struct fileent *e)
{
	if (loadBaseFile(e->name, e)) {
		e->data = malloc(0x60);
		if (!e->data)
			return 1;
		e->size = 0x60;
		memcpy(e->data, defBl60, 0x60);
	} else if (e->size != 0x60) {
		e->data = malloc(0x60);
		if (!e->data)
			return 1;
		e->size = 0x60;
		memcpy(e->data, defBl60, 0x60);
	}
	return 0;
}

''' + HELP
OLD60 = '''static int loadBl60(struct fileent *e)
{
	if (loadBaseFile(e->name, e) || e->size != 0x60) {
		e->data = malloc(0x60);
		if (!e->data)
			return 1;
		e->size = 0x60;
		memcpy(e->data, defBl60, 0x60);
	}
	return 0;
}
'''
AXES = [[
    ('n1', [(OLD24, nest(C1))]), ('n2', [(OLD24, nest(C2))]),
    ('r1', [(OLD24, rev(C1))]), ('r2', [(OLD24, rev(C2))]),
    ('helper', [(HELP, HELPER), (OLD24, '''		if (xb.type == BUILD_JTAG || xb.glitch2mfg)
			*pr = loadBl60b(e);
''')]),
    ('helper2nd', [(HELP, HELPER), ('''		if (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16)
			*pr = loadBl60(e);
''', '''		if (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16)
			*pr = loadBl60b(e);
''')]),
    ('elsehelper', [(OLD24, '''		if (xb.type == BUILD_JTAG) {
			*pr = loadBl60(e);
		} else if (xb.glitch2mfg) {
			*pr = loadBl60(e);
		}
''')]),
]]
